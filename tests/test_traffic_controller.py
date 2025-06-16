import json
import asyncio
from pathlib import Path
import sys
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src import traffic_controller as tc
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


@pytest.mark.asyncio
async def test_determine_route_compass(tmp_path, monkeypatch):
    tc.CONTEXT_FILE = str(tmp_path / "ctx.json")
    tc.METRICS_FILE = str(tmp_path / "m.json")
    pheromone = {"signals": [{"category": "compass"}]}
    agent = await determine_route(pheromone)
    assert agent == "concept-to-blueprint-translator"


@pytest.mark.asyncio
async def test_determine_route_need_coder(tmp_path, monkeypatch):
    tc.CONTEXT_FILE = str(tmp_path / "ctx.json")
    tc.METRICS_FILE = str(tmp_path / "m.json")
    pheromone = {"signals": [{"category": "need", "message": "implement"}]}
    agent = await determine_route(pheromone)
    assert agent == "coder-test-driven"


@pytest.mark.asyncio
async def test_determine_route_need_testing(tmp_path):
    tc.CONTEXT_FILE = str(tmp_path / "ctx.json")
    tc.METRICS_FILE = str(tmp_path / "m.json")
    pheromone = {"signals": [{"category": "need", "signalType": "test_addition"}]}
    agent = await determine_route(pheromone)
    assert agent == "tester-tdd-master"


@pytest.mark.asyncio
async def test_determine_route_block(tmp_path):
    tc.CONTEXT_FILE = str(tmp_path / "ctx.json")
    tc.METRICS_FILE = str(tmp_path / "m.json")
    pheromone = {"signals": [{"category": "block"}]}
    agent = await determine_route(pheromone)
    assert agent == "debugger-targeted"


@pytest.mark.asyncio
async def test_determine_route_default(tmp_path):
    tc.CONTEXT_FILE = str(tmp_path / "ctx.json")
    tc.METRICS_FILE = str(tmp_path / "m.json")
    agent = await determine_route({"signals": []})
    assert agent == "orchestrator-pheromone-scribe"


@pytest.mark.asyncio
async def test_specialist_routing_security(tmp_path):
    tc.CONTEXT_FILE = str(tmp_path / "ctx.json")
    tc.METRICS_FILE = str(tmp_path / "m.json")
    pheromone = {
        "signals": [
            {
                "category": "block",
                "signalType": "security_error",
                "strength": 9.0,
                "message": "Security vulnerability found",
            }
        ]
    }
    agent = await determine_route(pheromone)
    assert agent == "security-validator"


@pytest.mark.asyncio
async def test_context_continuity(tmp_path):
    tc.CONTEXT_FILE = str(tmp_path / "ctx.json")
    tc.METRICS_FILE = str(tmp_path / "m.json")
    # First call stores context
    pher1 = {
        "signals": [
            {
                "category": "need",
                "signalType": "test_task",
                "context": {"id": "123"},
                "message": "needs tests",
            }
        ]
    }
    await determine_route(pher1)
    # Next signal with same context should return same agent
    pher2 = {"signals": [{"category": "need", "context": {"id": "123"}}]}
    agent = await determine_route(pher2)
    assert agent == "tester-tdd-master"


@pytest.mark.asyncio
async def test_circuit_breaker(tmp_path):
    tc.CONTEXT_FILE = str(tmp_path / "ctx.json")
    tc.METRICS_FILE = str(tmp_path / "m.json")
    # Write failing metrics for tester-tdd-master
    metrics = {"tester-tdd-master": {"failures": 6, "total": 10}}
    (Path(tc.METRICS_FILE)).write_text(json.dumps(metrics))
    pheromone = {"signals": [{"category": "need", "signalType": "test"}]}
    agent = await determine_route(pheromone)
    assert agent == "coder-test-driven"

