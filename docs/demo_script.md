# Demo Script

## Before the demonstration

Start the app from the project folder:

```powershell
python -m streamlit run app.py
```

Open the browser before presenting. Keep Streamlit running in the terminal.

Check the current working inventory. Saved stock may differ from the original sample, so describe the values actually shown.

Select All categories and turn off the attention-only filter. Keep this script open separately as speaking notes.

## 1. Introduce the problem

My project is called Cafe Stock Check. It helps a café shift lead decide what to reorder before closing.

A stock count alone can be misleading. If there are 18 liters of milk but the café uses 10 liters a day, that is less than two days of stock.

The app brings the count, estimated days left, and reorder suggestion together so the shift lead can see what needs attention.

The data is fictional. This is a local prototype, not a system already used by a working café.

## 2. Explain what changed after feedback

[Show the browser.]

My first version showed a report in the terminal. Professor Solis asked me to think about how a café worker would use it.

I added this browser interface and a stock-entry form. Workers can select an existing item instead of typing its name, ID, and category into a spreadsheet.

I also added colored warnings and a reason for each status.

## 3. Update a stock count

[Select Whole milk. Choose Enter directly in L. Enter 25 and click Save stock.]

Here I select Whole milk. The app already knows that it belongs to Dairy and is measured in liters.

I enter the total stock currently on hand, not an amount to add. I’ll save 25 liters.

[Point to Whole milk in the report.]

At 10 liters of use per day, that gives 2.5 days left. The app marks it ORDER SOON and suggests 45 liters under the default target.

The shift lead still needs to check storage space and shelf life before placing an order.

## 4. Show container conversion

[Keep Whole milk selected. Choose 2 L container. Enter 3 and click Save stock.]

Instead of entering liters directly, I can count containers. Three 2-liter containers become 6 liters.

[Point to the updated milk row.]

The report now shows 0.6 days left and REORDER NOW. The stock is below the milk's 12-liter reorder level.

The suggested order is 64 liters because the default target is 70 liters and there are 6 liters left.

This container size is an example for the dairy sample. It is not a complete supplier package catalog.

## 5. Explain the warnings and download

[Point to the Status and Reason columns.]

Red means REORDER NOW, yellow means ORDER SOON, and green means OK. Each status also has a text label and an explanation.

The program checks the reorder level first. That is why an item can have several days left and still be marked REORDER NOW.

[Select Dairy in the report category filter.]

I can focus on one category. The summary numbers above still count the full inventory; the filter changes this table and the download list.

[Click Download reorder list and open the downloaded CSV.]

The download includes only attention items in this category. With these stock counts, that is Whole milk.

The app prepares a list for review. It does not place an order.

## 6. Explain saving and validation

The app saves stock counts in a separate working file, so the original sample stays available.

I checked that saved counts remain after refreshing the browser and restarting the app.

I also tried entering negative stock. The form blocked it, and the saved count did not change.

[Optional: demonstrate -1 in direct entry, show the warning, then refresh to clear the invalid input.]

## 7. Describe testing and feedback

I checked the calculations with examples and compared the downloaded records with the report. I also tested filters, container conversion, empty results, and saving.

A classmate followed the updated README and got the browser app running without my help. That check was not timed. I have not yet recorded detailed feedback on the form or report, or measured savings compared with spreadsheet work.

## 8. Wrap up

The main improvement is that the worker can now enter stock and review warnings in the browser instead of editing a spreadsheet and reading terminal output.

I used ChatGPT and Claude for development help, then ran the code and checked the results myself. The app itself does not connect to an AI service.

The next usability check is to ask someone to update a count, explain a warning, and download the list without guidance. That will tell me more than checking whether they can start the app.

## Possible questions

### Why is one item REORDER NOW and another ORDER SOON when their days left are similar?

The first check compares stock with each item's reorder level. Only items above that level are checked against the three-day warning. The Reason column explains which rule applied.

### Why does the app suggest so much milk?

The default target is the higher of seven days of usage or twice the reorder level. That is a simple rule, not an optimized purchasing decision. Storage space, shelf life, and delivery schedules still need human review.

### Why use this instead of Excel?

The browser gives workers a guided way to enter counts and immediately review stock warnings. Item details are already filled in. Excel can do similar calculations, but this app puts the entry and review steps together. I have not measured which approach is faster.

### Does a worker still need Python?

The computer hosting this local app needs Python and the required packages. Once Streamlit is running, workers use the browser interface. I have not deployed a public website.

### Where are stock changes stored?

They are stored in data/working_inventory.csv on the computer running the app. That file is excluded from Git. It is not shared cloud storage.

### Does it predict demand or automatically subtract daily use?

No. Daily usage is an estimate used to calculate days left. Stock changes when someone saves a new count.

### Does selecting a 2 L container change the order suggestion into containers?

No. It converts the stock count into liters. Suggested orders still use the item's stock unit and are not rounded to supplier package sizes.

### What Python concepts did you use?

Functions separate the main tasks. Lists and dictionaries hold inventory records. Loops and conditions check records and assign statuses. Exception handling reports expected problems, and CSV reading and writing handle storage and exports.
