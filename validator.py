"""Row validation: airport list loading, single-row checks, record building."""

import math
import re
from datetime import datetime

_FLIGHT_ID = re.compile(r"[A-Za-z0-9]{2,8}\Z", re.ASCII)
_AIRPORT = re.compile(r"[A-Z]{3}\Z", re.ASCII)
_DATETIME = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}\Z", re.ASCII)
_DATETIME_FORMAT = "%Y-%m-%d %H:%M"

def load_airports(path: str) -> set[str]:
    """Read an airport list file and return the set of codes.

    One code per line. Strip whitespace; skip blank lines and lines
    starting with '#'.
    """
    raise NotImplementedError


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
