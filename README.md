# Cafe Stock Check

Cafe Stock Check helps a café shift lead figure out which supplies need ordering before closing. It reads an inventory CSV, checks the stock and daily usage, and shows the items that need attention.

The goal is to make the stock check easier and help users avoid overlooking an item. Users can review the suggested quantities and export a reorder list. The program does not place orders.

## Main features

- Read an inventory CSV and explain problems with the file or individual rows.
- Calculate days of stock left, assign a stock status, and suggest an order quantity.
- Filter and sort the report, then export the items needing attention.

## What you need

- A computer with Python 3.9 or newer.
- VS Code to open the project and use its terminal.

This project was tested on Windows with Python 3.13.9.

It uses only Python's standard library. You do not need to install packages, create a virtual environment, or set up an API key.

## 1. Install Python and VS Code

If both are already installed, skip to Step 2.

Download Python from:

https://www.python.org/downloads/

Download VS Code from:

https://code.visualstudio.com/

Follow the installation instructions. After installing Python, close and reopen VS Code so its terminal can recognize the installation.

## 2. Download the project

On the GitHub page containing this project:

1. Click the green **Code** button.
2. Select **Download ZIP**.
3. Find the downloaded ZIP file.
4. Right-click it and select **Extract All**.
5. Open the extracted folder and find `cafe-stock-check`.

If you downloaded the whole course repository, the project may be inside that repository's folder.

The correct project folder contains:

- `README.md`
- `.gitignore`
- `data`
- `src`
- `docs`

Extract the files before running the program.

## 3. Open the project in VS Code

1. Open VS Code.
2. Select **File → Open Folder**.
3. Choose the `cafe-stock-check` folder.
4. Click **Select Folder**.
5. If a trust prompt appears, confirm that you opened the project you intended to download.

The project files should appear in the Explorer panel on the left.

## 4. Open the terminal and check Python

Select **Terminal → New Terminal**.

On Windows, check your current folder:

```powershell
Get-Location
```

The location should be the folder containing this project's `README.md`, `data`, and `src`.

Then check Python:

```powershell
python --version
```

You should see a Python version number.

If `python` is not recognized, try:

```powershell
py --version
```

If `py` works, use `py` instead of `python` in the commands below. On macOS or Linux, you may need to use `python3`.

## 5. Run the sample inventory

Enter:

```powershell
python src/main.py data/sample_inventory.csv
```

The sample contains 20 items. The report should include:

```text
Items checked: 20 | REORDER NOW: 4 | ORDER SOON: 3 | OK: 13
```

By default, the table only shows the seven items needing attention.

For example, Whole milk should be:

```text
Whole milk   Dairy   18 L   10   1.8   ORDER SOON   52 L
```

This means there are 18 liters in stock, estimated usage is 10 liters per day, and the stock may last 1.8 days. The suggested order is 52 liters under the default rules.

## 6. Try the report options

### Show every item in name order

```powershell
python src/main.py data/sample_inventory.csv --all --sort name
```

`--all` includes items marked OK. `--sort name` sorts by item name.

You should see all 20 items.

### Show only dairy items

```powershell
python src/main.py data/sample_inventory.csv --category Dairy --all
```

The report should show Whole milk, Oat milk, and Heavy cream:

```text
Items checked: 3 | REORDER NOW: 0 | ORDER SOON: 1 | OK: 2
```

Category matching ignores capitalization.

### Change the warning period to five days

```powershell
python src/main.py data/sample_inventory.csv --warn-days 5
```

The counts should change to:

```text
Items checked: 20 | REORDER NOW: 4 | ORDER SOON: 6 | OK: 10
```

Croissants, Lids, and Oat milk are added to the attention list.

### Sort all items by days left

```powershell
python src/main.py data/sample_inventory.csv --all --sort days
```

Items with fewer days left appear first. Items without a days-left estimate appear last.

### View the available options

```powershell
python src/main.py --help
```

| Option | What it does | Default |
| --- | --- | --- |
| `--warn-days N` | Warn when stock will last N days or less | 3 |
| `--target-days N` | Set the usage-based stock target | 7 |
| `--sort` | Choose urgency, days, name, or category | urgency |
| `--category NAME` | Select one category | All categories |
| `--all` | Display OK items too | Off |
| `--export FILE` | Save a reorder CSV | No export |

Options only apply to the current run. For example, a run without `--warn-days 5` returns to the default three-day warning.

## 7. Export a reorder list

Run:

```powershell
python src/main.py data/sample_inventory.csv --export reorder_list.csv
```

The last line should say:

```text
Saved reorder list (7 item(s)) to reorder_list.csv
```

With this command, the file is saved in the project folder.

Click `reorder_list.csv` in VS Code to inspect it. You can also open it in a spreadsheet program. It should contain a header and seven records.

The Whole milk record should be:

```csv
D201,Whole milk,Dairy,L,18,10,1.8,ORDER SOON,52
```

Export includes only the items needing attention, even when `--all` displays every item on screen. A category filter also applies to the export.

### Check overwrite protection

Run the same export command again:

```powershell
python src/main.py data/sample_inventory.csv --export reorder_list.csv
```

The program should show:

```text
Error: 'reorder_list.csv' already exists. Choose a new export filename.
```

This is expected. The existing file is not replaced. To save another list, choose a new filename.

## 8. Try the error examples

### Invalid rows

Run:

```powershell
python src/main.py data/sample_with_errors.csv
```

The program should report five skipped rows:

- A quantity written as `six`.
- A negative daily usage value.
- A blank item name.
- A duplicate item ID.
- A missing reorder-level value.

It should continue with three valid items:

```text
Items checked: 3 | REORDER NOW: 1 | ORDER SOON: 1 | OK: 1
```

The report only includes valid rows. Correct the skipped rows and run the file again before treating it as a complete inventory check.

### Missing file

Run this with a filename that does not exist:

```powershell
python src/main.py missing.csv
```

Expected message:

```text
Error: File not found: 'missing.csv'. Check the name and folder.
```

### Negative warning period

```powershell
python src/main.py data/sample_inventory.csv --warn-days=-2
```

The program should reject the option. Warning days must be finite and zero or more. Target days must be finite and greater than zero.

### Unknown category

```powershell
python src/main.py data/sample_inventory.csv --category Fruit
```

Expected message:

```text
Error: No items found in category 'Fruit'.
```

## How the stock rules work

The program checks the reorder level first.

| Status | Rule |
| --- | --- |
| REORDER NOW | Stock is at or below the reorder level |
| ORDER SOON | Stock is above the reorder level, but days left is at or below the warning period |
| OK | Neither condition applies |

Days left is calculated as:

```text
Stock on hand ÷ daily usage
```

If daily usage is zero, the report shows `-` for days left. The reorder-level check still applies.

For items needing attention, the target stock is the higher of:

- Target days multiplied by daily usage.
- Twice the reorder level.

The program subtracts current stock and rounds the difference up to a whole unit. The minimum suggestion is one unit. OK items have a suggested order of zero.

For Whole milk:

```text
Days left:        18 ÷ 10 = 1.8 days
Target stock:     max(7 × 10, 2 × 12) = 70 L
Suggested order:  70 − 18 = 52 L
```

The calculations use floats and round the relevant intermediate values to six decimal places. Days left is displayed to one decimal place on screen and up to two in the CSV. The displayed value may be slightly different from the value used for the status check.

## Using another inventory file

Use a UTF-8 CSV with these headers:

```csv
item_id,item_name,category,unit,quantity_on_hand,daily_use,reorder_level
```

Example row:

```csv
D201,Whole milk,Dairy,L,18,10,12
```

| Column | Meaning |
| --- | --- |
| `item_id` | Unique item code |
| `item_name` | Supply name |
| `category` | Group used for filtering |
| `unit` | Stock unit, such as L, kg, or bottle |
| `quantity_on_hand` | Current stock |
| `daily_use` | Estimated daily usage |
| `reorder_level` | Stock level that triggers REORDER NOW |

All seven headers are required. Header capitalization and surrounding spaces are ignored. Blank or duplicate headers are rejected. Extra named columns are ignored.

IDs and names cannot be blank. IDs must be unique among accepted rows. Numeric values must be finite and nonnegative. A blank category becomes Uncategorized.

A blank unit is currently allowed, but fill it in before using the order list. Stock, daily usage, and reorder level must use the same unit for each item.

Both supplied CSVs contain fictional café supplies. No external dataset or actual café or customer records are used.

## Project files

| Location | Contents |
| --- | --- |
| `data/sample_inventory.csv` | Twenty fictional inventory items |
| `data/sample_with_errors.csv` | Sample data with deliberate errors |
| `src/main.py` | Command-line options and program flow |
| `src/load_data.py` | CSV loading and file errors |
| `src/validate_data.py` | Header and row checks |
| `src/reports.py` | Calculations, sorting, filtering, display, and export |
| `docs/proposal.md` | Project objective, user, and scope |
| `docs/plan.md` | Workflow and implementation plan |
| `docs/code_guide.md` | Explanation of the main functions |
| `docs/demo_script.md` | Demonstration commands and speaking notes |
| `docs/evaluation_plan.md` | Plan for getting user feedback |
| `docs/manual_test_checklist.md` | Recorded checks and expected results |
| `docs/ai_work_log.md` | Development assistance and personal verification |
| `docs/sample_report.txt` | Example report output |

## Testing and current progress

The main commands were tested on Windows with Python 3.13.9. The checks covered the sample report, sorting, filtering, changing the warning period, export, and invalid inputs.

The earlier version's 50 automated tests passed on October 24, 2026. Those test files are not included in this version. The source code and sample data remain unchanged.

Use the manual checks above to test this version. Recorded results are in [docs/manual_test_checklist.md](docs/manual_test_checklist.md).

Feedback from a classmate or the instructor is still pending. Time savings have not been measured. See [docs/evaluation_plan.md](docs/evaluation_plan.md).

## Python concepts used

| Concept | Where it appears |
| --- | --- |
| Functions | Loading, validation, calculations, and reporting are separate functions |
| Lists and dictionaries | `validate_rows()` stores valid items and problems; each item is a dictionary |
| Loops and conditions | `analyze_items()` processes items and assigns their statuses |
| Exception handling | File, conversion, and export errors become readable messages |
| File input and output | `read_csv_rows()` reads inventory; `write_reorder_csv()` saves the list |

More explanation is in [docs/code_guide.md](docs/code_guide.md).

## Common problems

### Python is not recognized

Try `py --version` on Windows. If neither command works, check that Python is installed and reopen VS Code after installation.

### Python cannot find src/main.py

Check the terminal's current folder:

```powershell
Get-Location
Get-ChildItem
```

You should be in the folder containing `src`, `data`, `docs`, and `README.md`. Open that folder in VS Code, then create a new terminal.

### The inventory file cannot be found

Check the filename and path. The sample command assumes the terminal is in the project folder.

### The export file already exists

Choose a new export filename. The program deliberately refuses to overwrite existing files.

### Some rows were skipped

Read the line numbers and reasons in the warning messages. Correct those rows and run the file again.

## Limitations

The report depends on the stock and daily usage figures entered in the CSV. It does not predict changes in demand or account for delivery times, supplier pack sizes, expiry dates, storage space, or cost.

Review suggested quantities before ordering, especially for perishable supplies. The program does not place orders or contact suppliers.

## AI assistance

I worked on this project with support from ChatGPT and Claude. They helped with code drafts, explanations, and troubleshooting. I ran the program, checked the output, and reviewed the functions myself.

More details are in [docs/ai_work_log.md](docs/ai_work_log.md). The application itself does not use AI.
