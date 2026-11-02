"""Turn validated inventory items into a reorder report.

Rules (all calculated here in plain Python):
  days_left       = quantity_on_hand / daily_use           (unknown if daily_use is 0)
  REORDER NOW     = quantity_on_hand <= reorder_level
  ORDER SOON      = days_left <= warn_days                 (and not REORDER NOW)
  OK              = everything else
  suggested order = enough to restock up to `target_days` of use, or to twice the
                    reorder level if that is higher; always at least 1 for items
                    that need attention.
"""
import csv
import math
import os

from validate_data import DataError

STATUS_RANK = {"REORDER NOW": 0, "ORDER SOON": 1, "OK": 2}
SORT_CHOICES = ["urgency", "days", "name", "category"]
EXPORT_COLUMNS = [
    "item_id", "item_name", "category", "unit", "quantity_on_hand",
    "daily_use", "days_left", "status", "suggested_order",
]


def analyze_items(items, warn_days=3, target_days=7):
    """Return a new list of items with days_left, status and suggested_order added."""
    results = []
    for item in items:
        quantity = item["quantity_on_hand"]
        daily_use = item["daily_use"]
        reorder_level = item["reorder_level"]

        if daily_use > 0:
            # Rounding avoids tiny floating-point errors such as 3.0000000000000004.
            days_left = round(quantity / daily_use, 6)
        else:
            days_left = None  # a zero usage rate gives no depletion estimate

        if days_left is not None and not math.isfinite(days_left):
            raise DataError('Cannot calculate days left for ' + item['item_name'] + '. Check the size of the input numbers.')

        if quantity <= reorder_level:
            status = "REORDER NOW"
        elif days_left is not None and days_left <= warn_days:
            status = "ORDER SOON"
        else:
            status = "OK"

        if status == "OK":
            suggested_order = 0
        else:
            target_level = max(target_days * daily_use, reorder_level * 2)
            if not math.isfinite(target_level):
                raise DataError('Cannot calculate an order for ' + item['item_name'] + '. Check the usage, reorder level and target days.')
            suggested_order = max(1, math.ceil(round(target_level - quantity, 6)))

        row = dict(item)  # copy so the original item is not changed
        row["days_left"] = days_left
        row["status"] = status
        row["suggested_order"] = suggested_order
        results.append(row)
    return results


# ---- sorting -------------------------------------------------------------

def _days_key(row):
    # Items with unknown days_left (None) go last.
    missing = row["days_left"] is None
    days = 0 if missing else row["days_left"]
    return (missing, days, row["item_name"].lower())


def _urgency_key(row):
    return (STATUS_RANK[row["status"]],) + _days_key(row)


def _name_key(row):
    return row["item_name"].lower()


def _category_key(row):
    return (row["category"].lower(), row["item_name"].lower())


def sort_items(results, sort_by="urgency"):
    """Return the rows sorted by 'urgency' (default), 'days', 'name' or 'category'."""
    keys = {
        "urgency": _urgency_key,
        "days": _days_key,
        "name": _name_key,
        "category": _category_key,
    }
    if sort_by not in keys:
        raise DataError("Unknown sort option '" + str(sort_by) + "'. Choose from: "
                        + ", ".join(SORT_CHOICES))
    return sorted(results, key=keys[sort_by])


# ---- filtering and counting ---------------------------------------------

def filter_items(results, category=None, attention_only=False):
    """Keep rows in one category (any capitalization) and/or only those needing attention."""
    kept = []
    for row in results:
        if category and row["category"].lower() != category.strip().lower():
            continue
        if attention_only and row["status"] == "OK":
            continue
        kept.append(row)
    return kept


def count_by_status(results):
    counts = {"REORDER NOW": 0, "ORDER SOON": 0, "OK": 0}
    for row in results:
        counts[row["status"]] += 1
    return counts


# ---- text report ---------------------------------------------------------

def format_number(value):
    """Show 4.0 as '4' and 0.4 as '0.4'."""
    if float(value).is_integer():
        return str(int(value))
    return str(round(value, 2))


def format_table(rows):
    """Return a fixed-width text table for the rows ('' if there are none)."""
    if not rows:
        return ""
    headers = ["Item", "Category", "On hand", "Use/day", "Days left", "Status", "Suggest order"]
    table = []
    for row in rows:
        days = "-" if row["days_left"] is None else format_number(round(row["days_left"], 1))
        suggest = "-"
        if row["suggested_order"] > 0:
            suggest = str(row["suggested_order"]) + " " + row["unit"]
        table.append([
            row["item_name"],
            row["category"],
            format_number(row["quantity_on_hand"]) + " " + row["unit"],
            format_number(row["daily_use"]),
            days,
            row["status"],
            suggest,
        ])

    widths = [len(h) for h in headers]
    for line in table:
        for i, cell in enumerate(line):
            widths[i] = max(widths[i], len(cell))

    def make_line(cells):
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells)).rstrip()

    lines = [make_line(headers), "  ".join("-" * w for w in widths)]
    for line in table:
        lines.append(make_line(line))
    return "\n".join(lines)


def format_report(all_results, shown_rows, source_name, warn_days, target_days, show_all):
    """Build the full report text."""
    counts = count_by_status(all_results)
    lines = [
        "Cafe Stock Check - report for " + source_name,
        "Rules: ORDER SOON = stock lasts " + format_number(warn_days) + " days or less. "
        "Order target = the higher of " + format_number(target_days) + " days of use or twice the reorder level.",
        "Items checked: " + str(len(all_results))
        + " | REORDER NOW: " + str(counts["REORDER NOW"])
        + " | ORDER SOON: " + str(counts["ORDER SOON"])
        + " | OK: " + str(counts["OK"]),
        "",
    ]
    if shown_rows:
        title = "All items:" if show_all else "Items that need attention:"
        lines.append(title)
        lines.append(format_table(shown_rows))
    else:
        lines.append("No items need attention. Every item is above its reorder level "
                     "and lasts more than " + format_number(warn_days) + " days.")
    return "\n".join(lines)


# ---- export ---------------------------------------------------------------

def write_reorder_csv(rows, path):
    """Save rows to a new CSV file. Raises DataError if the file cannot be written."""
    path = os.fspath(path)
    try:
        with open(path, "x", newline="", encoding="utf-8") as out_file:
            writer = csv.DictWriter(out_file, fieldnames=EXPORT_COLUMNS, extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                out = dict(row)
                out["days_left"] = "" if row["days_left"] is None else format_number(row["days_left"])
                out["quantity_on_hand"] = format_number(row["quantity_on_hand"])
                out["daily_use"] = format_number(row["daily_use"])
                writer.writerow(out)
    except FileExistsError:
        raise DataError("'" + path + "' already exists. Choose a new export filename.")
    except OSError as error:
        raise DataError("Could not save '" + path + "': " + str(error))
