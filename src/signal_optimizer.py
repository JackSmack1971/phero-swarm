from collections import defaultdict
from typing import Any, Dict, List


class OptimizationError(Exception):
    """Raised when signal optimization fails."""


def cluster_by_context(signals: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group signals by context id or target."""
    clusters: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for sig in signals:
        key = sig.get("context", {}).get("id") or sig.get("target") or "global"
        clusters[key].append(sig)
    return dict(clusters)


def consolidate_duplicates(signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Merge duplicate signals with matching type and context."""
    seen: Dict[tuple, Dict[str, Any]] = {}
    result: List[Dict[str, Any]] = []
    for sig in signals:
        key = (
            sig.get("signalType"),
            sig.get("target"),
            sig.get("category"),
            sig.get("context", {}).get("id"),
        )
        if key in seen:
            exist = seen[key]
            exist["message"] = f"{exist.get('message','')}; {sig.get('message','')}"
            exist["strength"] = max(exist.get("strength", 0), sig.get("strength", 0))
        else:
            seen[key] = sig
            result.append(sig)
    return result


def normalize_strengths(signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Scale signal strengths to the 0-10 range."""
    if not signals:
        return signals
    max_val = max(sig.get("strength", 0) for sig in signals)
    if max_val <= 10:
        return signals
    for sig in signals:
        sig["strength"] = round((sig.get("strength", 0) / max_val) * 10, 2)
    return signals


async def adaptive_evaporation(
    path: str,
    config: Dict[str, Any],
    load_cb,
    save_cb,
) -> None:
    """Decay signal strengths using context-aware rates."""
    data = await load_cb(path)
    rates = config.get("coreConfig", {}).get("evaporationRates", {})
    adaptive = config.get("adaptiveEvaporation", {"base": 0.05, "urgencyMultiplier": 1})
    prun = config.get("coreConfig", {}).get("signalPruneThreshold", 0.1)
    updated: List[Dict[str, Any]] = []
    for sig in data.get("signals", []):
        cat = sig.get("category")
        base = rates.get(cat, adaptive.get("base", 0.05))
        urgency = sig.get("context", {}).get("urgency", 0)
        decay = base * (1 - urgency * adaptive.get("urgencyMultiplier", 1))
        sig["strength"] = max(0.1, round(sig.get("strength", 0) * (1 - decay), 2))
        if sig["strength"] >= prun:
            updated.append(sig)
    data["signals"] = updated
    await save_cb(path, data)

