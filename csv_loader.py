
"""Reading CSV files into flight records and error messages."""
import csv
import os

from numpy import record
from validator import to_record, validate_row
def parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]:
    """Process the CSV files in the order given.

    Return (records, errors):
      records - valid flight records, in input order
      errors  - one message per invalid row, in input order, formatted as
                "<file name>:<line number>: <ERROR_CODE> | <free text>"
                (base file name only, no timestamp or level, no newline)

    Also performs the DUPLICATE_FLIGHT check across all the files.
    Does not write any files and does not log anything itself.
    """
    records: list[dict] = []
    errors: list[str] = []
    seen: set[tuple[str, str, str]] = set()  # (flight_number, departure_date, departure_airport)
    for path in paths:
        with open(path, "r", encoding="utf-8-sig", newline="") as csv_file:
            for line_number, line in enumerate(csv_file, start=1):
                line = line.strip()
                if line_number == 1:
                    # Skip header row
                    continue
                if not line or line.lstrip().startswith("#"):
                    continue
                try:
                    fields = next(csv.reader([line], strict=True))
                except (csv.Error, StopIteration):
                    fields = [line.rstrip("\r\n")]
                error = validate_row(fields, airports)
                if error is None:
                    record=to_record(fields)
                    duplicate_key = (record["flight_id"], record["departure_datetime"])
                    if duplicate_key in seen:
                        error = "DUPLICATE_FLIGHT"
                    else:
                        seen.add(duplicate_key)
                        records.append(record)
                if error is not None:
                    free_text=line.rstrip("\r\n")
                    errors.append(f"{os.path.basename(path)}:{line_number}: {error} | {free_text}")
    return records, errors