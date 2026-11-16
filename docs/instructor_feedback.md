# Instructor Feedback and Improvement Plan

## What came up in the meeting

During the meeting, my professor asked me to explain the project as if she owned a coffee shop. I focused too much on the CSV file and Python code. I needed to show what a café worker would actually use and why it would help them.

Professor Solis suggested two main improvements: show the report in a web browser and give workers a form for entering inventory instead of editing a spreadsheet.

She also pointed out that workers could mistype item names or have trouble maintaining unique item IDs. She suggested dropdowns for items and sizes, with the system already knowing the category. For the report, she suggested red, yellow, and green status indicators.

Another question was why cold brew with 1.7 days left was marked REORDER NOW while whole milk with 1.8 days left was marked ORDER SOON. I need to make the reason behind each status easier to understand.

## What I plan to change

I plan to use Streamlit to build a browser interface around the existing calculations.

Workers will select an existing item and enter its current stock. The system will fill in its ID, category, and unit. Where package sizes are offered, the program will convert the entered amount into the item's stock unit.

The report will show the stock status with both color and text. It will also explain why an item needs attention. Workers will be able to review and export the reorder list from the browser.

## How I will check the changes

I will compare the browser report with the current program using the same sample data. The default results should still be 4 REORDER NOW, 3 ORDER SOON, and 13 OK.

I will also check that stock updates are saved and remain available after reopening the application. Invalid quantities should show a clear message without changing the saved inventory.

Finally, I will ask a classmate to select an item, update its stock, and find the reorder list. I will record any help they need and anything they find confusing.

## Current status

These changes are planned. I will add the completed changes, test results, and any further feedback after implementing them.