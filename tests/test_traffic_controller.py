import json
import asyncio
from pathlib import Path
import sys
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.traffic_controller import (
    load_json_file,
    load_config,
    load_pheromone,
    determine_route,
    add_coordination_signal,
    RoutingError,
    PheromoneHandler,
)


@pytest.mark.asyncio
async def test_load_json_file(tmp_path: Path) -> None:
    file = tmp_path / "config.json"
    file.write_text('{"a": 1}')
    data = await load_json_file(str(file))
    assert data["a"] == 1


@pytest.mark.asyncio
async def test_load_json_file_error(tmp_path: Path) -> None:
    file = tmp_path / "bad.json"
    file.write_text('{bad}')
    with pytest.raises(RoutingError):
        await load_json_file(str(file))


@pytest.mark.asyncio
async def test_load_config_and_pheromone(tmp_path: Path) -> None:
    cfg = tmp_path / "config.json"
    pher = tmp_path / "state.json"
    cfg.write_text(json.dumps({"pheromoneFile": str(pher)}))
    pher.write_text('{"signals": []}')
    config = await load_config(str(cfg))
    data = await load_pheromone(config)
    assert data["signals"] == []


@pytest.mark.asyncio
async def test_routing_rules(tmp_path: Path) -> None:
    handler = PheromoneHandler(str(tmp_path / "pher.json"))
    pheromone = {
        "signals": [
            {"category": "need", "message": "requires architecture", "strength": 5.0},
            {"category": "need", "signalType": "test", "strength": 9.0},
        ]
    }
    agent = await determine_route(pheromone, handler)
    assert agent == "tester-tdd-master"
    data = await handler.read_safe()
    assert data["signals"][-1]["target"] == agent


@pytest.mark.asyncio
async def test_fallback_and_coordination(tmp_path: Path) -> None:
    handler = PheromoneHandler(str(tmp_path / "pher.json"))
    agent = await determine_route({"signals": []}, handler)
    assert agent == "orchestrator-pheromone-scribe"
    data = await handler.read_safe()
    assert data["signals"][0]["target"] == agent


@pytest.mark.asyncio
async def test_priority_block(tmp_path: Path) -> None:
    handler = PheromoneHandler(str(tmp_path / "pher.json"))
    pheromone = {
        "signals": [
            {"category": "compass", "strength": 2.0},
            {"category": "block", "strength": 9.0},
        ]
    }
    agent = await determine_route(pheromone, handler)
    assert agent == "debugger-targeted"

