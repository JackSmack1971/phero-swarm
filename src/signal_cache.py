from __future__ import annotations
import asyncio
import os
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Awaitable


class SignalCacheError(Exception):
    """Raised when cache operations fail."""


@dataclass
class _Entry:
    data: List[Dict[str, Any]]
    timestamp: float


class SignalCache:
    """In-memory TTL cache with write-through persistence."""

    def __init__(self, ttl: int | None = None, persist: Callable[[str, List[Dict[str, Any]]], Awaitable[None]] | None = None) -> None:
        self.ttl = ttl or int(os.getenv("SIGNAL_CACHE_TTL", "60"))
        self.persist = persist or (lambda _k, _v: asyncio.sleep(0))
        self._cache: Dict[str, _Entry] = {}
        self._metrics: Dict[str, int] = {"hits": 0, "misses": 0, "writes": 0}

    async def get(self, key: str) -> List[Dict[str, Any]]:
        entry = self._cache.get(key)
        now = time.time()
        if entry and now - entry.timestamp < self.ttl:
            self._metrics["hits"] += 1
            return entry.data
        if entry:
            self._cache.pop(key, None)
        self._metrics["misses"] += 1
        raise SignalCacheError("Cache miss")

    async def set(self, key: str, value: List[Dict[str, Any]]) -> None:
        self._cache[key] = _Entry(value, time.time())
        self._metrics["writes"] += 1
        try:
            await self.persist(key, value)
        except Exception as exc:  # noqa: BLE001
            raise SignalCacheError("Persist failed") from exc

    def invalidate(self, key: str) -> None:
        self._cache.pop(key, None)

    def metrics(self) -> Dict[str, int]:
        return dict(self._metrics)
