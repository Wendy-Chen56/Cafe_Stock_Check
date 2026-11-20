# Cafe Stock Check

**Student:** Wendy Chen  
**Course:** MSBA 270 Python Programming

## Title

Cafe Stock Check

## Objective

Cafe Stock Check helps a café shift lead decide which supplies to reorder before closing. Instead of editing inventory rows in a spreadsheet, workers can select an item in a browser, enter the current stock, and review the supplies that need attention.

The goal is to reduce repeated typing and make stock decisions easier to follow. The app shows estimated days left, explains why an item is flagged, and suggests an order quantity for the shift lead to review.

I check the calculations against worked examples and ask classmates to follow the instructions. These checks help me assess whether the program works and can be started by another person. I have not measured whether it is faster or more accurate than using a spreadsheet.

## Dataset link

No external dataset is used. The project includes two sample files:

- `data/sample_inventory.csv`: 20 fictional café supplies.
- `data/sample_with_errors.csv`: eight rows, including five with deliberate errors.

Neither file contains actual café or customer records.

The browser initially loads the sample inventory. Stock changes are saved separately in `data/working_inventory.csv`, which is excluded from Git.

## Data and product

Each inventory record contains an item ID, name, category, stock unit, quantity on hand, estimated daily usage, and reorder level.

The app has three main features:

1. **Enter and save stock counts.** Workers select an existing item from a dropdown. The app displays its category and unit automatically. Workers enter the total stock on hand and save it without editing the CSV themselves. Dairy items also have an example 2 L container option that converts container counts into liters.

2. **Review stock warnings.** The report calculates days left, assigns REORDER NOW, ORDER SOON, or OK, and suggests an order quantity. Statuses have both colors and text labels, with a Reason column explaining each decision. Workers can filter by category or show only items needing attention.

3. **Download a reorder list.** Workers can download the attention items in the selected category as a CSV. The download is disabled when there are no matching attention items.

For example, the original sample has 18 L of whole milk and estimated usage of 10 L a day. That gives 1.8 days of stock. It is above its 12 L reorder level, so the app marks it ORDER SOON under the default three-day warning.

The default stock target is the higher of seven days of use or twice the reorder level. For milk, that target is 70 L, giving a suggested order of 52 L. The shift lead still needs to consider fridge space and shelf life before ordering.

## Scope and implementation

The main interface is a local Streamlit browser app. Its package versions are listed in `requirements.txt`. The original command-line program remains available and uses the same calculation functions.

The project uses these course concepts:

- Functions separate loading, validation, calculations, and saving across the files in `src`.
- Lists and dictionaries hold inventory records and validation messages.
- Loops and conditions process items and assign stock statuses in `src/reports.py`.
- Exception handling turns expected file and calculation problems into readable messages.
- File input and output load inventory, save working counts, and produce reorder CSVs.

The browser app uses a fixed sample item catalog. It does not currently provide screens for adding new products or changing daily usage and reorder levels. The container option is a demonstration of stock conversion, not a verified supplier catalog.

The app does not forecast demand, track stock usage automatically, contact suppliers, or place orders. It runs locally and has not been deployed as a public website.

## Testing and limitations

I tested the project on Windows with Python 3.13.9.

The original sample produced 4 REORDER NOW, 3 ORDER SOON, and 13 OK items. I checked filtering, exports, and invalid-input examples in the command-line version.

For the browser app, I checked stock updates, container conversion, status colors, filtering, CSV downloads, and empty results. Entering three 2 L containers saved 6 L. The milk report then showed 0.6 days left, REORDER NOW, and a suggested order of 64 L.

Saved stock remained after refreshing and restarting the app. Entering -1 triggered a minimum-value warning and did not change the saved inventory.

The earlier version's 50 automated tests passed on October 24, 2026. Those tests do not cover the new browser interface.

The browser download follows the browser's file-saving behavior. The original command-line export separately refuses to overwrite an existing file.

This is a local, single-user prototype using fictional data. It does not account for delivery time, expiry dates, storage capacity, or cost. Suggested orders are rounded to whole stock units, not supplier package sizes. I have not tested it in a working café or measured business savings.

## Progress and feedback

Professor Solis asked me to move the report into a browser, add guided inventory entry, make stock warnings easier to notice, and explain the benefit from the customer's point of view.

I added the browser report, stock form, item dropdown, container conversion, status colors, explanations, and download button in response. The completed changes and checks are recorded in `docs/instructor_feedback.md`.

A classmate followed the earlier command-line README and got the program running in about four minutes. A classmate also followed the updated README and started the browser app without my help. The browser check was not timed, and specific feedback on the form and report has not yet been recorded.

The next evaluation step is to ask a classmate to update a stock count, explain a flagged item, and download the reorder list. I will record any help needed or confusing steps. This will provide more information about usability than the setup check alone.
