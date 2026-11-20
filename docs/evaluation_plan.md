# Evaluation Plan and Results

## What I want to check

I want to check whether someone can start the browser app from the README, update a stock count, understand a warning, and download a reorder list.

Starting the app and completing the inventory task are separate checks. A successful setup does not tell me whether the form and report are clear.

## Checks already completed

A classmate followed the earlier command-line README and got the program running in about four minutes.

A classmate also followed the updated README and started the browser app without my help. This check was not timed. I have not recorded specific feedback about entering stock, interpreting the report, or downloading the list.

| Check | Recorded result |
| --- | --- |
| Earlier command-line setup | Program started in about four minutes |
| Browser setup using the updated README | App started successfully |
| Help during the browser setup check | None |
| Browser setup time | Not measured |
| Browser reviewer's name and test date | Not recorded |
| Detailed form and report feedback | Not recorded |

These results describe setup only. They are not evidence of time savings compared with spreadsheet work.

## Instructor feedback and changes

Professor Solis asked for a browser report, guided stock entry, dropdowns, clearer status indicators, and a better explanation of customer value.

I added a Streamlit interface, stock-entry form, item dropdown, automatic category and unit display, an example container conversion, colored status labels, and a Reason column.

I checked these features locally. The changes and results are recorded in `docs/instructor_feedback.md`.

The classmate setup check does not establish that every change is easy to use.

## Next usability check

Ask a reviewer to complete these tasks using the README. Do not show the expected answers first. Record any help given.

1. Start the browser app.
2. Select Whole milk and check its category and stock unit.
3. Choose direct entry in liters, enter a total stock count of 25, and save.
4. Find Whole milk in the report and explain its status.
5. Choose the 2 L container option, enter three containers, and save.
6. Explain how the saved quantity and stock status changed.
7. Select Dairy in the report filter and download the reorder list.
8. Find and open the downloaded CSV.
9. Explain whether the quantity entered replaces the stock count or adds to it.
10. Describe any confusing instructions, labels, or results.

Use fictional data. If the reviewer has working counts they want to keep, have them test a separate copy of the project.

## Expected results for these tasks

These answers are for the reviewer tasks above. They do not depend on Whole milk's starting count because the reviewer explicitly saves new totals.

| Task | Expected result |
| --- | --- |
| Select Whole milk | Category Dairy and stock unit L |
| Save a total of 25 L | 25 L, 2.5 days left, ORDER SOON, suggested order 45 L |
| Save three 2 L containers | 6 L, 0.6 days left, REORDER NOW, suggested order 64 L |
| Explain the status change | At 25 L, milk is above its reorder level but within the three-day warning; at 6 L, it is below its 12 L reorder level |
| Explain the input | It replaces the total stock count rather than adding a delivery |

If Oat milk and Heavy cream still have their original sample values, the Dairy download should contain only Whole milk. If those items were changed earlier, check the export against their current statuses instead.

The download should include only attention items in the selected category.

## Original sample reference

With the unchanged sample and default settings, the counts are 4 REORDER NOW, 3 ORDER SOON, and 13 OK.

The seven attention items are:

- Cold brew concentrate
- Caramel syrup
- Matcha powder
- Sanitizer wipes
- Whole milk
- 12oz cups
- Espresso beans

Whole milk is ORDER SOON at its original 18 L count. Matcha powder is REORDER NOW because its stock is below its reorder level.

These original results apply before stock updates. A browser using a saved working inventory may show different results.

## Usability results to record

| Check | Result or comment |
| --- | --- |
| Participant code and date | Pending |
| Could they select an item and understand its unit? | Pending |
| Could they save a total stock count? | Pending |
| Could they use the container option correctly? | Pending |
| Could they explain the status and reason? | Pending |
| Could they download and open the CSV? | Pending |
| Did they understand that saving replaces the count? | Pending |
| What help did they need? | Pending |
| Which steps or labels were confusing? | Pending |

Record observed results rather than assuming success because the app started.

## Optional comparison with a spreadsheet

A separate comparison could measure how long it takes to identify attention items and count missed items or wrong additions.

If this comparison is carried out, record the task, starting data, time, accuracy, and help given for each method. Using the same data twice may let the reviewer remember the answers.

No spreadsheet-versus-app time or accuracy comparison has been recorded.

## Changes after the usability check

- Issue reported or observed: Pending.
- Change made and reason: Pending.
- Result after checking the change: Pending.

If no change is needed, record what was checked and why the current design was kept.

## Limits

This evaluation uses fictional data and a small number of reviewers. A classmate is not necessarily representative of a café worker.

The completed setup check shows that another person could start the app from the instructions without my help. Further task testing can provide feedback on the workflow, but neither check proves savings, fewer stockouts, or better results in a working café.
