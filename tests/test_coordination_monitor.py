import json
import time
import pytest

from coordination_monitor import (
    detect_coordination_deadlock,
    analyze_signal_health,
    suggest_next_action,
    cleanup_expired_signals,
    CoordinationMonitor,
)
from src.pheromone_handler import PheromoneHandler


@pytest.mark.asyncio
async def test_detect_deadlock_due_to_stall() -> None:
    now = int(time.time()) - 600
    assert detect_coordination_deadlock([{"timestamp": now}], 300)


@pytest.mark.asyncio
async def test_detect_deadlock_circular() -> None:
    now = int(time.time())
    signals = [
        {"category": "coordinate", "target": "a", "timestamp": now - 10},
        {"category": "coordinate", "target": "a", "timestamp": now - 5},
        {"category": "coordinate", "target": "a", "timestamp": now - 1},
    ]
    assert detect_coordination_deadlock(signals, 60)


def test_analyze_signal_health_expired_and_malformed() -> None:
    now = int(time.time())
    good = {"id": "1", "signalType": "x", "category": "need", "strength": 1.0, "message": "m", "timestamp": now}
    old = {"id": "2", "signalType": "x", "category": "need", "strength": 1.0, "message": "m", "timestamp": now - 1000}
    bad = {"id": "3", "signalType": "x"}
    res = analyze_signal_health([good, old, bad], 60)
    assert old in res and bad in res and good not in res


def test_suggest_next_action_returns_agent() -> None:
    now = int(time.time())
    sig = {"category": "need", "message": "test suite", "signalType": "req", "strength": 5, "timestamp": now}
    assert suggest_next_action([sig]) == "tester-tdd-master"


def test_cleanup_expired_signals() -> None:
    now = int(time.time())
    valid = {"timestamp": now}
    old = {"timestamp": now - 100}
    assert cleanup_expired_signals([valid, old], 60) == [valid]


@pytest.mark.asyncio
async def test_monitor_check_once_resets_deadlock(tmp_path) -> None:
    file = tmp_path / "pher.json"
    stale = {
        "id": "1",
        "signalType": "route",
        "category": "coordinate",
        "strength": 5.0,
        "target": "a",
        "message": "old",
        "timestamp": int(time.time()) - 400,
    }
    file.write_text(json.dumps({"signals": [stale]}))
    monitor = CoordinationMonitor(str(file), stall_min=1, expiry_min=5)
    await monitor.check_once()
    data = await PheromoneHandler(str(file)).read_safe()
    assert any(s.get("target") == "orchestrator-pheromone-scribe" for s in data["signals"])
