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
    """Return the first validation error for a CSV row, if any."""
    fields = [field.strip() for field in fields]
    if len(fields) != 6:#checking the field count, if it is not 6 then return the error code
        return "WRONG_FIELD_COUNT"
    if any(not field for field in fields):
        return "MISSING_FIELD"
    flight_id, origin, destination, departure_text, arrival_text, price_text = fields
    if not _FLIGHT_ID.fullmatch(flight_id):
        return "INVALID_FLIGHT_ID"
    if not _AIRPORT.fullmatch(origin) or origin not in airports:
        return "INVALID_ORIGIN"
    if not _AIRPORT.fullmatch(destination) or destination not in airports:
        return "INVALID_DESTINATION"
    if origin == destination:
        return "SAME_ORIGIN_DESTINATION"
    departure = _parse_datetime(departure_text)
    if departure is None:
        return "INVALID_DEPARTURE"
    arrival = _parse_datetime(arrival_text)
    if arrival is None:
        return "INVALID_ARRIVAL"
    if arrival <= departure:
        return "ARRIVAL_NOT_AFTER_DEPARTURE"
    try:
        price = float(price_text)
    except (TypeError, ValueError, OverflowError):
        return "INVALID_PRICE"
    if not math.isfinite(price):
        return "INVALID_PRICE"
    if price <= 0:
        return "NON_POSITIVE_PRICE"
    return None


def to_record(fields: list[str]) -> dict:
    """Convert a valid row into the required flight record."""
    values = [field.strip() for field in fields]
    return {
        "flight_id": values[0],
        "origin": values[1],
        "destination": values[2],
        "departure_datetime": values[3],
        "arrival_datetime": values[4],
        "price": float(values[5]),
    }

