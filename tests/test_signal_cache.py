import asyncio
import time
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.signal_cache import SignalCache, SignalCacheError


@pytest.mark.asyncio
async def test_cache_set_and_get() -> None:
    calls = []

    async def persist(key, value):  # noqa: D401
        calls.append((key, value))

    cache = SignalCache(ttl=1, persist=persist)
    await cache.set("k", ["v"])
    result = await cache.get("k")
    assert result == ["v"]
    assert calls

    await asyncio.sleep(1.1)
    with pytest.raises(SignalCacheError):
        await cache.get("k")


@pytest.mark.asyncio
async def test_cache_metrics() -> None:
    cache = SignalCache(ttl=10)
    with pytest.raises(SignalCacheError):
        await cache.get("x")
    await cache.set("x", ["a"])
    await cache.get("x")
    metrics = cache.metrics()
    assert metrics["hits"] == 1
    assert metrics["misses"] == 1
    assert metrics["writes"] == 1


@pytest.mark.asyncio
async def test_cache_invalidate() -> None:
    cache = SignalCache(ttl=10)
    await cache.set("y", ["b"])
    cache.invalidate("y")
    with pytest.raises(SignalCacheError):
        await cache.get("y")
