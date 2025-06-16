import asyncio
import json
import re
from pathlib import Path
from typing import Any, Dict, List
from .signal_optimizer import consolidate_duplicates, normalize_strengths

from .context_manager import compress_context, validate_files, extract_decisions


class PheromoneError(Exception):
    """Custom exception for pheromone update issues."""


async def load_pheromone(path: str) -> Dict[str, Any]:
    """Load pheromone JSON asynchronously."""
    try:
        text = await asyncio.to_thread(Path(path).read_text)
        return json.loads(text)
    except (OSError, json.JSONDecodeError) as exc:
        raise PheromoneError("Invalid pheromone file") from exc


async def save_pheromone(path: str, data: Dict[str, Any]) -> None:
    """Persist pheromone JSON asynchronously."""
    try:
        await asyncio.to_thread(Path(path).write_text, json.dumps(data, indent=2))
    except OSError as exc:
        raise PheromoneError("Unable to save pheromone") from exc


def calculate_strength(category: str, complexity: int, urgency: float) -> float:
    """Calculate signal strength from complexity and urgency."""
    base = {
        "compass": 10.0,
        "state": 7.5,
        "need": 7.0,
        "block": 8.5,
        "coordinate": 6.5,
    }.get(category, 1.0)
    return min(10.0, base + complexity * 0.1 + urgency)


def sanitize_context(context: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize context fields and compress."""
    files = context.get("modified_files", [])
    context["modified_files"] = validate_files(files)
    summary = context.get("architecture_summary", "")
    if summary:
        context["architecture_decisions"] = extract_decisions(summary)
        pattern_rx = re.compile(r"([A-Z][a-zA-Z]+ Pattern)")
        context["patterns_used"] = pattern_rx.findall(summary)
    return compress_context(context)


async def update_pheromone(path: str, signal: Dict[str, Any]) -> None:
    """Update pheromone file with a sanitized signal."""
    pheromone = await load_pheromone(path)
    context = sanitize_context(signal.get("context", {}))
    signal["context"] = context
    pheromone.setdefault("signals", []).append(signal)
    pheromone["signals"] = consolidate_signals(pheromone["signals"])
    pheromone["signals"] = consolidate_duplicates(pheromone["signals"])
    pheromone["signals"] = normalize_strengths(pheromone["signals"])
    await save_pheromone(path, pheromone)


def consolidate_signals(signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Merge consecutive signals referencing the same files."""
    consolidated: List[Dict[str, Any]] = []
    for sig in signals:
        if consolidated and sig.get("context", {}).get(
            "modified_files"
        ) == consolidated[-1].get("context", {}).get("modified_files"):
            consolidated[-1]["message"] += f"; {sig['message']}"
        else:
            consolidated.append(sig)
    return consolidated
