import asyncio
import json
from pathlib import Path
from typing import Any, Dict


class RoutingError(Exception):
    """Custom exception for routing failures."""


async def load_json_file(path: str) -> Dict[str, Any]:
    """Asynchronously load a JSON file."""
    try:
        return json.loads(await asyncio.to_thread(Path(path).read_text))
    except (OSError, json.JSONDecodeError) as exc:
        raise RoutingError(f"Unable to load {path}") from exc


async def load_config(config_path: str) -> Dict[str, Any]:
    """Load swarm configuration."""
    return await load_json_file(config_path)


async def load_pheromone(config: Dict[str, Any]) -> Dict[str, Any]:
    """Load pheromone state using config path."""
    pheromone_path = config.get("pheromoneFile", ".pheromone")
    return await load_json_file(pheromone_path)


def determine_route(pheromone: Dict[str, Any]) -> str:
    """Determine next agent based on pheromone signals."""
    for signal in pheromone.get("signals", []):
        category = signal.get("category")
        stype = signal.get("signalType", "").lower()
        msg = signal.get("message", "").lower()
        if category == "compass":
            return "concept-to-blueprint-translator"
        if category == "need":
            if "test" in stype or "quality" in stype or "test" in msg:
                return "tester-tdd-master"
            return "coder-test-driven"
        if category == "block":
            return "debugger-targeted"
    return "orchestrator-pheromone-scribe"


async def main() -> None:
    config = await load_config(".swarmConfig")
    pheromone = await load_pheromone(config)
    next_agent = determine_route(pheromone)
    print(next_agent)


if __name__ == "__main__":
    asyncio.run(main())
