import asyncio
import re
from pathlib import Path
from typing import Dict

from src.pheromone_helpers import (
    update_pheromone,
    calculate_strength,
    PheromoneError,
)


class HealthError(Exception):
    """Raised when architecture health computation fails."""


async def _safe_read(path: Path) -> str:
    try:
        return await asyncio.to_thread(path.read_text)
    except OSError as exc:
        raise HealthError(f"Unable to read {path}") from exc


async def find_todos(directory: str) -> int:
    """Count TODO markers in a directory."""
    total = 0
    for file in Path(directory).rglob("*.py"):
        text = await _safe_read(file)
        total += len(re.findall(r"TODO", text))
    return total


async def parse_adrs(directory: str) -> Dict[str, int]:
    """Return ADR statistics."""
    accepted = 0
    total = 0
    for file in Path(directory).glob("*.md"):
        text = await _safe_read(file)
        if "Status" in text:
            total += 1
            if re.search(r"Status:\s*Accepted", text):
                accepted += 1
    return {"accepted": accepted, "total": total}


async def update_architecture_health(
    pheromone_path: str = ".pheromone",
    src_dir: str = "src",
    adr_dir: str = "docs/ADRs",
) -> None:
    """Compute health metrics and update pheromone."""
    try:
        debt = await find_todos(src_dir)
        patterns = await parse_adrs(adr_dir)
        msg = f"debt:{debt} patterns:{patterns['accepted']}/{patterns['total']}"
        signal = {
            "signalType": "architecture_health",
            "category": "state",
            "strength": calculate_strength("state", patterns["total"], 0),
            "message": msg,
            "context": {
                "technical_debt": debt,
                "pattern_success": patterns,
                "modified_files": [],
                "complexity_score": patterns["total"],
            },
        }
        await update_pheromone(pheromone_path, signal)
    except PheromoneError as exc:
        raise HealthError("Failed to update pheromone") from exc


async def main() -> None:
    await update_architecture_health()


if __name__ == "__main__":
    asyncio.run(main())
