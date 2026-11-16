"""Flight Schedule Parser and Query Tool - command-line entry point.

Run from the project folder, for example:
    python flight_parser.py -i data/db.csv -a data/airports.txt
"""
#imports
import argparse
import json
import logging
import os
import sys
from datetime import datetime

from csv_loader import parse_files
from query import run_queries
from validator import load_airports

# TODO: fill in your details: plain ASCII, no spaces or underscores.
STUDENT_ID = "251ADB024"
FIRST_NAME = "Sharan"
LAST_NAME = "Kunnel Suresh"


def main(argv: list[str] | None = None) -> int:
    """Run the whole program and return the exit code (0, 1 or 2).

    argv is the argument list without the program name.
    None means use sys.argv[1:] (argparse does this for you).
    Do not call sys.exit() inside main(); return the code instead.
    """
    parser = argparse.ArgumentParser(description="Validate, store, and query flight schedules.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("-i", metavar="FILE", help="parse one CSV file")
    source.add_argument("-d", metavar="FOLDER", help="parse CSV files in a folder")
    source.add_argument("-j", metavar="FILE", help="load a JSON flight database")
    parser.add_argument("-a", metavar="FILE", help="airport list (required with -i or -d)")
    parser.add_argument("-o", metavar="FILE", help="database output path (default: db.json)")
    parser.add_argument("-q", metavar="FILE", help="JSON file containing queries")
    parser.add_argument("-r", metavar="FOLDER", help="query response folder (default: current folder)")
    args = parser.parse_args(argv)

    if (args.i or args.d) and not args.a:
        parser.error("-a is required with -i or -d")
    if args.j and args.o:
        parser.error("-o cannot be used with -j")
    output_path = args.o or "db.json"
    logger = logging.getLogger("flight_parser")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = None
    try:
        if args.j:
            with open(args.j, "r", encoding="utf-8") as database_file:
                db = json.load(database_file)
            if not isinstance(db, list) or any(not isinstance(record, dict) for record in db):
                raise ValueError("JSON database must be an array of objects")
        else:
            log_path = os.path.join(os.path.dirname(os.path.abspath(output_path)), "errors.log")
            handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
            handler.setFormatter(logging.Formatter(
                "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            ))
            logger.addHandler(handler)

            if args.i:
                csv_paths = [args.i]
            else:
                if not os.path.isdir(args.d):
                    raise FileNotFoundError(f"folder does not exist: {args.d}")
                csv_paths = [
                    os.path.join(args.d, name)
                    for name in sorted(os.listdir(args.d))
                    if name.endswith(".csv") and os.path.isfile(os.path.join(args.d, name))
                ]
                if not csv_paths:
                    raise FileNotFoundError(f"no .csv files found in folder: {args.d}")
            airports = load_airports(args.a)
            db, errors = parse_files(csv_paths, airports)
            for error in errors:
                logger.warning("%s", error)
            with open(output_path, "w", encoding="utf-8") as database_file:
                json.dump(db, database_file, ensure_ascii=False, indent=2)
        if args.q:
            with open(args.q, "r", encoding="utf-8") as query_file:
                queries = json.load(query_file)
            if not isinstance(queries, (dict, list)):
                raise ValueError("query JSON must be an object or an array")
            responses = run_queries(db, queries)
            response_folder = args.r or "."
            response_name = (
                f"response_{STUDENT_ID}_{FIRST_NAME}_{LAST_NAME}_"
                f"{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            )
            response_path = os.path.join(response_folder, response_name)
            with open(response_path, "w", encoding="utf-8") as response_file:
                json.dump(responses, response_file, ensure_ascii=False, indent=2)
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    finally:
        if handler is not None:
            logger.removeHandler(handler)
            handler.close()
if __name__ == "__main__":
    sys.exit(main())
