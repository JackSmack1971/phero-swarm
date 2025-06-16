import json
from pathlib import Path
import pytest

from src.pheromone_handler import PheromoneHandler, PheromoneHandlerError


@pytest.mark.asyncio
async def test_write_and_read(tmp_path: Path) -> None:
    p = tmp_path / "pheromone.json"
    handler = PheromoneHandler(str(p))
    data = {"signals": []}
    await handler.write_safe(data)
    loaded = await handler.read_safe()
    assert loaded == data


@pytest.mark.asyncio
async def test_add_and_clear(tmp_path: Path) -> None:
    p = tmp_path / "pheromone.json"
    handler = PheromoneHandler(str(p))
    signal = {
        "id": "1",
        "signalType": "test",
        "category": "need",
        "strength": 5.0,
        "message": "hi",
        "timestamp": 1,
    }
    await handler.add_signal(signal)
    data = await handler.read_safe()
    assert len(data["signals"]) == 1
    await handler.clear_signals_by_category("need")
    data = await handler.read_safe()
    assert data["signals"] == []


@pytest.mark.asyncio
async def test_corruption_recovery(tmp_path: Path) -> None:
    p = tmp_path / "pheromone.json"
    handler = PheromoneHandler(str(p))
    good = {"signals": []}
    await handler.write_safe(good)
    p.write_text("{bad}")
    recovered = await handler.read_safe()
    assert recovered == good


@pytest.mark.asyncio
async def test_validate_failure(tmp_path: Path) -> None:
    handler = PheromoneHandler(str(tmp_path / "pheromone.json"))
    bad = {"signals": [{}]}
    with pytest.raises(PheromoneHandlerError):
        await handler.write_safe(bad)
