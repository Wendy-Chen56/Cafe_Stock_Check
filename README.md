# Cafe Stock Check

**Student:** Wendy Chen  
**Course:** MSBA 270 Python Programming

Cafe Stock Check helps a café shift lead decide which supplies to reorder before closing. Workers select an item, enter the stock they counted, and review a list of supplies that need attention.

The browser app shows how many days the stock may last, why an item is flagged, and a suggested order quantity. The goal is to reduce manual entry and make the next stock decision easier to see. Actual time or cost savings have not been measured.

## What the app does

- Update stock through a form. Selecting an item fills in its category and stock unit.
- Enter quantities directly, or use an example 2 L container option for dairy items. Three 2 L containers become 6 L of stock.
- Show red, yellow, and green stock statuses with text labels and explanations.
- Filter the report by category or show only items needing attention.
- Save working inventory locally and download a reorder CSV from the browser.

The original command-line program is also included. Both versions use the same stock calculations.

## 1. Install the tools

The browser app was checked on Windows with Python 3.13.9. Use that Python version to follow the tested setup. You also need a web browser. These instructions use VS Code to open the project and its terminal, though another editor or terminal can be used.

If needed, install:

- [Python](https://www.python.org/downloads/)
- [VS Code](https://code.visualstudio.com/)

After installation, close and reopen VS Code. Downloading the project and installing packages require internet access. Once installed, the app runs locally without an AI account or API key.

## 2. Download the project

1. Open [the Cafe Stock Check repository](https://github.com/Wendy-Chen56/Cafe_Stock_Check).
2. Click the green **Code** button.
3. Select **Download ZIP**.
4. Find the downloaded ZIP file, right-click it, and select **Extract All**.
5. Open the extracted project folder, usually named `Cafe_Stock_Check-main`.

The correct folder contains `app.py`, `requirements.txt`, `README.md`, `data`, `src`, and `docs`. Extract the ZIP before running the program.

## 3. Open the project and terminal

1. Open VS Code.
2. Select **File → Open Folder**.
3. Choose the extracted project folder containing `app.py`.
4. Click **Select Folder**. If asked about trust, confirm that this is the project you intended to open.
5. Select **Terminal → New Terminal**.

In the Windows terminal, check the folder:

```powershell
Get-Location
Get-ChildItem
```

You should see `app.py` and `requirements.txt` in the file list. Then check Python:

```powershell
python --version
```

If `python` is not recognized, try `py --version`. If that works, replace `python` with `py` in every command below, including installation and launch. On macOS or Linux, you may need `python3` instead.

## 4. Install the browser app's packages

Run this from the project folder:

```powershell
python -m pip install -r requirements.txt
```

Wait until installation finishes and the terminal prompt returns. The file lists the versions used for the working browser app:

```text
streamlit==1.51.0
pandas==2.3.3
Jinja2==3.1.6
```

Streamlit provides the browser interface. Pandas and Jinja2 support the colored report table. The command-line version uses only Python's standard library.

## 5. Start the browser app

In the same terminal, run:

```powershell
python -m streamlit run app.py
```

Your browser should open with the **Cafe Stock Check** heading. If it does not, open the **Local URL** printed in the terminal, usually `http://localhost:8501`.

Keep that terminal running while using the app. To stop the app, click in the terminal and press **Ctrl + C**. Use the same launch command to start it again.

This is a locally running app, not a publicly hosted website. The computer running Streamlit still needs Python and the installed packages. Once the app is running, the inventory work happens in the browser.

## 6. Update a stock count

1. Under **Update stock**, use **Choose an item** to select a supply, such as **Whole milk**.
2. Check the category and stock unit shown underneath. These come from the item's record; workers do not type an ID or category.
3. Under **How are you counting this item?**, select direct entry or an available container size.
4. Enter the **total stock currently on hand**. This replaces the previous count; it does not add a delivery to it.
5. Click **Save stock**.
6. Check the saved message and updated report.

For example, choosing **2 L container** and entering **3** saves **6 L**. Partial containers are allowed. Switching to **Enter directly in L** should show the equivalent 6 L.

The 2 L choice is an example for the fictional dairy inventory. It is not a verified supplier package size. Other items currently use their existing stock unit directly.

Selecting another item or changing a number alone does not save it. Click **Save stock** to apply the count.

## 7. Read and filter the report

The four summary numbers count **all loaded inventory items**. Category and attention filters change the table and download list; they do not change those summary totals.

- **Choose a category** limits the table to a group such as Dairy or Coffee.
- **Show only items that need reordering** hides items marked OK.
- **What do the stock statuses mean?** explains the three rules.
- The **Reason** column explains each item's status. Scroll sideways if it is outside the visible table area.

The report starts in urgency order. It keeps text labels as well as colors so users do not have to rely on color alone.

With the original sample, before saving any changes, the totals are:

```text
Items checked: 20 | REORDER NOW: 4 | ORDER SOON: 3 | OK: 13
```

Saving new stock counts can change these totals. They are not fixed targets for every run.

## 8. Download the reorder list

1. Select **All categories**, or choose a category for a smaller list.
2. Click **Download reorder list** below the report.
3. Open `cafe_reorder_list.csv` from your browser's download location.

The file includes a header and only the items needing attention in the selected category. Showing OK items in the table does not add them to the download. If there are no attention items, the download button is disabled.

For a saved Whole milk count of 6 L, its downloaded record should show:

| Field | Value |
| --- | --- |
| `quantity_on_hand` | 6 or 6.0 |
| `days_left` | 0.6 |
| `status` | REORDER NOW |
| `suggested_order` | 64 |

The browser handles where downloads are saved and how repeated filenames are treated. This differs from the command-line export, which refuses to overwrite an existing file.

## Where stock changes are saved

On first use, the browser app reads `data/sample_inventory.csv`. After **Save stock**, it writes the complete working inventory to `data/working_inventory.csv`. Later runs read that working file, so saved counts remain after refreshing the page or restarting the app.

- The original sample is kept for repeatable demonstrations and command-line checks.
- The working inventory is ignored by Git. Pushing the project does not upload your local stock counts.
- A newly downloaded copy starts with the supplied sample, not Wendy's working inventory.
- Storage is on the computer running the app. It is not shared cloud storage.

If you need a fresh sample demonstration, stop the app and move the working file to a safe backup location before restarting. Keep any counts you still need. The app will use the original sample when no working file is present.

## How the stock rules work

The reorder-level check comes first:

| Status | Rule |
| --- | --- |
| REORDER NOW | Stock is at or below the item's reorder level |
| ORDER SOON | Stock is above the reorder level, but will last three days or less |
| OK | Neither warning applies |

Days left equals stock divided by daily usage. Zero daily usage gives no days-left estimate, but the reorder-level rule still applies. The browser may show an empty estimate; the command-line report shows `-`.

For attention items, the target is the higher of seven days of usage or twice the reorder level. The program subtracts current stock, rounds up to a whole stock unit, and keeps a minimum suggestion of one. OK items have a suggested order of zero.

For the original Whole milk record:

```text
Days left:       18 / 10 = 1.8 days
Target stock:    max(7 * 10, 2 * 12) = 70 L
Suggested order: 70 - 18 = 52 L
```

After saving 6 L, Whole milk is below its 12 L reorder level. It becomes REORDER NOW, and its suggested order is 70 - 6 = 64 L.

Cold brew and milk can have similar days left but different statuses because the first check compares each item's stock with its own reorder level. The Reason column makes that distinction visible.

The calculations round relevant intermediate values to six decimal places. Days left is displayed to one decimal place in the report and up to two in the exported CSV, so a displayed estimate can differ slightly from the value used for a decision. Suggested orders are expressed in the stock unit, not rounded to the selected container size.

Review suggested quantities before ordering, especially for milk or other perishable supplies.

## Original command-line version

Run these commands from the project folder. They use the unchanged sample, regardless of stock saved in the browser.

```powershell
python src/main.py data/sample_inventory.csv
```

Expected counts: **4 REORDER NOW, 3 ORDER SOON, 13 OK**. The table shows the seven attention items.

| Task | Command |
| --- | --- |
| Show all items by name | `python src/main.py data/sample_inventory.csv --all --sort name` |
| Show all dairy items | `python src/main.py data/sample_inventory.csv --category Dairy --all` |
| Use a five-day warning | `python src/main.py data/sample_inventory.csv --warn-days 5` |
| Sort all items by days left | `python src/main.py data/sample_inventory.csv --all --sort days` |
| Export the default attention list | `python src/main.py data/sample_inventory.csv --export reorder_list.csv` |
| Try the error sample | `python src/main.py data/sample_with_errors.csv` |
| See all options | `python src/main.py --help` |

The command-line version also supports `--target-days N` and sorting by urgency, days, name, or category. These options apply only to that run. They do not change the browser app's default three-day warning or seven-day target.

The Dairy sample gives counts **0 / 1 / 2**. A five-day warning gives **4 / 6 / 10**. Exporting the default sample creates a header and seven records. Use a new filename if `reorder_list.csv` already exists; command-line export refuses to replace it.

To inspect the browser's saved inventory from the terminal after a save, use:

```powershell
python src/main.py data/working_inventory.csv
```

## Data and error handling

The supplied files contain fictional café supplies. No external dataset, actual café records, or customer information is included.

Inventory files use these seven required headers:

```csv
item_id,item_name,category,unit,quantity_on_hand,daily_use,reorder_level
```

Example:

```csv
D201,Whole milk,Dairy,L,18,10,12
```

IDs and names must not be blank. IDs must be unique among accepted rows. Stock, daily use, and reorder level must be finite, nonnegative numbers expressed in the same unit for each item. A blank category becomes Uncategorized. Blank units are accepted by the loader, but should be filled in before using the report.

The reader accepts UTF-8 CSV files, including a BOM. Header case and surrounding spaces are ignored. Missing, blank, or duplicate headers stop the run. Rows with invalid values or a mismatched number of fields are skipped with an explanation.

The browser displays loading warnings and blocks stock saves if any rows were skipped, so saving does not silently discard those records. Correct the source data before relying on a partial report. The current browser app does not include a CSV upload control or screens for adding new catalog items, changing daily usage, or editing reorder levels.

The error sample contains eight rows: five are skipped and three are analyzed. The resulting counts are **1 REORDER NOW, 1 ORDER SOON, 1 OK**.

Additional command-line error checks:

```powershell
python src/main.py missing.csv
python src/main.py data/sample_inventory.csv --warn-days=-2
python src/main.py data/sample_inventory.csv --category Fruit
```

These should report a missing file, reject a negative warning period, and explain that no Fruit category was found. Do not expect inventory results from these deliberately invalid commands.

## Testing and feedback

The following browser checks were completed locally during development:

- The initial sample report showed 20 items with counts 4 / 3 / 13.
- Selecting Dairy showed Whole milk, Oat milk, and Heavy cream.
- Saving Whole milk as 25 L updated its estimate to 2.5 days and its suggested order to 45 L. The saved count remained after a browser refresh, and Oat milk remained at 30 L.
- Saving three 2 L containers produced 6 L, 0.6 days, REORDER NOW, and a suggested order of 64 L. Direct and container entry agreed after refreshing.
- Status cells displayed red, yellow, and green backgrounds with their text labels.
- The downloaded CSV contained the updated milk values. A Dairy download contained only Whole milk under the tested stock counts.
- Selecting Bakery with the attention filter showed no matching items and disabled download.
- The installed environment returned `No broken requirements found.` from `python -m pip check`. This checks package dependencies, not application behavior.

Earlier command-line checks covered sorting, filtering, export, existing-file protection, and invalid inputs. The previous version's 50 automated tests passed on October 24, 2026. Those scripts are not included in this package, and that result is not an automated test of the new browser app.

A classmate followed the earlier README and got the command-line project running in about four minutes. That was a setup/run check, not a measured comparison with spreadsheet work. The browser version still needs a separate classmate usability check.

The instructor asked for a browser report, guided stock entry, clearer status cues, and a stronger explanation of customer value. This version adds those interfaces around the original calculations. The feedback and initial plan are in [docs/instructor_feedback.md](docs/instructor_feedback.md). Earlier test records are in [docs/manual_test_checklist.md](docs/manual_test_checklist.md).

## Project files

| Location | Purpose |
| --- | --- |
| `app.py` | Browser interface, stock-entry form, filters, colored report, and download |
| `requirements.txt` | Browser app dependencies and tested package versions |
| `.gitignore` | Excludes local working stock, Python cache, and other local files |
| `data/sample_inventory.csv` | Twenty fictional inventory items |
| `data/sample_with_errors.csv` | Inventory with deliberate row errors |
| `data/working_inventory.csv` | Created locally when stock is saved; excluded from Git |
| `src/main.py` | Original command-line entry point |
| `src/load_data.py` | CSV loading and file errors |
| `src/validate_data.py` | Header and row validation |
| `src/reports.py` | Shared calculations and command-line report/export functions |
| `src/inventory_store.py` | Writes a temporary file, then replaces the working inventory |
| `docs/instructor_feedback.md` | Instructor feedback and initial improvement plan |
| `docs/proposal.md` | Original project proposal |
| `docs/plan.md` | Original implementation plan |
| `docs/code_guide.md` | Guide to the original core functions |
| `docs/demo_script.md` | Earlier command-line demonstration notes |
| `docs/evaluation_plan.md` | Evaluation tasks and feedback plan |
| `docs/manual_test_checklist.md` | Earlier local checks and calculation examples |
| `docs/ai_work_log.md` | AI assistance and personal verification |
| `docs/sample_report.txt` | Original command-line sample output |

## Python concepts used

| Concept | Example in this project |
| --- | --- |
| Functions | Loading, validation, analysis, and saving are separate functions |
| Lists and dictionaries | Each inventory item is a dictionary; lists hold items and validation problems |
| Loops and conditions | `analyze_items()` processes records and assigns a status; the form checks input before saving |
| Exception handling | `DataError` reports expected file and calculation problems; the browser shows readable errors |
| File input and output | Inventory is loaded from CSV and saved to a working CSV; the reorder list can be downloaded |

## Common problems

**The terminal says `No module named streamlit`, `pandas`, or `jinja2`.**

Run `python -m pip install -r requirements.txt` using the same Python command you use to launch the app.

**Streamlit cannot find `app.py`.**

Run `Get-Location` and `Get-ChildItem` on Windows. Open the folder containing `app.py` in VS Code and create a terminal there.

**The browser did not open, or the page stopped responding.**

Check that Streamlit is still running in the terminal. Open the Local URL it prints. Restart with `python -m streamlit run app.py` if you stopped it.

**The report does not match the original sample counts.**

Check whether you have already saved stock. The browser reads your working inventory after the first save. The command-line sample command still reads the original sample.

**I changed the input, but the report did not change.**

Click **Save stock**. Enter the complete stock count rather than the quantity of a new delivery.

**The command-line program says `csv_file` is required.**

Give it a file path: `python src/main.py data/sample_inventory.csv`. Running `main.py` without that argument is incomplete. The browser app uses the separate Streamlit launch command.

## Limits

The report relies on the stock counts, usage estimates, and reorder levels entered for each item. It does not forecast demand, account for delivery lead times, calculate expiry or storage capacity, or optimize supplier orders and cost. The container selector converts stock counts; it does not round suggested orders to supplier pack sizes.

This is a local, single-user class prototype with a small fixed item catalog. It has no login, shared database, concurrent editing protection, automatic usage tracking, or supplier connection. Stock changes only when a worker saves a new count. Temporary-file saving helps avoid incomplete writes, but does not replace backups or a multi-user database.

## AI assistance

I used ChatGPT and Claude to help me work through the project step by step. I added my own ideas, asked follow-up questions, and used their help with code drafts, explanations, and troubleshooting. I ran the commands and checked the results myself. More details are in [docs/ai_work_log.md](docs/ai_work_log.md).

The application itself does not connect to an AI service.
