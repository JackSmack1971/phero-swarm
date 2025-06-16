import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import pytest

from scripts.handoff_scripts import (
    blueprint_complete_handoff,
    architecture_complete_handoff,
    code_complete_handoff,
    test_complete_handoff,
    debug_complete_handoff,
)
from src.pheromone_handler import PheromoneHandler
from src.traffic_controller import determine_route


@pytest.mark.asyncio
async def test_handoff_sequence(tmp_path: Path) -> None:
    pher = tmp_path / "pher.json"
    await blueprint_complete_handoff(str(pher))
    handler = PheromoneHandler(str(pher))
    agent = await determine_route(await handler.read_safe() or {}, handler)
    assert agent == "architect-highlevel-module"
    await architecture_complete_handoff(str(pher))
    agent = await determine_route(await handler.read_safe() or {}, handler)
    assert agent == "coder-test-driven"
    await code_complete_handoff(str(pher))
    agent = await determine_route(await handler.read_safe() or {}, handler)
    assert agent == "tester-tdd-master"
    await test_complete_handoff(str(pher))
    agent = await determine_route(await handler.read_safe() or {}, handler)
    assert agent == "coder-test-driven"
    await debug_complete_handoff("tester-tdd-master", str(pher))
    agent = await determine_route(await handler.read_safe() or {}, handler)
    assert agent == "tester-tdd-master"
