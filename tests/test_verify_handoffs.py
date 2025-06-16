import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from scripts.verify_handoffs import verify_chain


def test_verify_chain() -> None:
    assert asyncio.run(verify_chain())
