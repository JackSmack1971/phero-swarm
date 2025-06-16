import asyncio
import json
import os
import shutil
import tempfile
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional, AsyncGenerator
import fcntl


class PheromoneHandlerError(Exception):
    """Custom exception for pheromone handler failures."""


class PheromoneHandler:
    """Safe handler for pheromone file operations."""

    def __init__(self, path: Optional[str] = None) -> None:
        env_path = os.getenv("PHEROMONE_FILE", ".pheromone")
        self.path = Path(path or env_path)
        self.backup_path = self.path.with_name(self.path.name + ".backup")
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @asynccontextmanager
    async def _lock(self) -> AsyncGenerator[None, None]:
        handle = await asyncio.to_thread(open, self.path, "a+")
        try:
            await asyncio.to_thread(fcntl.flock, handle, fcntl.LOCK_EX)
            yield
        finally:
            await asyncio.to_thread(fcntl.flock, handle, fcntl.LOCK_UN)
            handle.close()

    async def _backup(self) -> None:
        if self.path.exists():
            await asyncio.to_thread(shutil.copy2, self.path, self.backup_path)

    async def _restore_backup(self) -> None:
        if self.backup_path.exists():
            await asyncio.to_thread(shutil.copy2, self.backup_path, self.path)

    async def _atomic_write(self, text: str) -> None:
        fd, tmp = tempfile.mkstemp(dir=str(self.path.parent))
        try:
            os.write(fd, text.encode("utf-8"))
            os.fsync(fd)
        finally:
            os.close(fd)
        await asyncio.to_thread(os.replace, tmp, self.path)

    def validate_structure(self, data: Dict[str, Any]) -> None:
        if not isinstance(data, dict) or "signals" not in data:
            raise PheromoneHandlerError("Invalid structure")
        if not isinstance(data["signals"], list):
            raise PheromoneHandlerError("Signals must be a list")
        required = {"id", "signalType", "category", "strength", "message", "timestamp"}
        for sig in data["signals"]:
            if not isinstance(sig, dict) or not required.issubset(sig):
                raise PheromoneHandlerError("Malformed signal")

    async def read_safe(self) -> Optional[Dict[str, Any]]:
        async with self._lock():
            try:
                text = await asyncio.to_thread(self.path.read_text, encoding="utf-8")
            except FileNotFoundError:
                return None
            except OSError as exc:
                raise PheromoneHandlerError("Read error") from exc
        try:
            data = json.loads(text)
            self.validate_structure(data)
            return data
        except (json.JSONDecodeError, PheromoneHandlerError):
            await self._restore_backup()
            try:
                text = await asyncio.to_thread(self.path.read_text, encoding="utf-8")
                data = json.loads(text)
                self.validate_structure(data)
                return data
            except Exception:
                return None

    async def write_safe(self, data: Dict[str, Any]) -> None:
        self.validate_structure(data)
        text = json.dumps(data, ensure_ascii=False, indent=2)
        async with self._lock():
            await self._backup()
            try:
                await self._atomic_write(text)
                await self._backup()
            except Exception as exc:
                await self._restore_backup()
                raise PheromoneHandlerError("Write failed") from exc

    async def add_signal(self, signal: Dict[str, Any]) -> None:
        data = await self.read_safe() or {"signals": []}
        data.setdefault("signals", []).append(signal)
        await self.write_safe(data)

    async def clear_signals_by_category(self, category: str) -> None:
        data = await self.read_safe() or {"signals": []}
        data["signals"] = [s for s in data.get("signals", []) if s.get("category") != category]
        await self.write_safe(data)
