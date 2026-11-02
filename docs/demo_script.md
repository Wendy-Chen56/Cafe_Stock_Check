# Demo Script

## Introduction

My project is called Cafe Stock Check. I built it to help the person closing a café figure out which supplies need to be ordered.

It reads an inventory CSV and checks the stock against the reorder levels and daily usage. The sample data is made up, and the program runs locally without installing extra packages.

## Run the default report

```powershell
python src/main.py data/sample_inventory.csv
```

Here I have 20 items. Four are at or below their reorder levels, and another three may run out within three days. The program shows those seven items and leaves out the thirteen marked OK.

Let’s look at whole milk. There are 18 liters left, and the estimated daily use is 10 liters. That means it will last about 1.8 days.

The stock is still above its reorder level, but it is getting close to running out, so the program marks it ORDER SOON.

The suggested order is 52 liters, based on the default stock target. Before actually ordering, the person would still need to check storage space and how long the milk will keep.

## Change the warning period

```powershell
python src/main.py data/sample_inventory.csv --warn-days 5
```

Now I’m changing the warning period from three days to five.

Croissants, Lids, and Oat milk are added to the list, so there are ten items needing attention. The inventory is the same. I’m just asking the program to warn me earlier.

## Try a file with errors

```powershell
python src/main.py data/sample_with_errors.csv
```

This file has a few mistakes on purpose. For example, one quantity says “six” instead of using a number, and another row has a negative daily usage value.

The program lists the problems and skips five rows. It can still analyze the three valid items.

This also tells me that the report is only based on part of the file. I would need to fix those errors and run it again to get the full list.

## Export the reorder list

```powershell
python src/main.py data/sample_inventory.csv --export demo_orders.csv
```

Use a filename that does not already exist.

This saves the seven items needing attention to a CSV that I can open in a spreadsheet.

If I try the same filename again, the program refuses to overwrite it. That protects the file I already saved.

The program prepares the list, but it does not place an order or send anything to a supplier.

## Wrap up

The idea is to make it easier to find the supplies that need attention without checking every row manually.

I’ve tested the calculations and tried the main commands on my computer. I still need feedback from a classmate or the instructor to find out whether the report is clear and useful. I haven’t measured time savings yet.

## Possible questions

**Why is Matcha REORDER NOW if it still has four days left?**

Its stock is already below the reorder level. The program checks that first, before checking the days left.

**Why does Oat milk change when you use a five-day warning?**

It has five days of stock left. That is outside the three-day warning, but it is included when I change the setting to five days.

**Why does the program suggest seven kilograms of Espresso beans?**

The target is 10.5 kilograms, and there are four kilograms left. The difference is 6.5, which the program rounds up to seven.

**Does the program predict demand?**

No. It uses the daily usage estimate in the CSV. If that estimate is wrong or demand changes, the result may not reflect what actually happens.
