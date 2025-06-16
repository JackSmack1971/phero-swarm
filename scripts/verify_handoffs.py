import asyncio
import tempfile
from pathlib import Path

from src.pheromone_handler import PheromoneHandler
from scripts.handoff_scripts import (
    blueprint_complete_handoff,
    architecture_complete_handoff,
    code_complete_handoff,
    test_complete_handoff,
)
from src.traffic_controller import determine_route


async def verify_chain() -> bool:
    path = Path(tempfile.mktemp())
    handler = PheromoneHandler(str(path))
    await blueprint_complete_handoff(str(path))
    route = await determine_route(await handler.read_safe() or {}, handler)
    if route != "architect-highlevel-module":
        return False
    await architecture_complete_handoff(str(path))
    route = await determine_route(await handler.read_safe() or {}, handler)
    if route != "coder-test-driven":
        return False
    await code_complete_handoff(str(path))
    route = await determine_route(await handler.read_safe() or {}, handler)
    if route != "tester-tdd-master":
        return False
    await test_complete_handoff(str(path))
    route = await determine_route(await handler.read_safe() or {}, handler)
    return route == "coder-test-driven"


async def main() -> None:
    result = await verify_chain()
    print("handoff chain ok" if result else "handoff chain failed")


if __name__ == "__main__":
    asyncio.run(main())
