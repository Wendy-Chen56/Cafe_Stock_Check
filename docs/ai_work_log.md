# AI Work Log

## Starting the project

I used ChatGPT and Claude to help me work through Cafe Stock Check step by step. I started by asking how to build the project, then added my own ideas and asked follow-up questions as I went. They helped with code drafts, explanations, and troubleshooting. I ran the commands myself and checked the results. The program itself does not connect to an AI service.

I tested the command-line version on Windows with Python 3.13.9. I checked the default report, sorting, category filtering, the five-day warning, CSV export, and error handling. I opened the exported CSV in VS Code and confirmed that the program would not overwrite an existing file.

On October 24, 2026, I ran the previous version's 50 automated tests. All passed in 1.269 seconds. These tests apply to the earlier version, not the new browser interface.

## Adding the browser app

After meeting with Professor Solis, I asked ChatGPT to help me add a browser interface and stock-entry form. I shared my existing code so we could reuse its calculations.

I followed the steps to add a Streamlit report, an item dropdown, automatic category and unit display, and a form for saving stock counts. I also added an example 2 L container option for dairy items, colored status labels, explanations, filters, and a CSV download button.

I used the suggested approach of saving updates to a separate working inventory file. This kept the original sample available for repeatable checks.

## Problems and changes

When restarting the app caused a missing-module error, I asked ChatGPT for help. I moved the inventory_store import below the code that adds the src folder to Python's search path. I restarted the app to check the fix.

I also asked to shorten the long decimal values in the table. I applied display formatting so stock, daily use, and days left show one decimal place, while suggested orders show whole numbers. This changed the display, not the calculations.

## How I checked the browser version

I tested each change as I added it.

Saving Whole milk as 25 L gave 2.5 days left and a suggested order of 45 L. Entering three 2 L containers saved 6 L and gave 0.6 days left, REORDER NOW, and a suggested order of 64 L. The saved count stayed after refreshing and restarting the app.

I checked the downloaded CSV against the report. I also checked category filtering, the disabled download button when no items needed attention, and negative stock entry. Entering -1 showed a minimum-value warning, and the saved stock remained unchanged.

A classmate followed the earlier command-line README and got it running in about four minutes. A classmate also followed the updated README and got the browser app running without my help. The browser check was not timed, and I have not recorded specific feedback on the form or report.

## What I learned

I asked follow-up questions when I did not understand the code and worked through examples to check the answers. This helped me understand the difference between REORDER NOW and ORDER SOON, the suggested-order calculation, and how the browser connects to the existing functions.

I also learned why refreshing a page and restarting an application are separate checks. The restart test found an import problem that I then fixed.
