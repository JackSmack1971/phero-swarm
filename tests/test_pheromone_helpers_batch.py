import json
from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.signal_cache import SignalCache
from src.pheromone_helpers import batch_update_pheromone, load_pheromone


@pytest.mark.asyncio
async def test_batch_update(tmp_path: Path) -> None:
    p = tmp_path / "p.json"
    p.write_text(json.dumps({"signals": []}))
    cache = SignalCache(ttl=10)
    signals = [
        {"id": "1", "signalType": "t", "category": "need", "strength": 1, "message": "m", "timestamp": 1},
        {"id": "2", "signalType": "t", "category": "need", "strength": 2, "message": "m", "timestamp": 2},
    ]
    await batch_update_pheromone(str(p), signals, cache)
    data = await load_pheromone(str(p), cache)
    assert len(data["signals"]) == 1
    assert cache.metrics()["writes"] >= 1
