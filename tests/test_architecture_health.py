import json
from pathlib import Path
import sys
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.architecture_health import (
    find_todos,
    parse_adrs,
    update_architecture_health,
)


@pytest.mark.asyncio
async def test_find_todos(tmp_path):
    file = tmp_path / "a.py"
    file.write_text("# TODO fix\nprint('x')\n")
    count = await find_todos(str(tmp_path))
    assert count == 1


@pytest.mark.asyncio
async def test_parse_adrs(tmp_path):
    adr = tmp_path / "0001.md"
    adr.write_text("Status: Accepted")
    stats = await parse_adrs(str(tmp_path))
    assert stats == {"accepted": 1, "total": 1}


@pytest.mark.asyncio
async def test_update_architecture_health(tmp_path):
    pher = tmp_path / "p.json"
    pher.write_text(json.dumps({"signals": []}))
    adr_dir = tmp_path / "adrs"
    adr_dir.mkdir()
    (adr_dir / "0001.md").write_text("Status: Accepted")
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "a.py").write_text("# TODO\n")
    await update_architecture_health(str(pher), str(src_dir), str(adr_dir))
    data = json.loads(pher.read_text())
    assert data["signals"][0]["signalType"] == "architecture_health"
