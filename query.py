"""Running queries against the flight database."""
import math
import re
from datetime import datetime
_RECORDED_KEYS = {
    "flight_id",
    "origin",
    "destination",
    "departure_datetime",
    "arrival_datetime",
    "price",
}
_ALLOWED_KEYS = _RECORDED_KEYS | {"min_price", "sort_by", "order", "limit"}
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
def _is_valid_query(query: object) -> bool:
    if not isinstance(query, dict) or any(key not in _ALLOWED_KEYS for key in query):
        return False

    for key in ("flight_id", "origin", "destination"):
        if key in query and not isinstance(query[key], str):
            return False
    for key in ("departure_datetime", "arrival_datetime"):
        if key in query and not _valid_datetime(query[key]):
            return False
    for key in ("price", "min_price"):
        if key in query and not _valid_number(query[key]):
            return False
    if "sort_by" in query:
        sort_by = query["sort_by"]
        if not isinstance(sort_by, str) or sort_by not in _RECORDED_KEYS:
            return False
    if "order" in query:
        if "sort_by" not in query or query["order"] not in ("asc", "desc"):
            return False
    if "limit" in query:
        limit = query["limit"]
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
            return False
    return True

def run_query(db: list[dict], query: dict) -> dict:
    """Return one response entry for a valid or invalid query."""
    if not _is_valid_query(query):
        return {"query": query, "error": "INVALID_QUERY", "matches": []}

    matches = []
    for flight in db:
        if any(
            flight[key] != query[key]
            for key in ("flight_id", "origin", "destination")
            if key in query
        ):
            continue
        if "departure_datetime" in query and flight["departure_datetime"] < query["departure_datetime"]:
            continue
        if "arrival_datetime" in query and flight["arrival_datetime"] > query["arrival_datetime"]:
            continue
        if "price" in query and flight["price"] > query["price"]:
            continue
        if "min_price" in query and flight["price"] < query["min_price"]:
            continue
        matches.append(flight)

    if "sort_by" in query:
        matches.sort(
            key=lambda flight: flight[query["sort_by"]],
            reverse=query.get("order", "asc") == "desc",
        )
    if "limit" in query:
        matches = matches[: query["limit"]]
    return {"query": query, "matches": matches}



def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
    """Accept one query object or a list of query objects."""
    query_list = queries if isinstance(queries, list) else [queries]
    return [run_query(db, query) for query in query_list]

