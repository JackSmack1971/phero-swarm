import argparse
import asyncio
import json
from pathlib import Path
from typing import Tuple

import aiofiles


class DiagnosticError(Exception):
    """Raised when pheromone diagnostics fail."""


async def read_pheromone(path: Path) -> Tuple[str, str, int]:
    """Return file text, encoding, and size."""
    try:
        async with aiofiles.open(path, 'rb') as f:
            data = await f.read()
    except OSError as exc:
        raise DiagnosticError(f"Cannot read {path}") from exc
    size = len(data)
    try:
        text = data.decode('utf-8')
        encoding = 'utf-8'
    except UnicodeDecodeError:
        text = data.decode('latin-1', errors='replace')
        encoding = 'unknown'
    return text, encoding, size


async def validate_json(text: str) -> None:
    """Validate JSON and raise DiagnosticError if invalid."""
    try:
        json.loads(text)
    except json.JSONDecodeError as exc:
        msg = f"JSON error line {exc.lineno} col {exc.colno}: {exc.msg}"
        raise DiagnosticError(msg) from exc


async def diagnose(path: Path) -> None:
    """Run diagnostics on the pheromone file."""
    if not path.exists():
        raise DiagnosticError(f"{path} does not exist")
    text, encoding, size = await read_pheromone(path)
    await validate_json(text)
    print(f"File encoding: {encoding}")
    print(f"File size: {size} bytes")
    print("JSON structure valid")


def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnose pheromone file")
    parser.add_argument("path", nargs="?", default=".pheromone")
    args = parser.parse_args()
    try:
        asyncio.run(diagnose(Path(args.path)))
    except DiagnosticError as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
