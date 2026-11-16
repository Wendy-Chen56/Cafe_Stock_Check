# Instructor Feedback and Project Updates

## Feedback from the meeting

During the meeting, Professor Solis asked me to explain the project as if she owned a coffee shop. I spent too much time talking about the CSV and Python files instead of showing what a café worker would use.

She suggested showing the report in a browser and adding a form so workers would not have to edit a spreadsheet. She also suggested dropdowns for items and sizes, automatic categories, and red, yellow, and green stock indicators.

She questioned why cold brew with 1.7 days left was marked REORDER NOW while whole milk with 1.8 days left was marked ORDER SOON. I needed to make the reason behind each status clearer.

## What I changed

I added a Streamlit browser app that uses the original stock calculations.

Workers can now select an item from a dropdown. The app displays its category and stock unit automatically, so they do not need to type an item ID or name.

The stock form lets workers enter the total quantity on hand and save it. Dairy items also have an example 2 L container option. The app converts container counts into liters before calculating the report.

The report now has colored status cells and a Reason column. Workers can filter by category, show only items needing attention, and download the reorder list.

Saved counts go into a separate working inventory file. The original sample stays available for demonstrations and checks. I also updated the README and added the required packages.

## What I checked

I ran the browser app locally and checked these results:

| Check | Result |
| --- | --- |
| Original sample | 20 items: 4 REORDER NOW, 3 ORDER SOON, 13 OK |
| Save Whole milk as 25 L | Report showed 2.5 days left and a suggested order of 45 L |
| Refresh after saving | Whole milk stayed at 25 L; Oat milk remained at 30 L |
| Enter three 2 L containers | Saved 6 L; report showed 0.6 days, REORDER NOW, and a suggested order of 64 L |
| Switch entry methods and refresh | Direct entry showed 6 L; container entry showed 3 |
| Status colors | Red, yellow, and green appeared with the status labels |
| Download the reorder list | CSV contained the updated milk values |
| Download with Dairy selected | CSV contained only Whole milk under the tested stock counts |
| Bakery with attention-only selected | No matching items; download button was disabled |
| Package dependency check | No broken requirements found |

These are my local checks. They do not show measured time or cost savings.

## What I learned

The meeting helped me see that explaining the code is different from showing someone how a product helps them. I can now demonstrate the task directly: select an item, enter a count, save it, and review what needs ordering.

The status explanation also matters. Similar days-left values can have different statuses because the program checks each item's reorder level first.

## What still needs checking

A classmate previously followed the command-line README and got the program running in about four minutes. That was a setup check for the earlier version.

I still need someone to try the browser version and tell me whether the form and report are clear. I also need to check invalid stock entry and confirm that saved counts remain after stopping and restarting the app.

The browser app runs locally and still needs Python and the packages installed on the host computer. It has not been deployed as a public website.

These updates have been implemented and checked locally. I have not yet received Professor Solis's review of this version.