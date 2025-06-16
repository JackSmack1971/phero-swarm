import asyncio
import json
import os
import time
from pathlib import Path
from typing import Any, Dict

import yaml
from src.pheromone_handler import PheromoneHandler, PheromoneHandlerError
from src.traffic_controller import determine_route, RoutingError


class SystemHealthError(Exception):
    """Raised when system health checks fail."""


async def check_config_files() -> None:
    """Ensure core configuration files exist and are valid JSON."""
    for name in [".swarmConfig", os.getenv("PHEROMONE_FILE", ".pheromone")]:
        path = Path(name)
        if not path.exists():
            raise SystemHealthError(f"{name} missing")
        try:
            await asyncio.to_thread(json.load, open(path))
        except json.JSONDecodeError as exc:
            raise SystemHealthError(f"{name} invalid") from exc


async def check_roomodes(path: str = ".roomodes") -> None:
    """Validate mode definitions if present."""
    file = Path(path)
    if not file.exists():
        print(f"Warning: {path} not found")
        return
    try:
        await asyncio.to_thread(yaml.safe_load, file.read_text())
    except yaml.YAMLError as exc:
        raise SystemHealthError("roomodes malformed") from exc


async def test_pheromone_ops() -> None:
    """Read and immediately rewrite pheromone to ensure file operations work."""
    handler = PheromoneHandler(os.getenv("PHEROMONE_FILE", ".pheromone"))
    try:
        data = await handler.read_safe()
        if data is None:
            raise SystemHealthError("pheromone unreadable")
        await handler.write_safe(data)
    except PheromoneHandlerError as exc:
        raise SystemHealthError("pheromone handler failure") from exc


async def verify_routing() -> None:
    """Confirm traffic controller can route a simple signal."""
    signal = {
        "id": "health-check",
        "signalType": "test",
        "category": "need",
        "strength": 5.0,
        "message": "verify routing",
        "timestamp": int(time.time()),
    }
    data = {"signals": [signal]}
    agent = await determine_route(data)
    if agent != "tester-tdd-master":
        raise SystemHealthError("routing incorrect")


async def main() -> None:
    try:
        await check_config_files()
        await check_roomodes()
        await test_pheromone_ops()
        await verify_routing()
        print("System healthy")
    except SystemHealthError as exc:
        print(f"Health issue: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
