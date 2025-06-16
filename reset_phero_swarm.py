import asyncio
import os
import shutil
import time
from pathlib import Path
from typing import Optional

from src.pheromone_handler import PheromoneHandler
from validate_system_health import (
    check_config_files,
    check_roomodes,
    test_pheromone_ops,
    verify_routing,
    SystemHealthError,
)


class ResetError(Exception):
    """Raised when system reset fails."""


async def backup_state(path: Path) -> Optional[Path]:
    if not path.exists():
        return None
    dest = path.with_suffix(f".bak.{int(time.time())}")
    await asyncio.to_thread(shutil.copy2, path, dest)
    return dest


async def reset_pheromone(path: Path) -> None:
    handler = PheromoneHandler(str(path))
    data = {"signals": [], "metadata": {"created": int(time.time())}}
    await handler.write_safe(data)


async def main() -> None:
    file_path = Path(os.getenv("PHEROMONE_FILE", ".pheromone"))
    try:
        await backup_state(file_path)
        await reset_pheromone(file_path)
        await check_config_files()
        await check_roomodes()
        await test_pheromone_ops()
        await verify_routing()
        print("System reset complete and healthy")
    except (SystemHealthError, Exception) as exc:
        raise ResetError("Reset failed") from exc


if __name__ == "__main__":
    asyncio.run(main())
