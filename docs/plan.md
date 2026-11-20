# Project Plan

## How someone uses the app

The café worker opens the running app in a browser, selects an item, and enters the total stock currently on hand. The app displays the item's category and unit automatically.

The worker can enter the stock directly in its existing unit. Dairy items also have an example 2 L container option. Three containers become 6 L before the stock calculations run.

After clicking Save stock, the worker can review the updated report, filter by category, show only items needing attention, and download a reorder list.

The browser uses a three-day warning and a seven-day usage target. The original command-line version lets users change these settings and choose a sort order.

## Inventory data

The project starts with 20 fictional café supplies in `data/sample_inventory.csv`.

| Column | What it contains | Example |
| --- | --- | --- |
| `item_id` | A unique item code | D201 |
| `item_name` | Supply name | Whole milk |
| `category` | Group used for filtering | Dairy |
| `unit` | Stock and daily usage unit | L |
| `quantity_on_hand` | Current stock | 18 |
| `daily_use` | Estimated usage per day | 10 |
| `reorder_level` | Stock level that triggers REORDER NOW | 12 |

All seven headers are required. Header capitalization and surrounding spaces are ignored. Blank or duplicate headers cause an error. Extra named columns are ignored, but each row must have the same number of values as the header.

IDs and names cannot be blank. IDs must be unique among accepted records. Stock, usage, and reorder level must be finite, nonnegative numbers.

A blank category becomes Uncategorized. Blank units are currently accepted by the loader, but should be filled in before using the inventory.

The browser uses the existing item catalog. It does not currently include screens for adding items or changing daily usage and reorder levels.

## Browser workflow

1. Load the working inventory if it exists. Otherwise, load the original sample.
2. Check the headers and validate the rows.
3. Show any validation warnings. Stop if no valid items remain.
4. Let the worker select an item and view its category and unit.
5. Accept a total stock count, converting containers into stock units where applicable.
6. When Save stock is clicked, check the quantity and calculations before saving.
7. Save the working inventory and recalculate the report.
8. Show summary counts, colored status labels, and an explanation for each item.
9. Apply the selected category and attention filter to the table.
10. Offer a CSV download containing only attention items in the selected category.

The summary counts cover all loaded items. The filters affect the table and download list.

If no items match the filters, the app shows a message. If there are no attention items in the selected category, the download button is disabled.

## Saving stock changes

The first run reads `data/sample_inventory.csv`. Saving a stock count creates or updates `data/working_inventory.csv`. Later runs use that working file.

The original sample is kept for demonstrations and repeatable checks. The working file is excluded from Git, so local stock changes are not uploaded.

Saving replaces the selected item's total stock count. It does not add a delivery to the previous count.

The save function writes the complete inventory to a temporary file before replacing the working file. This reduces the chance of leaving an incomplete CSV if writing fails.

This is local file storage for a single-user prototype. It does not provide a shared database, concurrent editing protection, or automatic backups.

## Validation and errors

File-reading problems and unusable headers stop processing. Invalid rows are reported and skipped when loading, so a report may contain only part of the inventory.

The browser blocks stock saves if any rows were skipped. This prevents saving a partial inventory over the working file. The source data needs to be corrected first.

The stock input has a minimum value of zero. The save handler also checks that the converted quantity is finite and nonnegative. Calculations are checked before writing the new inventory.

Expected data and saving errors are displayed as readable messages.

## How the code is divided

| File | What it does |
| --- | --- |
| `app.py` | Browser layout, item selection, stock form, filters, colored report, and download |
| `requirements.txt` | Lists the browser app's package versions |
| `src/inventory_store.py` | Saves the complete working inventory through a temporary file |
| `src/main.py` | Runs the original command-line workflow |
| `src/load_data.py` | Opens CSV files and handles file-reading errors |
| `src/validate_data.py` | Checks headers, row structure, IDs, names, and numeric values |
| `src/reports.py` | Shared stock calculations, filtering, sorting, and command-line reporting/export |

The browser app uses Streamlit, pandas, and Jinja2. Both interfaces reuse the original stock calculation functions.

Command-line exit codes remain 0 for a completed run, 1 for a data or export error, and 2 for an invalid option. These codes describe the command-line version, not browser interactions.

## Calculation rules

The program checks the reorder level first:

- Stock at or below the reorder level becomes REORDER NOW.
- Stock above that level becomes ORDER SOON if it will last three days or less under the browser's default settings.
- Otherwise, the item is OK.

Days left equals stock divided by daily usage. Zero usage gives no days-left estimate, but the reorder-level check still applies.

For an attention item, the stock target is the higher of:

- Target days multiplied by daily usage.
- Twice the reorder level.

The program subtracts current stock, rounds the difference up to a whole stock unit, and keeps a minimum suggestion of one. OK items have a suggestion of zero.

The container selector converts stock counts only. It does not round suggested orders to supplier package sizes.

Calculations use floats and round relevant intermediate values to six decimal places. The browser displays stock, daily use, and days left to one decimal place, and suggested orders as whole numbers. Exported days-left values use up to two decimal places. Display formatting does not change the underlying calculations.

## Checks completed

The original sample produced 20 items with counts of 4 REORDER NOW, 3 ORDER SOON, and 13 OK.

For the browser version, I checked:

- Selecting an item displays its category and unit.
- Saving Whole milk as 25 L gives 2.5 days left and a suggested order of 45 L.
- Saving three 2 L containers gives 6 L, 0.6 days left, REORDER NOW, and a suggested order of 64 L.
- Stock counts remain after refreshing and restarting the app.
- Updating Whole milk leaves Oat milk unchanged.
- Status colors and reasons appear in the report.
- Category filters apply to both the table and reorder download.
- An empty attention list disables downloading.
- Negative stock entry is blocked without changing the saved inventory.

Restarting the app exposed an import-order problem. I fixed it by adding the src path before importing the project modules, then checked that the app restarted successfully.

A classmate followed the updated README and started the browser app without my help. That check was not timed. Specific feedback on the form and report has not yet been recorded.

## Remaining work

Ask a classmate to update a stock count, explain a flagged item, and download the reorder list. Record any help needed or confusing steps.

Keep the test records and AI work log current as changes are made. Prepare the final demonstration around the worker's task and show how the project changed after the instructor's feedback.

The project has not been evaluated in a working café, so time savings, error reduction, and financial benefits remain unmeasured.
