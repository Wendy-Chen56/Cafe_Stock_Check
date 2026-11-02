# Project Plan

## How someone would use it

The user saves the inventory as a CSV and runs the program from the project folder. The report shows which supplies need attention and suggests how much to order.

They can choose a category, change the warning period, sort the results, or export a reorder list.

The defaults are a three-day warning and a seven-day usage target. These are settings for this project, and the user can change them to suit the task.

## What goes in the CSV

| Column | What it contains | Example |
| --- | --- | --- |
| `item_id` | A unique code for the item | D201 |
| `item_name` | The supply name | Whole milk |
| `category` | A group used for filtering | Dairy |
| `unit` | The unit used for stock and daily usage | L |
| `quantity_on_hand` | How much is currently in stock | 18 |
| `daily_use` | About how much is used each day | 10 |
| `reorder_level` | The stock level that triggers REORDER NOW | 12 |

The file needs all seven headers. Capital letters and spaces around the headers are handled automatically. Blank or repeated headers cause an error. Extra named columns are ignored, but each row still needs the same number of values as the header.

Each item needs an ID and a name. An ID cannot repeat one already accepted from another row. Stock, usage, and reorder level must be finite numbers of zero or more.

A blank category becomes Uncategorized. The code currently allows a blank unit, but the user should fill it in so the suggested quantity makes sense.

## What the program does

1. Read the filename and options.
2. Open the CSV and check its headers.
3. Check each row, list any problems, and keep the valid items.
4. Calculate days left, stock status, and suggested order quantities.
5. Filter and sort the results, then print the report.
6. Save the items needing attention if the user requests an export.

If the file cannot be read or the headers are wrong, the program stops. If only some rows have problems, it skips those rows and continues. It also stops if no valid rows remain.

A report with skipped rows is incomplete. The user needs to fix those rows and run the file again.

## How the code is divided

| File | What it does |
| --- | --- |
| `src/main.py` | Reads the options and connects the steps |
| `src/load_data.py` | Opens the CSV and handles file-reading errors |
| `src/validate_data.py` | Checks the headers, IDs, names, row structure, and numbers |
| `src/reports.py` | Calculates results, filters, sorts, displays, and exports |

The program returns 0 when it finishes, 1 for a data or export problem, and 2 for an invalid command-line option. A run can finish with code 0 even when some rows were skipped, so the warning messages still matter.

## Rules used in the calculations

The program checks the reorder level first. If stock is at or below that level, the item is REORDER NOW.

If stock is above the reorder level, the program checks how many days it may last. An item within the warning period is ORDER SOON. Otherwise, it is OK.

When daily usage is zero, there is no days-left estimate. The reorder-level check still applies.

For an item needing attention, the program chooses the higher of:

- Target days multiplied by daily usage.
- Twice the reorder level.

It subtracts the stock already on hand, rounds the difference up to a whole unit, and keeps a minimum suggestion of one. OK items have a suggested order of zero.

The calculations use floats. Ratios and order differences are rounded to six decimal places at the relevant step. Days left is shown to one decimal place on screen and up to two in the CSV. The displayed number may therefore be slightly different from the value used to decide the status.

## What is left to do

I’ve run the main commands and worked through the code. Next, I’ll get feedback from a classmate or the instructor on whether the instructions and report are clear.

I’ll record any confusing steps and decide what needs changing. If I make a change, I’ll check it again and update the documents. I’ll then prepare the final demonstration and submission.
