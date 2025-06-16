import pytest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.pheromone_helpers import sanitize_context, calculate_strength, consolidate_signals


@pytest.mark.asyncio
async def test_calculate_strength():
    strength = calculate_strength("need", 5, 0.5)
    assert strength > 7


def test_sanitize_context(tmp_path):
    ctx = {"modified_files": ["src/main.py", "bad path"], "handoff_instructions": "continue"}
    result = sanitize_context(ctx)
    assert result["modified_files"] == ["@src/main.py"]


@pytest.mark.asyncio
async def test_consolidate_signals():
    signals = [
        {"message": "a", "context": {"modified_files": ["@f"]}},
        {"message": "b", "context": {"modified_files": ["@f"]}},
    ]
    consolidated = consolidate_signals(signals)
    assert len(consolidated) == 1
    assert "b" in consolidated[0]["message"]
