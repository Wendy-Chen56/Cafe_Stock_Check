# Code Guide

## Starting the app

Run the browser version from the project folder:

```powershell
python -m streamlit run app.py
```

Streamlit runs `app.py` and displays the interface in a browser. Interacting with controls normally reruns the script. Inputs inside the stock form are submitted together when Save stock is clicked.

The original command-line version is still available:

```powershell
python src/main.py data/sample_inventory.csv
```

Its `build_parser()` function defines options such as `--category` and `--warn-days`. Its `main()` function reads those options and calls the loading, validation, and reporting functions.

Both versions use the calculations in `src/reports.py`.

## Finding the project files

In `app.py`, the project folder is found from the location of the script:

```python
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "src"))
```

This lets the app find its data and import functions from `src`. The path must be added before importing modules such as `inventory_store`.

The browser loads `data/working_inventory.csv` if it exists. Otherwise, it uses `data/sample_inventory.csv`.

## Reading and checking the CSV

`read_csv_rows()` in `src/load_data.py` uses `csv.DictReader`. Each row becomes a dictionary:

```python
row["item_name"]         # "Whole milk"
row["quantity_on_hand"]  # "18"
```

At this point, "18" is text. The reader trims and lowercases headers, handles a UTF-8 BOM, and records line numbers for error messages.

`check_columns()` checks for required, blank, and duplicate headers. `validate_rows()` checks each record for missing IDs or names, duplicate IDs, and invalid numbers.

`parse_number()` converts numeric text into a float. It rejects blank, negative, and nonfinite values. For example, "18" becomes 18.0, while "six" cannot be used.

Validation returns two lists: valid items and problem messages. Invalid rows are skipped and reported. Both entry points stop if no valid items remain.

The browser also blocks stock saves when rows were skipped. This prevents a partial set of valid records from replacing the working inventory.

Expected file problems become `DataError` messages. The command-line version prints them; the browser displays them with `st.error()`.

## Selecting an item and entering stock

In `app.py`, `items_by_id` maps each item ID to its inventory record. The item dropdown uses those IDs internally but displays item names.

Once an item is selected, the app shows its category and unit from the record. The worker does not type an ID, name, or category.

The form accepts the total stock currently on hand. Saving replaces the previous count; it does not add a delivery.

For dairy items measured in liters, the app offers an example 2 L container option:

```python
new_quantity = entered_amount * package_size
```

Three containers multiplied by 2 gives 6 L. Direct entry uses a multiplier of one. Partial containers are allowed.

The form uses `st.number_input()` with a minimum of zero. The save handler also checks that the converted quantity is finite and nonnegative.

## Saving the stock count

When Save stock is submitted, the app copies the inventory records and changes the selected item's quantity in the copied list.

It calls `analyze_items()` before saving to check that the updated inventory can be calculated. It then passes the updated records to `save_inventory()` in `src/inventory_store.py`.

That function:

1. Creates a temporary file in the working file's folder.
2. Writes the required CSV headers and inventory records.
3. Closes the temporary file.
4. Uses `os.replace()` to replace the working inventory.
5. Attempts to remove any leftover temporary file.

Writing the complete temporary file first reduces the risk of leaving a partially written working CSV. It does not provide backups or protection against multiple users overwriting each other's changes.

After saving, the app calculates the report from the updated records. Later runs load the saved working inventory. The original sample is not changed by the stock form.

## Calculating stock status

`analyze_items()` in `src/reports.py` calculates days left when daily usage is positive:

```python
days_left = round(quantity / daily_use, 6)
```

For the original Whole milk sample, 18 L divided by 10 L per day gives 1.8 days.

If daily usage is zero, the function uses `None` instead of dividing by zero. The reorder-level rule still applies.

The status checks run in this order:

```python
if quantity <= reorder_level:
    status = "REORDER NOW"
elif days_left is not None and days_left <= warn_days:
    status = "ORDER SOON"
else:
    status = "OK"
```

The first check compares stock quantities. The second compares days. Similar days-left estimates can therefore produce different statuses.

With the original sample and a three-day warning:

- Whole milk is above its reorder level but has only 1.8 days left, so it is ORDER SOON.
- Oat milk is above its reorder level and has five days left, so it is OK.
- Matcha powder is below its reorder level, so it is REORDER NOW despite having four days left.

If Whole milk is updated to 6 L, it is below its 12 L reorder level and becomes REORDER NOW.

## Calculating suggested orders

For attention items, the function chooses the higher of target days multiplied by daily usage or twice the reorder level.

It subtracts current stock, rounds the difference to six decimal places, and uses `math.ceil()` to round up to a whole stock unit. The minimum suggestion for an attention item is one. OK items receive zero.

For Espresso beans under the default seven-day target:

```text
Seven days of use:       7 * 1.5 = 10.5 kg
Twice the reorder level: 2 * 3 = 6 kg
Target stock:            10.5 kg
Current stock:           4 kg
Amount needed:           6.5 kg
Suggested order:          7 kg
```

For Whole milk, the target is 70 L. With 6 L on hand, the suggestion is 64 L.

The container selector changes how stock is entered. It does not round suggested orders to supplier package sizes or account for storage and shelf life.

## Showing the browser report

`count_by_status()` counts all analyzed items. `st.columns()` and `st.metric()` display the summary counts.

The category dropdown and attention checkbox select which records appear in the table. They do not change the summary counts.

For each displayed record, the app adds a readable status reason. The records become a pandas DataFrame, and a styling function colors the Status cells:

- Red for REORDER NOW.
- Yellow for ORDER SOON.
- Green for OK.

Text labels remain visible alongside the colors.

Display formatting shows stock, daily use, and days left to one decimal place, and suggested orders as whole numbers. This does not change the calculation values.

If the filters produce no records, the app shows a message instead of a table.

## Downloading from the browser

The app selects attention items from the category-filtered results. OK items are excluded even when they appear in the table.

`csv.DictWriter` writes the export into an `io.StringIO` buffer. The app converts it to UTF-8 with a BOM and supplies it to `st.download_button()`.

Days-left values are rounded to two decimal places for export. Missing estimates are written as empty values.

The browser handles the download location and repeated filenames. The download does not replace the working inventory. When there are no attention items to export, the button is disabled.

## Command-line reporting and export

In the original version, `filter_items()` selects a category or attention items, and `sort_items()` applies the requested order.

`format_report()` builds a text report that `main()` prints in the terminal. Its counts and displayed rows are handled separately, so it can count 20 items while displaying only seven.

`write_reorder_csv()` opens the export file in `"x"` mode. This creates a new file and refuses an existing filename.

That protection belongs to the command-line export. Working-inventory saves deliberately replace the working file, while browser downloads follow the browser's behavior.

## Python concepts used

Functions separate loading, validation, calculations, and saving. Lists hold inventory items and problem messages. Dictionaries hold each record and connect item IDs to dropdown selections.

Loops process records, while conditions check input and assign stock statuses. Exceptions turn expected failures into readable messages. CSV reading and writing let the app load inventory, keep saved counts, and export results.

The Streamlit interface calls these functions so workers can use the inventory workflow from a browser.