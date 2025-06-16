import json
from pathlib import Path
import sys
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.signal_analytics import (
    load_analytics,
    save_analytics,
    update_metrics,
    detect_pollution,
    AnalyticsError,
)


@pytest.mark.asyncio
async def test_load_and_save(tmp_path):
    file = tmp_path / "a.json"
    data = {"x": 1}
    await save_analytics(str(file), data)
    loaded = await load_analytics(str(file))
    assert loaded["x"] == 1


@pytest.mark.asyncio
async def test_load_bad(tmp_path):
    file = tmp_path / "bad.json"
    file.write_text("{")
    with pytest.raises(AnalyticsError):
        await load_analytics(str(file))


def test_update_and_pollution():
    metrics = {}
    signals = [{"signalType": "a"} for _ in range(6)]
    metrics = update_metrics(metrics, signals)
    polluted = detect_pollution(metrics, threshold=5)
    assert "a" in polluted
