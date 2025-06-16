import asyncio
import time
from typing import List, Dict

import pytest

from src.signal_optimizer import consolidate_duplicates, build_signal_index


def generate_signals(num: int) -> List[Dict[str, int]]:
    return [
        {
            "signalType": "a",
            "category": "need",
            "target": f"t{i%10}",
            "context": {"id": str(i % 5)},
            "strength": i % 10,
            "message": str(i),
        }
        for i in range(num)
    ]


@pytest.mark.asyncio
async def test_consolidate_performance() -> None:
    data1 = generate_signals(1000)
    start = time.perf_counter()
    consolidate_duplicates(data1)
    t1 = time.perf_counter() - start

    data2 = generate_signals(2000)
    start = time.perf_counter()
    consolidate_duplicates(data2)
    t2 = time.perf_counter() - start

    assert t2 / t1 < 3


@pytest.mark.asyncio
async def test_build_index() -> None:
    signals = generate_signals(100)
    index = build_signal_index(signals)
    assert "need" in index
    assert list(index["need"].keys())
