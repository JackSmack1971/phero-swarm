import re
import json
from typing import Any, Dict, List


class ContextError(Exception):
    """Custom exception for context management issues."""


def extract_decisions(summary: str) -> List[str]:
    """Extract decision statements from an agent summary."""
    decisions = []
    for line in summary.splitlines():
        if line.strip().lower().startswith(('decided', 'decision', '*')):
            decisions.append(line.strip())
    return decisions


def compress_context(context: Dict[str, Any], max_tokens: int = 500) -> Dict[str, Any]:
    """Truncate long fields to keep context under token limits."""
    compressed = {}
    token_count = 0
    for key, value in context.items():
        text = json.dumps(value) if not isinstance(value, str) else value
        tokens = len(text.split())
        if token_count + tokens > max_tokens:
            break
        compressed[key] = value
        token_count += tokens
    return compressed


def validate_files(files: List[str]) -> List[str]:
    """Validate and format file references."""
    valid = []
    pattern = re.compile(r'^[\w./-]+$')
    for f in files:
        if pattern.match(f) and ".." not in f and " " not in f:
            valid.append(f"@{f}")
    return valid


def verify_progress(previous: Dict[str, Any], current: Dict[str, Any]) -> bool:
    """Check if progress has been made between contexts."""
    return previous != current

