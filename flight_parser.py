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
LAST_NAME = "Kunnel_Suresh"


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
if __name__ == "__main__":
    sys.exit(main())
