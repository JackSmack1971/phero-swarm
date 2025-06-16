import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class RoutingError(Exception):
    """Custom exception for routing failures."""


WORKLOAD_CACHE: Dict[str, int] = {}
METRICS_FILE = ".traffic_metrics.json"
CONTEXT_FILE = ".traffic_context.json"
SPECIALIST_MAP = {
    "security": "security-validator",
    "performance": "performance-optimizer",
    "test": "tester-tdd-master",
}


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


def specialist_route(signal: Dict[str, Any]) -> Optional[str]:
    """Route block signals to specialists when appropriate."""
    if signal.get("category") != "block" or signal.get("strength", 0) <= 8.0:
        return None
    text = f"{signal.get('signalType','')} {signal.get('message','')}".lower()
    for key, agent in SPECIALIST_MAP.items():
        if key in text:
            return agent
    return SPECIALIST_MAP.get("test") if "test" in text else None


def circuit_breaker(metrics: Dict[str, Any], agent: str) -> bool:
    """Check if agent should be temporarily disabled."""
    stat = metrics.get(agent, {})
    failures = stat.get("failures", 0)
    total = stat.get("total", 0)
    return total > 5 and failures / total > 0.5


def update_routing_history(metrics: Dict[str, Any], context_id: str, agent: str) -> bool:
    """Record routing history and detect potential loops."""
    history = metrics.setdefault("routing_history", {}).setdefault(context_id, [])
    history.append(agent)
    if len(history) > 5:
        history.pop(0)
    return len(history) >= 3 and len(set(history[-3:])) == 1


async def load_config(config_path: str) -> Dict[str, Any]:
    """Load swarm configuration."""
    return await load_json_file(config_path)


async def load_pheromone(config: Dict[str, Any]) -> Dict[str, Any]:
    """Load pheromone state using config path."""
    pheromone_path = config.get("pheromoneFile", ".pheromone")
    return await load_json_file(pheromone_path)


def analyze_signal(signal: Dict[str, Any], ctx: Dict[str, str], metrics: Dict[str, Any]) -> Optional[str]:
    """Return preferred agent for a single signal."""
    context_id = signal.get("context", {}).get("id")
    if context_id and ctx.get(context_id) and not circuit_breaker(metrics, ctx[context_id]):
        return ctx[context_id]

    agent = specialist_route(signal)
    if agent:
        if not circuit_breaker(metrics, agent):
            if context_id:
                ctx[context_id] = agent
            return agent

    category = signal.get("category")
    stype = signal.get("signalType", "").lower()
    msg = signal.get("message", "").lower()
    if category == "compass":
        agent = "concept-to-blueprint-translator"
        if context_id:
            ctx[context_id] = agent
        return agent
    if category == "need":
        agent = "tester-tdd-master" if "test" in stype or "test" in msg else "coder-test-driven"
        if context_id:
            ctx[context_id] = agent
        return agent
    if category == "block":
        agent = "debugger-targeted"
        if context_id:
            ctx[context_id] = agent
        return agent
    return None


async def determine_route(pheromone: Dict[str, Any]) -> str:
    """Determine next agent considering context and load."""
    metrics = await load_metrics()
    ctx = await load_context_cache()
    for signal in pheromone.get("signals", []):
        agent = analyze_signal(signal, ctx, metrics)
        if agent:
            if circuit_breaker(metrics, agent):
                fallback = "coder-test-driven" if agent == "tester-tdd-master" else "debugger-targeted"
                await save_context_cache(ctx)
                return least_busy_agent([fallback])
            cid = signal.get("context", {}).get("id")
            if cid and update_routing_history(metrics, cid, agent):
                await save_metrics(metrics)
                await save_context_cache(ctx)
                return least_busy_agent(["orchestrator-pheromone-scribe"])
            await save_context_cache(ctx)
            await save_metrics(metrics)
            return least_busy_agent([agent])
    await save_context_cache(ctx)
    await save_metrics(metrics)
    return least_busy_agent(["orchestrator-pheromone-scribe"])


async def main() -> None:
    config = await load_config(".swarmConfig")
    pheromone = await load_pheromone(config)
    next_agent = await determine_route(pheromone)
    print(next_agent)


if __name__ == "__main__":
    asyncio.run(main())
