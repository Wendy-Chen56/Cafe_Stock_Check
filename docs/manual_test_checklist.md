# Test Record

## My setup

I tested the project on Windows with Python 3.13.9 using the VS Code terminal.

The original command-line checks were run on October 24, 2026, and the main commands were repeated on October 29. The browser checks below were completed while adding the Streamlit version.

The browser environment used:

- Streamlit 1.51.0
- pandas 2.3.3
- Jinja2 3.1.6

## Command-line checks

These checks use the original sample inventory.

| Test | Recorded result |
| --- | --- |
| Default report | 20 items: 4 REORDER NOW, 3 ORDER SOON, and 13 OK; seven attention items displayed |
| Sort by name | `--all --sort name` showed all 20 items in name order |
| Dairy filter | Whole milk, Oat milk, and Heavy cream appeared; counts were 0 / 1 / 2 |
| Five-day warning | Counts changed to 4 / 6 / 10; Croissants, Lids, and Oat milk became ORDER SOON |
| CSV export | Created `reorder_list.csv` with seven records |
| Export contents | Opened the CSV in VS Code; Whole milk's suggested order was 52 L |
| Existing filename | Repeating the export showed an already-exists error |
| Invalid data | Five rows were skipped and three valid items were analyzed |
| Missing file | `missing.csv` produced a file-not-found message |
| Negative warning period | `--warn-days=-2` was rejected |
| Unknown category | `--category Fruit` reported that no matching items were found |
| Sort by days left | `--all --sort days` listed items from fewer days left to more |

## Command-line commands

Run these from the project folder:

```powershell
python src/main.py data/sample_inventory.csv
python src/main.py data/sample_inventory.csv --all --sort name
python src/main.py data/sample_inventory.csv --category Dairy --all
python src/main.py data/sample_inventory.csv --warn-days 5
python src/main.py data/sample_inventory.csv --export reorder_list.csv
python src/main.py data/sample_with_errors.csv
python src/main.py missing.csv
python src/main.py data/sample_inventory.csv --warn-days=-2
python src/main.py data/sample_inventory.csv --category Fruit
python src/main.py data/sample_inventory.csv --all --sort days
```

The first export needs an unused filename. Repeating the same export checks overwrite protection.

## Browser checks

Start the browser app with:

```powershell
python -m streamlit run app.py
```

The original sample counts apply before stock changes are saved. Later runs load the local working inventory, which may have different quantities and statuses.

| Test | Recorded result |
| --- | --- |
| Start the browser app | Cafe Stock Check opened in the browser |
| Original sample report | Summary showed 20 items with counts 4 / 3 / 13 |
| Category filter | Selecting Dairy showed Whole milk, Oat milk, and Heavy cream |
| Item dropdown | Selecting Whole milk displayed category Dairy and unit L |
| Attention-only filter | With the original sample, the table showed seven items and no OK items |
| Status reasons | Cold brew and Whole milk displayed different reasons for their warnings |
| Save Whole milk as 25 L | Report showed 25 L, 2.5 days, ORDER SOON, and suggested order 45 L |
| Refresh after saving | Whole milk remained at 25 L |
| Check another item | Oat milk remained at 30 L after updating Whole milk |
| Container conversion | Entering three 2 L containers saved 6 L |
| Recalculate after conversion | Whole milk showed 0.6 days, REORDER NOW, and suggested order 64 L |
| Switch entry methods | Direct entry showed 6 L and container entry showed 3 |
| Refresh after conversion | The saved 6 L and equivalent container count remained |
| Status colors | Red, yellow, and green backgrounds appeared with the status labels |
| Download updated inventory results | CSV showed Whole milk at 6 L, 0.6 days, REORDER NOW, and suggested order 64 L |
| Category-filtered download | With Dairy selected, the download contained only Whole milk under the tested stock counts |
| No attention items | Selecting Bakery and attention-only showed no matching items and disabled the download |
| Stop and restart | After fixing the import order, the app restarted and Whole milk remained at 6 L |
| Negative stock entry | Entering -1 showed a minimum-value warning; after refreshing, Whole milk remained at 6 L |
| Number formatting | Stock, daily use, and days left displayed one decimal place; suggested orders displayed whole numbers |
| Package dependencies | `python -m pip check` returned `No broken requirements found.` |

The negative-entry check confirms the form's minimum-value protection and that the saved count stayed unchanged. It does not separately test every validation branch in the Python save handler.

The package dependency check does not test application behavior.

## Problem found and fix

Stopping and restarting the browser app exposed this error:

```text
ModuleNotFoundError: No module named 'inventory_store'
```

The import appeared before the code that adds the src folder to Python's search path.

I moved the import below that path setup and restarted the app. The browser opened successfully, and the saved stock was still available.

I also shortened the table's decimal display after seeing long values such as 6.000000. This changed the display format without changing the calculation values.

## Calculation checks

With the original sample and default settings:

| Item | Status | Suggested order |
| --- | --- | --- |
| Cold brew concentrate | REORDER NOW | 7 L |
| Caramel syrup | REORDER NOW | 3 bottles |
| Matcha powder | REORDER NOW | 1 kg |
| Sanitizer wipes | REORDER NOW | 2 packs |
| Whole milk | ORDER SOON | 52 L |
| 12oz cups | ORDER SOON | 13 sleeves |
| Espresso beans | ORDER SOON | 7 kg |

For Whole milk, the target is:

```text
max(7 * 10, 2 * 12) = 70 L
```

The checks used these quantities:

| Stock on hand | Days left | Status | Suggested order |
| --- | --- | --- | --- |
| 18 L | 1.8 | ORDER SOON | 52 L |
| 25 L | 2.5 | ORDER SOON | 45 L |
| 6 L | 0.6 | REORDER NOW | 64 L |

The 6 L count is below the 12 L reorder level, so it becomes REORDER NOW.

For Espresso beans:

```text
Target: max(7 * 1.5, 2 * 3) = 10.5 kg
Amount needed: 10.5 − 4 = 6.5 kg
Suggested order: rounded up to 7 kg
```

## Earlier automated tests

On October 24, 2026, I ran the earlier package's test suite:

```powershell
python -m unittest discover -s tests -v
```

The result was:

```text
Ran 50 tests in 1.269s

OK
```

The current package does not include those test scripts. This historical result is not an automated test of the new browser app. The browser results above are manual checks.

## Classmate and instructor feedback

A classmate followed the earlier command-line README and got the program running in about four minutes.

A classmate also followed the updated README and started the browser app without my help. This check was not timed. Specific feedback on the form, status explanations, and download task has not yet been recorded.

Professor Solis's feedback led to the browser report, guided stock entry, dropdowns, colored warnings, and clearer status explanations. The feedback and completed changes are recorded in `docs/instructor_feedback.md`.

## Remaining checks and limits

- A separate classmate task check is still needed for updating stock, interpreting a warning, and downloading the list.
- Opening the exported CSV in Excel or another spreadsheet program has not been recorded.
- A fresh installation in an isolated environment has not been recorded.
- Saving when the file is locked or unwritable has not been manually tested.
- No timed spreadsheet comparison or real café evaluation has been completed.

These checks provide evidence about the tested examples. They do not establish time savings, financial savings, or reliability in a multi-user café environment.
