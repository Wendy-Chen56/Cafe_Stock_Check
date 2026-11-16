import sys
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "src"))

from load_data import read_csv_rows
from validate_data import DataError, check_columns, validate_rows
from reports import analyze_items, count_by_status, sort_items

st.set_page_config(
    page_title="Cafe Stock Check",
    page_icon="☕",
    layout="wide",
)

st.title("☕ Cafe Stock Check")
st.write("Check your inventory and see which supplies need reordering.")
st.caption("Demo inventory: 20 fictional café supplies.")

try:
    inventory_path = BASE_DIR / "data" / "sample_inventory.csv"

    column_names, rows = read_csv_rows(inventory_path)
    check_columns(column_names)
    items, problems = validate_rows(rows)

    for problem in problems:
        st.warning(problem)

    if not items:
        raise DataError("No valid inventory items were found.")

    results = analyze_items(items)
    results = sort_items(results, "urgency")
    counts = count_by_status(results)

    total, reorder, soon, okay = st.columns(4)

    total.metric("Items checked", len(results))
    reorder.metric("🔴 Reorder now", counts["REORDER NOW"])
    soon.metric("🟡 Order soon", counts["ORDER SOON"])
    okay.metric("🟢 OK", counts["OK"])
    
    with st.expander("What do the stock statuses mean?"):
        st.write(
            "🔴 REORDER NOW: Stock is at or below the item's reorder level."
        )
        st.write(
            "🟡 ORDER SOON: Stock is above the reorder level, "
            "but will last three days or less."
        )
        st.write(
            "🟢 OK: Stock is above the reorder level "
            "and does not trigger the three-day warning."
        )
        st.caption(
            "The reorder-level check comes first. "
            "Days left uses the daily usage estimate entered for each item."
        )    
    
    st.subheader("Inventory report")

    categories = sorted({item["category"] for item in results})
    selected_category = st.selectbox(
        "Choose a category",
        ["All categories"] + categories,
    )

    filtered_results = [
        item for item in results
        if selected_category == "All categories"
        or item["category"] == selected_category
    ]

    attention_only = st.checkbox("Show only items that need reordering")

    if attention_only:
        filtered_results = [
            item for item in filtered_results
            if item["status"] != "OK"
        ]

    display_rows = []

    for item in filtered_results:
        if item["status"] == "REORDER NOW":
            reason = "Stock is at or below the reorder level."
        elif item["status"] == "ORDER SOON":
            reason = "Stock will last three days or less."
        elif item["days_left"] is None:
            reason = "Above reorder level; no daily usage estimate."
        else:
            reason = "Above reorder level with more than three days left."

        display_rows.append({
            "Item": item["item_name"],
            "Category": item["category"],
            "Unit": item["unit"],
            "On hand": item["quantity_on_hand"],
            "Daily use": item["daily_use"],
            "Days left": (
                round(item["days_left"], 1)
                if item["days_left"] is not None
                else None
            ),
            "Reason": reason,
            "Suggested order": item["suggested_order"],
        })

    st.dataframe(display_rows, hide_index=True)

except DataError as error:
    st.error(str(error))