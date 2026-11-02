# Test Record

## My setup

I ran the project on Windows using Python 3.13.9 in the VS Code terminal. I first tested it on October 24, 2026, and repeated the main commands on October 29.

## What I checked

| Test | What happened |
| --- | --- |
| Default report | The program checked 20 items: 4 REORDER NOW, 3 ORDER SOON, and 13 OK. It displayed the seven items needing attention. |
| Sort by name | Using `--all --sort name` showed all 20 items in name order. |
| Dairy filter | The report showed Whole milk, Oat milk, and Heavy cream. One was ORDER SOON and two were OK. |
| Five-day warning | ORDER SOON increased from three items to six. Croissants, Lids, and Oat milk were added. |
| CSV export | The program created `reorder_list.csv` with seven records. |
| Export contents | I opened the CSV in VS Code and checked the records. Whole milk had a suggested order of 52 L. |
| Existing filename | Running the export again showed an already-exists error instead of replacing the file. |
| Invalid data | The error sample reported five bad rows and continued with three valid items. |
| Missing file | Running the program with `missing.csv` showed a clear file-not-found message. |
| Negative warning period | Using `--warn-days=-2` showed an error explaining that the value must be zero or more. |
| Unknown category | Using `--category Fruit` showed a message saying no items were found in that category. |
| Sort by days left | Using `--all --sort days` listed the items from the fewest days left to the most. |

## Commands I used

Run these from the `cafe-stock-check` folder:

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

The export command needs a new filename. Running it again with the same name is how I checked the overwrite protection.

## Checking the calculations

The default report gave these results:

| Item | Status | Suggested order |
| --- | --- | --- |
| Cold brew concentrate | REORDER NOW | 7 L |
| Caramel syrup | REORDER NOW | 3 bottles |
| Matcha powder | REORDER NOW | 1 kg |
| Sanitizer wipes | REORDER NOW | 2 packs |
| Whole milk | ORDER SOON | 52 L |
| 12oz cups | ORDER SOON | 13 sleeves |
| Espresso beans | ORDER SOON | 7 kg |

I worked through the whole-milk example:

- Days left: 18 ÷ 10 = 1.8 days.
- Seven days of usage: 7 × 10 = 70 L.
- Twice the reorder level: 2 × 12 = 24 L.
- The larger target is 70 L.
- Suggested order: 70 − 18 = 52 L.

For Espresso beans, the target is max(7 × 1.5, 2 × 3) = 10.5 kg. There are 4 kg left, so the difference is 6.5 kg. The program rounds that up to 7 kg.

## Earlier automated tests

On October 24, I ran:

```powershell
python -m unittest discover -s tests -v
```

The result was:

```text
Ran 50 tests in 1.269s

OK
```

That result came from the earlier version, which included the test files. The current folder does not include the old `tests` folder. The manual checks above record what I ran with the current project.

## Still to check

I checked the exported CSV in VS Code, but I have not recorded a check in Excel or another spreadsheet program.

Feedback from a classmate or the instructor is still pending. I have not measured whether the program saves users time yet.
