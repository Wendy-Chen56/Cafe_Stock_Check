"""Cafe Stock Check - command-line entry point.

Example:
    python src/main.py data/sample_inventory.csv
    python src/main.py data/sample_inventory.csv --all --sort name
    python src/main.py data/sample_inventory.csv --export reorder_list.csv
"""
import argparse
import math
import os
import sys

from load_data import read_csv_rows
from reports import (SORT_CHOICES, analyze_items, filter_items, format_report,
                     sort_items, write_reorder_csv)
from validate_data import DataError, check_columns, validate_rows


def build_parser():
    parser = argparse.ArgumentParser(
        description="Find café supplies that need reordering from an inventory CSV file.")
    parser.add_argument("csv_file", help="path to the inventory CSV file")
    parser.add_argument("--warn-days", type=float, default=3,
                        help="flag items that will run out within this many days (default 3)")
    parser.add_argument("--target-days", type=float, default=7,
                        help="suggested orders restock up to this many days of use (default 7)")
    parser.add_argument("--sort", choices=SORT_CHOICES, default="urgency",
                        help="sort order (default urgency)")
    parser.add_argument("--category", help="only show one category, e.g. Dairy")
    parser.add_argument("--all", action="store_true",
                        help="show every item, not just those needing attention")
    parser.add_argument("--export", metavar="FILE",
                        help="save the reorder list (items needing attention) to a CSV file")
    return parser


def main(argv=None):
    """Run the program. Returns 0 on success and 1 if the input has a problem."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if not math.isfinite(args.warn_days) or args.warn_days < 0:
        parser.error("--warn-days must be a finite number of zero or more")
    if not math.isfinite(args.target_days) or args.target_days <= 0:
        parser.error("--target-days must be a finite number greater than zero")

    try:
        column_names, rows = read_csv_rows(args.csv_file)
        check_columns(column_names)
        items, problems = validate_rows(rows)

        if problems:
            print("Warning: " + str(len(problems)) + " row(s) were skipped because of problems:")
            for message in problems:
                print("  - " + message)
            print("")
        if not items:
            raise DataError("There are no valid rows to analyze. Fix the problems above "
                            "and try again.")

        results = analyze_items(items, args.warn_days, args.target_days)
        results = filter_items(results, category=args.category)
        if args.category and not results:
            raise DataError("No items found in category '" + args.category + "'.")
        results = sort_items(results, args.sort)

        shown = filter_items(results, attention_only=not args.all)
        print(format_report(results, shown, os.path.basename(args.csv_file),
                            args.warn_days, args.target_days, args.all))

        if args.export:
            to_reorder = filter_items(results, attention_only=True)
            write_reorder_csv(to_reorder, args.export)
            print("")
            print("Saved reorder list (" + str(len(to_reorder)) + " item(s)) to " + args.export)
    except DataError as error:
        print("Error: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
