import asyncio
import time
from pathlib import Path
import pytest

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from coordination_monitor import CoordinationMonitor
from src.pheromone_handler import PheromoneHandler, PheromoneHandlerError
from src.traffic_controller import determine_route


@pytest.mark.asyncio
async def test_pheromone_corruption_resistance(tmp_path: Path) -> None:
    path = tmp_path / "pher.json"
    handler = PheromoneHandler(str(path))
    good = {"signals": []}
    await handler.write_safe(good)
    path.write_text("{bad}")
    assert await handler.read_safe() == good


@pytest.mark.asyncio
async def test_traffic_controller_routing_accuracy() -> None:
    data = {"signals": [{"id": "1", "signalType": "req", "category": "need", "strength": 5.0, "message": "write tests", "timestamp": 1}]}
    assert await determine_route(data) == "tester-tdd-master"


@pytest.mark.asyncio
async def test_mode_handoff_completion(tmp_path: Path) -> None:
    handler = PheromoneHandler(str(tmp_path / "p.json"))
    start = {"id": "1", "signalType": "start", "category": "compass", "strength": 5.0, "message": "idea", "timestamp": 1}
    await handler.write_safe({"signals": [start]})
    agent = await determine_route(await handler.read_safe(), handler)
    assert agent == "concept-to-blueprint-translator"
    await handler.clear_signals_by_category("compass")
    await handler.add_signal({"id": "2", "signalType": "bp", "category": "need", "strength": 6.0, "message": "architecture", "timestamp": 2})
    agent = await determine_route(await handler.read_safe(), handler)
    assert agent == "architect-highlevel-module"


@pytest.mark.asyncio
async def test_signal_lifecycle_management(tmp_path: Path) -> None:
    handler = PheromoneHandler(str(tmp_path / "p.json"))
    await handler.write_safe({"signals": []})
    sig = {"id": "1", "signalType": "t", "category": "need", "strength": 1.0, "message": "m", "timestamp": 1}
    await handler.add_signal(sig)
    data = await handler.read_safe()
    assert len(data["signals"]) == 1
    await handler.clear_signals_by_category("need")
    data = await handler.read_safe()
    assert data["signals"] == []


@pytest.mark.asyncio
async def test_error_recovery_mechanisms(tmp_path: Path) -> None:
    path = tmp_path / "pher.json"
    handler = PheromoneHandler(str(path))
    old = {"id": "1", "signalType": "route", "category": "coordinate", "strength": 5.0, "target": "a", "message": "old", "timestamp": int(time.time()) - 400}
    await handler.write_safe({"signals": [old]})
    monitor = CoordinationMonitor(str(path), stall_min=1, expiry_min=5)
    await monitor.check_once()
    data = await handler.read_safe()
    assert any(s.get("target") == "orchestrator-pheromone-scribe" for s in data["signals"])


@pytest.mark.asyncio
async def test_full_project_workflow(tmp_path: Path) -> None:
    handler = PheromoneHandler(str(tmp_path / "p.json"))
    await handler.write_safe({"signals": []})
    await handler.add_signal({"id": "c1", "signalType": "new", "category": "compass", "strength": 5.0, "message": "start", "timestamp": 1})
    agent = await determine_route(await handler.read_safe())
    assert agent == "concept-to-blueprint-translator"
    await handler.clear_signals_by_category("compass")
    await handler.add_signal({"id": "c2", "signalType": "bp", "category": "need", "strength": 6.0, "message": "architecture plan", "timestamp": 2})
    agent = await determine_route(await handler.read_safe())
    assert agent == "architect-highlevel-module"
    await handler.clear_signals_by_category("need")
    await handler.add_signal({"id": "c3", "signalType": "design", "category": "need", "strength": 6.0, "message": "code implementation", "timestamp": 3})
    agent = await determine_route(await handler.read_safe())
    assert agent == "coder-test-driven"
    await handler.clear_signals_by_category("need")
    await handler.add_signal({"id": "c4", "signalType": "impl", "category": "need", "strength": 6.0, "message": "test cases", "timestamp": 4})
    agent = await determine_route(await handler.read_safe())
    assert agent == "tester-tdd-master"


@pytest.mark.asyncio
async def test_error_injection_and_recovery(tmp_path: Path) -> None:
    path = tmp_path / "pher.json"
    handler = PheromoneHandler(str(path))
    await handler.write_safe({"signals": []})
    path.write_text("{bad}")
    assert await handler.read_safe() == {"signals": []}


@pytest.mark.asyncio
async def test_concurrent_access_protection(tmp_path: Path) -> None:
    handler = PheromoneHandler(str(tmp_path / "p.json"))
    await handler.write_safe({"signals": []})
    for i in range(5):
        sig = {"id": str(i), "signalType": "t", "category": "need", "strength": 1.0, "message": "m", "timestamp": i}
        await handler.add_signal(sig)
    data = await handler.read_safe()
    assert len(data["signals"]) == 5


@pytest.mark.asyncio
async def test_signal_malformation_handling(tmp_path: Path) -> None:
    handler = PheromoneHandler(str(tmp_path / "p.json"))
    with pytest.raises(PheromoneHandlerError):
        await handler.write_safe({"signals": [{}]})
