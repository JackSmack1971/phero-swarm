import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List


class AnalyticsError(Exception):
    """Raised when analytics processing fails."""


async def load_analytics(path: str) -> Dict[str, Any]:
    """Load analytics data asynchronously."""
    try:
        text = await asyncio.to_thread(Path(path).read_text)
        return json.loads(text)
    except (OSError, json.JSONDecodeError) as exc:
        raise AnalyticsError("Invalid analytics file") from exc


async def save_analytics(path: str, data: Dict[str, Any]) -> None:
    """Persist analytics data."""
    try:
        await asyncio.to_thread(Path(path).write_text, json.dumps(data, indent=2))
    except OSError as exc:
        raise AnalyticsError("Unable to save analytics") from exc


def update_metrics(metrics: Dict[str, Any], signals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Update success metrics based on signals."""
    for sig in signals:
        stype = sig.get("signalType")
        stats = metrics.setdefault(stype, {"count": 0})
        stats["count"] += 1
    return metrics


def detect_pollution(metrics: Dict[str, Any], threshold: int = 5) -> List[str]:
    """Return signal types exceeding threshold occurrences."""
    return [k for k, v in metrics.items() if v.get("count", 0) > threshold]
