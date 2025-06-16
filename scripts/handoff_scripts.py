import asyncio
from typing import Any

from src.pheromone_handler import PheromoneHandler
from src.handoff_templates import task_completion, work_request


async def _execute_signals(path: str, *signals: Any) -> None:
    handler = PheromoneHandler(path)
    for sig in signals:
        await handler.add_signal(sig)


async def blueprint_complete_handoff(path: str = ".pheromone") -> None:
    """Route blueprint completion to the architect."""
    done = task_completion("Blueprint finalized")
    request = work_request(
        "architecture design required",
        "architect-highlevel-module",
        strength=7.0,
    )
    await _execute_signals(path, done, request)


async def architecture_complete_handoff(path: str = ".pheromone") -> None:
    """Route architecture completion to the coder."""
    done = task_completion("Architecture documented")
    request = work_request(
        "coding implementation needed",
        "coder-test-driven",
        strength=7.1,
    )
    await _execute_signals(path, done, request)


async def code_complete_handoff(path: str = ".pheromone") -> None:
    """Route code completion to the tester."""
    done = task_completion("Code implemented")
    request = work_request("run tests", "tester-tdd-master", strength=7.2)
    await _execute_signals(path, done, request)


async def test_complete_handoff(path: str = ".pheromone") -> None:
    """Notify orchestrator that testing finished."""
    done = task_completion("Testing complete")
    request = work_request(
        "review results",
        "orchestrator-pheromone-scribe",
        strength=7.3,
    )
    await _execute_signals(path, done, request)


async def debug_complete_handoff(target: str, path: str = ".pheromone") -> None:
    """Return debugging results to the requested agent."""
    done = task_completion("Bug resolved")
    request = work_request("retest fix", target, strength=7.4)
    await _execute_signals(path, done, request)


async def main() -> None:
    await blueprint_complete_handoff()


if __name__ == "__main__":
    asyncio.run(main())
