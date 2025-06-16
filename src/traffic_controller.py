import asyncio
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from src.pheromone_handler import PheromoneHandler, PheromoneHandlerError
except ImportError:  # pragma: no cover - fallback for direct execution
    from pheromone_handler import PheromoneHandler, PheromoneHandlerError


class RoutingError(Exception):
    """Custom exception for routing failures."""


WORKLOAD_CACHE: Dict[str, int] = {}
METRICS_FILE = os.getenv("METRICS_FILE", ".traffic_metrics.json")
CONTEXT_FILE = os.getenv("CONTEXT_FILE", ".traffic_context.json")


async def load_json_file(path: str) -> Dict[str, Any]:
    """Asynchronously load a JSON file."""
    try:
        return json.loads(await asyncio.to_thread(Path(path).read_text))
    except (OSError, json.JSONDecodeError) as exc:
        raise RoutingError(f"Unable to load {path}") from exc


async def save_json_file(path: str, data: Dict[str, Any]) -> None:
    """Persist data as JSON asynchronously."""
    try:
        await asyncio.to_thread(Path(path).write_text, json.dumps(data))
    except OSError as exc:
        raise RoutingError(f"Unable to save {path}") from exc


async def load_metrics() -> Dict[str, Any]:
    """Load routing metrics."""
    try:
        return await load_json_file(METRICS_FILE)
    except RoutingError:
        return {}


async def save_metrics(metrics: Dict[str, Any]) -> None:
    """Save routing metrics."""
    await save_json_file(METRICS_FILE, metrics)


async def load_context_cache() -> Dict[str, str]:
    """Load context-to-agent mapping."""
    try:
        return await load_json_file(CONTEXT_FILE)
    except RoutingError:
        return {}


async def save_context_cache(cache: Dict[str, str]) -> None:
    """Persist context mapping."""
    await save_json_file(CONTEXT_FILE, cache)


def least_busy_agent(candidates: List[str]) -> str:
    """Return least busy agent from candidates and update workload."""
    if not candidates:
        raise RoutingError("No candidates provided")
    for agent in candidates:
        WORKLOAD_CACHE.setdefault(agent, 0)
    chosen = min(candidates, key=lambda a: WORKLOAD_CACHE[a])
    WORKLOAD_CACHE[chosen] += 1
    return chosen


async def add_coordination_signal(handler: PheromoneHandler, agent: str) -> None:
    """Record routing decision."""
    signal = {
        "id": f"coord-{int(time.time())}",
        "signalType": "routing_decision",
        "category": "coordinate",
        "strength": 5.0,
        "target": agent,
        "message": f"Routed to {agent}",
        "timestamp": int(time.time()),
    }
    try:
        await handler.add_signal(signal)
    except PheromoneHandlerError as exc:
        raise RoutingError("Failed to update pheromone") from exc




async def load_config(config_path: str) -> Dict[str, Any]:
    """Load swarm configuration."""
    return await load_json_file(config_path)


async def load_pheromone(config: Dict[str, Any]) -> Dict[str, Any]:
    """Load pheromone using PheromoneHandler."""
    path = config.get("pheromoneFile", ".pheromone")
    handler = PheromoneHandler(path)
    try:
        data = await handler.read_safe()
    except PheromoneHandlerError as exc:
        raise RoutingError("Failed to read pheromone") from exc
    return data or {"signals": []}


def analyze_signal(signal: Dict[str, Any]) -> Optional[str]:
    """Return preferred agent for a signal."""
    text = f"{signal.get('signalType','')} {signal.get('message','')}".lower()
    category = signal.get("category")
    if category == "compass":
        return "concept-to-blueprint-translator"
    if category == "need":
        if "test" in text:
            return "tester-tdd-master"
        if "architecture" in text:
            return "architect-highlevel-module"
        return "coder-test-driven"
    if category == "block":
        return "debugger-targeted"
    return None


async def determine_route(pheromone: Dict[str, Any], handler: Optional[PheromoneHandler] | None = None) -> str:
    """Return next agent and record coordination."""
    signals = sorted(
        pheromone.get("signals", []),
        key=lambda s: s.get("strength", 0),
        reverse=True,
    )
    for sig in signals:
        agent = analyze_signal(sig)
        if agent:
            if handler:
                await add_coordination_signal(handler, agent)
            return least_busy_agent([agent])
    fallback = "orchestrator-pheromone-scribe"
    if handler:
        await add_coordination_signal(handler, fallback)
    return fallback


async def main() -> None:
    config = await load_config(".swarmConfig")
    pheromone = await load_pheromone(config)
    handler = PheromoneHandler(config.get("pheromoneFile", ".pheromone"))
    next_agent = await determine_route(pheromone, handler)
    print(next_agent)


if __name__ == "__main__":
    asyncio.run(main())
