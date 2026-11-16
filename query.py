"""Running queries against the flight database."""
import math
import re
from datetime import datetime

_ALLOWED_KEYS = _RECORD_KEYS | {"min_price", "sort_by", "order", "limit"}
_DATETIME = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}\Z", re.ASCII)

def _valid_datetime(value: str) -> bool:
    if not isinstance(value, str) or not _DATETIME.fullmatch(value):
        return False
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d %H:%M")
    except ValueError:
        return False
    # strptime accepts some non-zero-padded fields on some Python versions.
    return parsed.strftime("%Y-%m-%d %H:%M") == value
def _valid_number(value: object) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return isinstance(value, int) or math.isfinite(value)

def run_query(db: list[dict], query: dict) -> dict:
    """Return one response entry for one query object.

    Valid query:   {"query": query, "matches": [...]}
    Invalid query: {"query": query, "error": "INVALID_QUERY", "matches": []}
    """
    raise NotImplementedError


def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
    """Accept one query object or a list of them; always return a list."""
    raise NotImplementedError
