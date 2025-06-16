import json
import asyncio
import pytest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.validate_agent_access import validate_roomodes


@pytest.mark.asyncio
async def test_validate_success(tmp_path):
    roomodes = {"customModes": [{"slug": "a", "groups": ["read"], "fileRegex": ["^docs/.*"]}]}
    file = tmp_path / "roomodes.json"
    file.write_text(json.dumps(roomodes))
    assert await validate_roomodes(str(file))


@pytest.mark.asyncio
async def test_validate_fail(tmp_path):
    roomodes = {"customModes": [{"slug": "a", "groups": ["bad"], "fileRegex": ["../secret"]}]}
    file = tmp_path / "roomodes.json"
    file.write_text(json.dumps(roomodes))
    assert not await validate_roomodes(str(file))
