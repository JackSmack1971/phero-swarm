import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Set

ALLOWED_GROUPS: Set[str] = {"read", "edit", "command", "mcp"}
DISALLOWED_TOOLS: Set[str] = {"rm", "sudo"}

class ValidationError(Exception):
    """Raised when the ROOMODES file is insecure or malformed."""

async def load_json(path: str) -> Dict[str, Any]:
    try:
        text = await asyncio.to_thread(Path(path).read_text)
        return json.loads(text)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"Unable to load {path}") from exc


def _check_regex(slug: str, regexes: List[str], errors: List[str]) -> None:
    if not regexes:
        errors.append(f"{slug}: missing fileRegex")
    for rx in regexes or []:
        if ".." in rx or rx.startswith("/"):
            errors.append(f"{slug}: invalid fileRegex '{rx}'")


def _check_groups(slug: str, groups: List[str], tools: List[str], errors: List[str]) -> None:
    if not set(groups).issubset(ALLOWED_GROUPS):
        errors.append(f"{slug}: invalid groups {groups}")
    if "command" in groups:
        if not tools:
            errors.append(f"{slug}: command group requires allowedTools")
        for tool in tools:
            if tool in DISALLOWED_TOOLS:
                errors.append(f"{slug}: disallowed tool {tool}")


async def validate_roomodes(path: str = ".ROOMODES") -> bool:
    data = await load_json(path)
    errors: List[str] = []
    for mode in data.get("customModes", []):
        slug = mode.get("slug", "unknown")
        file_regex = mode.get("fileRegex", [])
        tools = mode.get("allowedTools", [])
        groups = mode.get("groups", [])
        _check_regex(slug, file_regex, errors)
        _check_groups(slug, groups, tools, errors)
    if errors:
        for err in errors:
            print(err)
        return False
    return True


async def main() -> None:
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else ".ROOMODES"
    if not await validate_roomodes(path):
        raise SystemExit(1)
    print("Validation successful")


if __name__ == "__main__":
    asyncio.run(main())

