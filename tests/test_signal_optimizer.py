import json
from pathlib import Path
import sys
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.signal_optimizer import (
    consolidate_duplicates,
    normalize_strengths,
    adaptive_evaporation,
)
from src.pheromone_helpers import load_pheromone, save_pheromone


def test_consolidate_duplicates():
    signals = [
        {
            "signalType": "a",
            "category": "need",
            "target": "x",
            "context": {"id": "1"},
            "strength": 5,
            "message": "m1",
        },
        {
            "signalType": "a",
            "category": "need",
            "target": "x",
            "context": {"id": "1"},
            "strength": 6,
            "message": "m2",
        },
    ]
    result = consolidate_duplicates(signals)
    assert len(result) == 1
    assert "m2" in result[0]["message"]
    assert result[0]["strength"] == 6


def test_normalize_strengths():
    signals = [{"strength": 5}, {"strength": 20}]
    out = normalize_strengths(signals)
    assert out[1]["strength"] == 10


@pytest.mark.asyncio
async def test_adaptive_evaporation(tmp_path):
    file = tmp_path / "p.json"
    file.write_text(json.dumps({"signals": [{"category": "need", "strength": 10, "context": {}}]}))
    cfg = {
        "coreConfig": {"evaporationRates": {"need": 0.1}, "signalPruneThreshold": 0.1},
        "adaptiveEvaporation": {"base": 0.1, "urgencyMultiplier": 1},
    }
    await adaptive_evaporation(str(file), cfg, load_pheromone, save_pheromone)
    data = await load_pheromone(str(file))
    assert data["signals"][0]["strength"] < 10
