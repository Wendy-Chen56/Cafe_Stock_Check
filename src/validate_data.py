"""Check that inventory data is complete and sensible before we use it.

Two kinds of problems are handled differently:
  * Problems with the whole file (wrong columns, no valid rows) stop the program
    by raising DataError.
  * Problems with a single row (bad number, blank name, duplicate id) only skip
    that row. They are collected in a list so the user can fix their spreadsheet.
"""
import math

REQUIRED_COLUMNS = [
    "item_id",
    "item_name",
    "category",
    "unit",
    "quantity_on_hand",
    "daily_use",
    "reorder_level",
]
NUMBER_COLUMNS = ["quantity_on_hand", "daily_use", "reorder_level"]


class DataError(Exception):
    """A problem with the input that the user needs to fix before we can continue."""


def check_columns(fieldnames):
    """Stop with a clear message if any required column is missing."""
    if any(not name for name in fieldnames):
        raise DataError('A column header is blank. Give each column a name.')
    if len(fieldnames) != len(set(fieldnames)):
        raise DataError('Column headers must be unique after trimming spaces and ignoring case.')
    missing = [name for name in REQUIRED_COLUMNS if name not in fieldnames]
    if missing:
        raise DataError(
            "Missing required column(s): " + ", ".join(missing)
            + ".\nExpected columns: " + ", ".join(REQUIRED_COLUMNS)
        )


def parse_number(text):
    """Turn text such as '4' or '0.5' into a number that is zero or more.

    Raises ValueError with a short reason if the text is not usable.
    """
    text = (text or "").strip()
    if text == "":
        raise ValueError("is blank")
    try:
        value = float(text)
    except ValueError:
        raise ValueError("'" + text + "' is not a number")
    if not math.isfinite(value):
        raise ValueError("'" + text + "' is not a usable number")
    if value < 0:
        raise ValueError("is negative (" + text + ")")
    return value


def validate_rows(rows):
    """Check each row. Return (valid_items, problems).

    valid_items - list of dictionaries with numbers converted to floats
    problems    - list of readable messages, one per skipped row
    """
    valid_items = []
    problems = []
    first_line_of_id = {}  # item_id -> line number where we first saw it

    # Line 1 of the file is the header, so the first data row is line 2.
    for line_number, row in enumerate(rows, start=2):
        line_number = row.get('__line_number__', line_number)
        reasons = []
        if None in row or any(value is None for value in row.values()):
            missing = [name for name, value in row.items() if name is not None and value is None]
            detail = ' Missing values: ' + ', '.join(missing) + '.' if missing else ''
            problems.append('Line ' + str(line_number) + ': the number of values does not match the header.' + detail)
            continue

        item_id = (row.get("item_id") or "").strip()
        item_name = (row.get("item_name") or "").strip()
        category = (row.get("category") or "").strip()
        unit = (row.get("unit") or "").strip()

        if item_id == "":
            reasons.append("item_id is blank")
        elif item_id in first_line_of_id:
            reasons.append(
                "duplicate item_id '" + item_id + "' (first used on line "
                + str(first_line_of_id[item_id]) + ")"
            )
        if item_name == "":
            reasons.append("item_name is blank")

        numbers = {}
        for column in NUMBER_COLUMNS:
            try:
                numbers[column] = parse_number(row.get(column))
            except ValueError as error:
                reasons.append(column + " " + str(error))

        if reasons:
            problems.append("Line " + str(line_number) + ": " + "; ".join(reasons))
            continue  # skip this row, keep checking the others

        first_line_of_id[item_id] = line_number
        valid_items.append({
            "item_id": item_id,
            "item_name": item_name,
            "category": category if category else "Uncategorized",
            "unit": unit,
            "quantity_on_hand": numbers["quantity_on_hand"],
            "daily_use": numbers["daily_use"],
            "reorder_level": numbers["reorder_level"],
        })

    return valid_items, problems
