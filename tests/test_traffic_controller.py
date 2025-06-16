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
    RoutingError,
)


@pytest.mark.asyncio
async def test_load_json_file(tmp_path):
    file = tmp_path / "config.json"
    file.write_text("{\"a\": 1}")
    data = await load_json_file(str(file))
    assert data["a"] == 1


@pytest.mark.asyncio
async def test_load_json_file_error(tmp_path):
    file = tmp_path / "bad.json"
    file.write_text("{bad}")
    with pytest.raises(RoutingError):
        await load_json_file(str(file))


@pytest.mark.asyncio
async def test_load_config_and_pheromone(tmp_path):
    cfg = tmp_path / "config.json"
    pher = tmp_path / "state.json"
    cfg.write_text(json.dumps({"pheromoneFile": str(pher)}))
    pher.write_text("{\"signals\": []}")
    config = await load_config(str(cfg))
    data = await load_pheromone(config)
    assert data["signals"] == []


def test_determine_route_compass():
    pheromone = {"signals": [{"category": "compass"}]}
    assert determine_route(pheromone) == "concept-to-blueprint-translator"


def test_determine_route_need_coder():
    pheromone = {"signals": [{"category": "need", "message": "implement"}]}
    assert determine_route(pheromone) == "coder-test-driven"


def test_determine_route_need_testing():
    pheromone = {"signals": [{"category": "need", "signalType": "test_addition"}]}
    assert determine_route(pheromone) == "tester-tdd-master"


def test_determine_route_block():
    pheromone = {"signals": [{"category": "block"}]}
    assert determine_route(pheromone) == "debugger-targeted"


def test_determine_route_default():
    assert determine_route({"signals": []}) == "orchestrator-pheromone-scribe"

