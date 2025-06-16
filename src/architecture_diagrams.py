import asyncio
import json
import os
from pathlib import Path
from typing import Any, Dict, List


class DiagramError(Exception):
    """Raised on diagram generation failures."""


PHEROMONE_FILE = os.getenv("PHEROMONE_FILE", ".pheromone")


def _validate_path(path: str) -> None:
    """Ensure the path is safe for file operations."""
    if ".." in path or Path(path).expanduser().as_posix().startswith("~"):
        raise DiagramError("Invalid path")


async def load_signals(path: str = PHEROMONE_FILE) -> List[Dict[str, Any]]:
    """Load signals from a pheromone file."""
    _validate_path(path)
    try:
        text = await asyncio.to_thread(Path(path).read_text)
        data = json.loads(text)
        return data.get("signals", [])
    except (OSError, json.JSONDecodeError) as exc:
        raise DiagramError("Unable to read pheromone") from exc


def _node_id(name: str) -> str:
    return name.replace("@", "").replace("/", "_").replace(".", "_")


def create_signal_flow(signals: List[Dict[str, Any]]) -> str:
    """Return Mermaid graph linking signal types to targets."""
    lines = ["graph TD"]
    for sig in signals:
        src = _node_id(sig.get("signalType", "unknown"))
        tgt = _node_id(sig.get("target", sig.get("category", "unknown")))
        lines.append(f"    {src}--> {tgt}")
    return "\n".join(lines)


def create_dependency_graph(signals: List[Dict[str, Any]]) -> str:
    """Return Mermaid graph linking signals to files."""
    lines = ["graph TD"]
    for sig in signals:
        src = _node_id(sig.get("signalType", "unknown"))
        files = sig.get("context", {}).get("modified_files", [])
        for f in files:
            tgt = _node_id(f)
            lines.append(f"    {src}--> {tgt}")
    return "\n".join(lines)


async def write_diagrams(directory: str = "docs/architecture") -> List[str]:
    """Generate diagrams from the current pheromone file."""
    _validate_path(directory)
    signals = await load_signals()
    Path(directory).mkdir(parents=True, exist_ok=True)
    flow = create_signal_flow(signals)
    deps = create_dependency_graph(signals)
    flow_path = Path(directory) / "signal_flow.mmd"
    dep_path = Path(directory) / "file_dependencies.mmd"
    await asyncio.to_thread(flow_path.write_text, flow)
    await asyncio.to_thread(dep_path.write_text, deps)
    return [str(flow_path), str(dep_path)]


async def main() -> None:
    paths = await write_diagrams()
    for p in paths:
        print(f"Diagram written to {p}")


if __name__ == "__main__":
    asyncio.run(main())
