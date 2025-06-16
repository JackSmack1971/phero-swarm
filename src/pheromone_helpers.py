import asyncio
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Iterable

import aiofiles

from .signal_cache import SignalCache, SignalCacheError


class FilePool:
    """Simple async file connection pool."""

    async def read(self, path: str) -> str:
        async with aiofiles.open(path, "r") as handle:
            return await handle.read()

    async def write(self, path: str, text: str) -> None:
        async with aiofiles.open(path, "w") as handle:
            await handle.write(text)


FILE_POOL = FilePool()
from .signal_optimizer import consolidate_duplicates, normalize_strengths

from .context_manager import compress_context, validate_files, extract_decisions


class PheromoneError(Exception):
    """Custom exception for pheromone update issues."""


async def load_pheromone(path: str, cache: SignalCache | None = None) -> Dict[str, Any]:
    """Load pheromone JSON asynchronously with caching."""
    if cache:
        try:
            return await cache.get(path)
        except SignalCacheError:
            pass
    try:
        text = await FILE_POOL.read(path)
        data = json.loads(text)
    except (OSError, json.JSONDecodeError) as exc:
        raise PheromoneError("Invalid pheromone file") from exc
    if cache:
        await cache.set(path, data)
    return data


async def save_pheromone(path: str, data: Dict[str, Any], cache: SignalCache | None = None) -> None:
    """Persist pheromone JSON asynchronously with cache write-through."""
    try:
        await FILE_POOL.write(path, json.dumps(data, indent=2))
    except OSError as exc:
        raise PheromoneError("Unable to save pheromone") from exc
    if cache:
        await cache.set(path, data)


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


async def update_pheromone(path: str, signal: Dict[str, Any], cache: SignalCache | None = None) -> None:
    """Update pheromone file with a sanitized signal."""
    pheromone = await load_pheromone(path, cache)
    context = sanitize_context(signal.get("context", {}))
    signal["context"] = context
    pheromone.setdefault("signals", []).append(signal)
    pheromone["signals"] = consolidate_signals(pheromone["signals"])
    pheromone["signals"] = consolidate_duplicates(pheromone["signals"])
    pheromone["signals"] = normalize_strengths(pheromone["signals"])
    await save_pheromone(path, pheromone, cache)


async def batch_update_pheromone(path: str, signals: Iterable[Dict[str, Any]], cache: SignalCache | None = None) -> None:
    """Apply a list of signals efficiently."""
    pheromone = await load_pheromone(path, cache)
    sanitized = []
    for sig in signals:
        ctx = sanitize_context(sig.get("context", {}))
        sig["context"] = ctx
        sanitized.append(sig)
    pheromone.setdefault("signals", []).extend(sanitized)
    pheromone["signals"] = consolidate_signals(pheromone["signals"])
    pheromone["signals"] = consolidate_duplicates(pheromone["signals"])
    pheromone["signals"] = normalize_strengths(pheromone["signals"])
    await save_pheromone(path, pheromone, cache)


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
