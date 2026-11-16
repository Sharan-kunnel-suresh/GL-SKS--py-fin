"""Row validation: airport list loading, single-row checks, record building."""

import math
import re
from datetime import datetime

_FLIGHT_ID = re.compile(r"[A-Za-z0-9]{2,8}\Z", re.ASCII)
_AIRPORT = re.compile(r"[A-Z]{3}\Z", re.ASCII)
_DATETIME = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}\Z", re.ASCII)
_DATETIME_FORMAT = "%Y-%m-%d %H:%M"


#extra functions creating to parse datetime and check if it is valid
def _parse_datetime(value: str) -> datetime | None:
    if not _DATETIME.fullmatch(value):
        return None
    try:
        parsed = datetime.strptime(value, _DATETIME_FORMAT)
    except ValueError:
        return None
    # strptime accepts some non-zero-padded fields on some Python versions.
    return parsed if parsed.strftime(_DATETIME_FORMAT) == value else None

def load_airports(path: str) -> set[str]:
    """Read airport codes, ignoring blank and comment lines."""
    airports: set[str] = set()
    with open(path, "r", encoding="utf-8") as airport_file:
        for line in airport_file:
            code = line.strip()
            if code and not code.startswith("#"):
                airports.add(code)
    return airports
    


def validate_row(fields: list[str], airports: set[str]) -> str | None:
    """Check one CSV row (fields as returned by csv.reader, not yet stripped).

    Return None if the row is valid, otherwise the error code of the
    FIRST failing check (checks 1-11 in the specification, in order).
    Does not check for duplicates.
    """
    raise NotImplementedError


def to_record(fields: list[str]) -> dict:
    """Turn a valid row into a flight record dictionary.

    Keys: flight_id, origin, destination, departure_datetime,
    arrival_datetime (stripped strings) and price (float).
    """
    raise NotImplementedError
