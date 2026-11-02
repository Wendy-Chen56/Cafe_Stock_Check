# Code Guide

## Running the program

```powershell
python src/main.py data/sample_inventory.csv
```

This command runs `main.py` and tells it which CSV to use. `build_parser()` sets up the options, such as `--category` and `--warn-days`. `main()` reads those options and calls the functions in the other files.

## Reading the CSV

`read_csv_rows()` in `load_data.py` opens the file and reads it with `csv.DictReader`. Each row becomes a dictionary, so the program can look up values by their column names.

For example:

```python
row["item_name"]         # "Whole milk"
row["quantity_on_hand"]  # "18"
```

At this point, `"18"` is still text. It gets converted to a number during validation.

The function also removes spaces around column names, changes them to lowercase, and records the row numbers. If the file cannot be read, it raises a `DataError`. `main()` catches that error and displays the message.

## Checking the data

`check_columns()` checks that the required headers are present and that none are blank or repeated.

`validate_rows()` then checks each row. It looks for missing IDs or names, duplicate IDs, and invalid numbers. `parse_number()` converts numeric text into floats and rejects blank, negative, or nonfinite values.

For example, `"18"` becomes `18.0`, but `"six"` produces an error. The program records the reason, skips that row, and keeps checking the others.

The function returns two lists: the valid items and the error messages. If no valid items remain, the program stops.

## Working out the stock status

`analyze_items()` in `reports.py` takes each valid item and calculates how long its stock may last:

```python
days_left = round(quantity / daily_use, 6)
```

For whole milk, that is 18 ÷ 10 = 1.8 days.

If daily usage is zero, the program uses `None` instead of dividing by zero. That means there is no days-left estimate. The item can still need reordering based on its stock level.

The status is checked in this order:

```python
if quantity <= reorder_level:
    status = "REORDER NOW"
elif days_left is not None and days_left <= warn_days:
    status = "ORDER SOON"
else:
    status = "OK"
```

First, the program compares stock with the reorder level. Only if stock is above that level does it check the remaining days.

With the default three-day warning:

- Whole milk is above its reorder level but has only 1.8 days left, so it is ORDER SOON.
- Oat milk is above its reorder level and has five days left, so it is OK.
- Matcha powder is already below its reorder level, so it is REORDER NOW even though it has four days left.

## Working out how much to order

For items needing attention, the program chooses the higher of:

- Seven days of daily usage.
- Twice the reorder level.

It then subtracts the current stock and rounds the difference up to a whole unit.

For Espresso beans:

```text
Seven days of use:       7 × 1.5 = 10.5 kg
Twice the reorder level: 2 × 3 = 6 kg
Target stock:            10.5 kg
Current stock:           4 kg
Amount needed:           6.5 kg
Suggested order:         7 kg
```

`max()` chooses the larger target, and `math.ceil()` rounds the order up. Items needing attention get a minimum suggestion of one unit. OK items get zero.

This is a simple rule. It does not check supplier pack sizes, storage space, or how long a product will keep.

## Showing the report

`filter_items()` keeps the selected category or removes items marked OK. `sort_items()` puts the results in the requested order.

`format_report()` combines the filename, rules, status counts, and item table into text. `main()` prints that text in the terminal.

The counts and displayed rows are handled separately. That is why the default report can count all 20 items while showing only the seven that need attention.

## Exporting the list

`write_reorder_csv()` saves the items needing attention to a CSV. Even when `--all` shows every item on screen, the export still leaves out OK items.

The file is opened in `"x"` mode, which only creates a new file. If the filename already exists, the program shows an error instead of replacing it.

The report is printed before export starts, so it can still appear on screen when saving fails.

## Python concepts used

The project uses functions to divide the work between files. Lists store the items and error messages, while dictionaries store each item's values.

Loops go through the records, and conditions decide which status to assign. Exception handling gives readable messages when something goes wrong. The CSV module handles reading the inventory and writing the reorder list.
