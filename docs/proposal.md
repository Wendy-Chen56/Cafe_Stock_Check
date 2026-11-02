# Cafe Stock Check

**Student:** Wendy Chen  
**Course:** MSBA 270 Python Programming

## Title

Cafe Stock Check

## Objective

I’m building a Python program to help the person closing a café figure out which supplies need to be ordered. Instead of checking every row in a spreadsheet, they can run the program and get a list of items that are low in stock or may run out soon.

I want to see whether this makes the task faster and helps people miss fewer items. I plan to ask classmates to try both the spreadsheet and the program, then compare their time and answers. I haven’t done that comparison yet.

## Dataset link

I’m using sample data for this project, so there is no external dataset link.

- `data/sample_inventory.csv` contains 20 made-up café supplies.
- `data/sample_with_errors.csv` contains eight rows, with five rows that have errors for testing.

Neither file contains real café or customer information.

## Data and product

Each row includes an item’s ID, name, category, unit, current stock, estimated daily use, and reorder level.

The program does three main things:

1. Reads the CSV and reports problems such as missing values, negative numbers, or duplicate IDs. It skips invalid rows and continues with the valid ones.
2. Calculates how many days the stock may last, labels each item REORDER NOW, ORDER SOON, or OK, and suggests how much to order. Users can also sort the list or select a category.
3. Saves the items needing attention to a new CSV. It won’t overwrite a file that already exists.

For example, the sample has 18 liters of whole milk, and the café uses about 10 liters a day. That leaves only 1.8 days of milk. The program marks it ORDER SOON and suggests ordering 52 liters under the default rules. The person ordering still needs to check whether that amount makes sense for the café’s storage space and how long the milk will keep.

## Scope

The program runs in a terminal and uses Python’s standard library, so there are no extra packages to install. It uses the functions, lists, dictionaries, loops, conditions, error handling, and file operations covered in class.

It works with the numbers entered in the CSV. It doesn’t predict future demand, contact suppliers, or place orders.

The café is an example for this project. I haven’t tested the program in a working café, so I can’t say yet how much time or money it would save there.

## Progress

I’ve run the program on Windows with Python 3.13.9. I checked the sample report, sorting, category filter, five-day warning, and CSV export. I also tried the error file and confirmed that an existing export file could not be overwritten.

On October 24, 2026, I ran the earlier version’s 50 automated tests. All passed.

Next, I’ll get feedback from a classmate or the instructor to see whether the report is clear and useful, then decide what needs improvement.
