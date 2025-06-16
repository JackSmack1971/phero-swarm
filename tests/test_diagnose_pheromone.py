from pathlib import Path
import json
import sys
import pytest

from diagnose_pheromone import diagnose, DiagnosticError, main


@pytest.mark.asyncio
async def test_diagnose_success(tmp_path: Path) -> None:
    p = tmp_path / "pheromone.json"
    p.write_text(json.dumps({"signals": []}))
    await diagnose(p)


@pytest.mark.asyncio
async def test_diagnose_invalid_json(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text("{bad}")
    with pytest.raises(DiagnosticError):
        await diagnose(p)


@pytest.mark.asyncio
async def test_diagnose_missing_file(tmp_path: Path) -> None:
    with pytest.raises(DiagnosticError):
        await diagnose(tmp_path / "no.json")


@pytest.mark.asyncio
async def test_diagnose_bad_encoding(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_bytes(b"\xff\ff")
    with pytest.raises(DiagnosticError):
        await diagnose(p)


@pytest.mark.asyncio
async def test_diagnose_unreadable(tmp_path: Path) -> None:
    d = tmp_path / "dir"
    d.mkdir()
    with pytest.raises(DiagnosticError):
        await diagnose(d)


def test_main(tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch) -> None:
    p = tmp_path / "pheromone.json"
    p.write_text(json.dumps({"signals": []}))
    monkeypatch.setattr(sys, "argv", ["prog", str(p)])
    main()
    captured = capsys.readouterr()
    assert "JSON structure valid" in captured.out


def test_main_error(tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch) -> None:
    missing = tmp_path / "missing.json"
    monkeypatch.setattr(sys, "argv", ["prog", str(missing)])
    main()
    captured = capsys.readouterr()
    assert "does not exist" in captured.out
