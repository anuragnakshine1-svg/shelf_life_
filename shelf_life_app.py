import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from dateutil.relativedelta import relativedelta

st.title("📦 Shelf-Life Progress Calculator")

# Sidebar inputs
st.sidebar.header("Enter Details")
product_name = st.sidebar.text_input("Product Name")
start_date = st.sidebar.date_input("Start Date", datetime.today())
end_date = st.sidebar.date_input("End Date (optional)", None)
months = st.sidebar.number_input("Shelf Life (Months)", min_value=0, value=0)
days = st.sidebar.number_input("Shelf Life (Days)", min_value=0, value=0)
weeks = st.sidebar.number_input("Shelf Life (Weeks)", min_value=0, value=0)

today = datetime.today().date()

# --- Formula 1: Month-based ---
progress_months = None
if months > 0:
    expiry_months = start_date + relativedelta(months=months)
    progress_months = 100 * max(
        0,
        min(1, (expiry_months - today).days / (expiry_months - start_date).days)
    )

# --- Formula 2: Fixed start–end dates ---
progress_fixed = None
if end_date:
    total_days = (end_date - start_date).days
    remaining_days = (end_date - today).days

    if total_days > 0:
        progress_fixed = 100 - ((remaining_days / total_days) * 100)
        # Clamp between 0–100
        progress_fixed = max(0, min(100, progress_fixed))
    else:
        progress_fixed = None  # invalid range

# --- Formula 3: Days-based ---
progress_days = None
if days > 0:
    expiry_days = start_date + timedelta(days=days)
    progress_days = 100 * max(0, min(1, (expiry_days - today).days / days))

# --- Formula 4: Weeks-based ---
progress_weeks = None
if weeks > 0:
    expiry_weeks = start_date + timedelta(days=weeks*7)
    progress_weeks = 100 * max(0, min(1, (expiry_weeks - today).days / (weeks*7)))

# --- Display results in a table ---
st.subheader("📊 Results")
results = {
    "Product": [product_name],
    "Start Date": [start_date],
    "End Date": [end_date if end_date else "-"],
    "Shelf Life (Months)": [months],
    "Shelf Life (Days)": [days],
    "Shelf Life (Weeks)": [weeks],
    "Progress (Months)": [f"{progress_months:.2f}%" if progress_months is not None else "-"],
    "Progress (Fixed)": [f"{progress_fixed:.2f}%" if progress_fixed is not None else "-"],
    "Progress (Days)": [f"{progress_days:.2f}%" if progress_days is not None else "-"],
    "Progress (Weeks)": [f"{progress_weeks:.2f}%" if progress_weeks is not None else "-"]
}

df = pd.DataFrame(results)
st.dataframe(df)

# Progress bar (show whichever is last calculated)
if progress_months is not None:
    st.progress(progress_months/100)
elif progress_fixed is not None:
    st.progress(progress_fixed/100)
elif progress_days is not None:
    st.progress(progress_days/100)
elif progress_weeks is not None:
    st.progress(progress_weeks/100)
