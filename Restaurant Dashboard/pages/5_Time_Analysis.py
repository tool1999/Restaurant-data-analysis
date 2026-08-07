import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Time Analysis", page_icon="📅", layout="wide")

st.title("📅 Time Analysis")

# ==========================
# Read Data
# ==========================
df = pd.read_csv("restaurant_sales_cleaned.csv")

df["Order Date"] = pd.to_datetime(df["Order Date"])

# ==========================
# Sidebar Filters
# ==========================

years = sorted(df["Order Date"].dt.year.unique())

selected_year = st.sidebar.selectbox(
    "Select Year",
    years
)

filtered_df = df[df["Order Date"].dt.year == selected_year]

months = sorted(filtered_df["Order Date"].dt.month.unique())

month_names = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

selected_month = st.sidebar.selectbox(
    "Select Month",
    months,
    format_func=lambda x: month_names[x]
)

filtered_df = filtered_df[
    filtered_df["Order Date"].dt.month == selected_month
]

# ==========================
# Daily Sales
# ==========================

daily_sales = (
    filtered_df.groupby("Order Date")["Total price"]
    .sum()
    .reset_index()
)

fig = px.bar(
    daily_sales,
    x="Order Date",
    y="Total price",
    title="Daily Sales",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# Daily Sales Trend
# ==========================

fig = px.line(
    daily_sales,
    x="Order Date",
    y="Total price",
    title="Daily Sales Trend",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# Sales by Weekday
# ==========================

filtered_df["Day Name"] = filtered_df["Order Date"].dt.day_name()

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

weekday_sales = (
    filtered_df.groupby("Day Name")["Total price"]
    .sum()
    .reindex(days)
    .reset_index()
)

fig = px.bar(
    weekday_sales,
    x="Day Name",
    y="Total price",
    title="Sales by Day of Week",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)