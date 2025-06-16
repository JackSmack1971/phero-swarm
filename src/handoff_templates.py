import time
from typing import Any, Dict

DEFAULT_TARGET = "orchestrator-pheromone-scribe"


def _build(
    signal_type: str, category: str, target: str, message: str, strength: float
) -> Dict[str, Any]:
    """Return a fully structured pheromone signal."""
    return {
        "id": f"{signal_type}-{int(time.time()*1000)}",
        "signalType": signal_type,
        "category": category,
        "strength": strength,
        "target": target,
        "message": message,
        "timestamp": int(time.time()),
    }


def task_completion(
    message: str,
    target: str = DEFAULT_TARGET,
    strength: float = 7.5,
) -> Dict[str, Any]:
    """Template for announcing task completion."""
    return _build("task_completed", "state", target, message, strength)


def work_request(
    message: str,
    target: str,
    strength: float = 7.0,
) -> Dict[str, Any]:
    """Template for requesting work from another agent."""
    return _build("work_request", "need", target, message, strength)


def coordination_signal(
    message: str,
    target: str,
    strength: float = 6.5,
) -> Dict[str, Any]:
    """Template for coordinating complex handoffs."""
    return _build("coordination", "coordinate", target, message, strength)


def error_signal(
    message: str,
    target: str = DEFAULT_TARGET,
    strength: float = 8.5,
) -> Dict[str, Any]:
    """Template for reporting errors or blocks."""
    return _build("error_block", "block", target, message, strength)
