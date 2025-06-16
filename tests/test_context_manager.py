import pytest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.context_manager import (
    extract_decisions,
    compress_context,
    validate_files,
    verify_progress,
)


def test_extract_decisions():
    summary = """Decision: adopt API\n* Use async functions\nNo action"""
    decisions = extract_decisions(summary)
    assert len(decisions) == 2


def test_compress_context():
    ctx = {"a": "word " * 300, "b": "ok"}
    compressed = compress_context(ctx, max_tokens=50)
    assert "b" not in compressed or compressed.get("b") == "ok"


def test_validate_files():
    files = ["src/app.py", "invalid file", "../bad"]
    valid = validate_files(files)
    assert "@src/app.py" in valid
    assert len(valid) == 1


def test_verify_progress():
    prev = {"a": 1}
    curr = {"a": 2}
    assert verify_progress(prev, curr)
