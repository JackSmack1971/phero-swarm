import pytest
import json
import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.architecture_diagrams import (
    load_signals,
    create_signal_flow,
    create_dependency_graph,
    write_diagrams,
    DiagramError,
)


@pytest.mark.asyncio
async def test_load_signals(tmp_path):
    data = {"signals": [{"signalType": "a"}]}
    f = tmp_path / "p.json"
    f.write_text(json.dumps(data))
    signals = await load_signals(str(f))
    assert signals[0]["signalType"] == "a"


@pytest.mark.asyncio
async def test_load_signals_bad(tmp_path):
    f = tmp_path / "bad.json"
    f.write_text("{")
    with pytest.raises(DiagramError):
        await load_signals(str(f))


def test_mermaid_generation():
    signals = [{"signalType": "a", "target": "b", "context": {"modified_files": ["@x"]}}]
    flow = create_signal_flow(signals)
    deps = create_dependency_graph(signals)
    assert "a--> b" in flow
    assert "a--> x" in deps


@pytest.mark.asyncio
async def test_write_diagrams(tmp_path, monkeypatch):
    monkeypatch.setenv("PHEROMONE_FILE", str(tmp_path / "p.json"))
    (tmp_path / "p.json").write_text(json.dumps({"signals": []}))
    paths = await write_diagrams(str(tmp_path / "out"))
    assert Path(paths[0]).exists() and Path(paths[1]).exists()

