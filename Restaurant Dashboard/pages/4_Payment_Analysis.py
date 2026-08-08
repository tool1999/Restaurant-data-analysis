import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# Page Config
# ==========================
st.set_page_config(
    page_title="Payment Analysis",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Payment Analysis")
st.markdown("### Analyze Payment Methods")

# ==========================
# Read Data
# ==========================
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(BASE_DIR, "restaurant_sales_cleaned.csv"))

df["Order Date"] = pd.to_datetime(df["Order Date"])

# ==========================
# Sidebar
# ==========================
st.sidebar.header("🔍 Filters")

years = sorted(df["Order Date"].dt.year.unique())

selected_year = st.sidebar.selectbox(
    "Select Year",
    years
)

months = [
    "All Year",
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

selected_month = st.sidebar.selectbox(
    "Select Month",
    months
)

month_map = {
    "Jan":1,"Feb":2,"Mar":3,"Apr":4,
    "May":5,"Jun":6,"Jul":7,"Aug":8,
    "Sep":9,"Oct":10,"Nov":11,"Dec":12
}

# ==========================
# Filtering
# ==========================
filtered_df = df[df["Order Date"].dt.year == selected_year]

if selected_month != "All Year":
    filtered_df = filtered_df[
        filtered_df["Order Date"].dt.month == month_map[selected_month]
    ]

# ==========================
# KPIs
# ==========================

most_used = (
    filtered_df["Payment Method"]
    .value_counts()
    .idxmax()
)

highest_revenue = (
    filtered_df.groupby("Payment Method")["Total price"]
    .sum()
    .idxmax()
)

total_transactions = filtered_df["Order ID"].nunique()

avg_transaction = filtered_df["Total price"].mean()

# ==========================
# Display KPIs
# ==========================

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric("💳 Most Used", most_used)

with col2:
    st.metric("💰 Highest Revenue", highest_revenue)

with col3:
    st.metric("🧾 Transactions", total_transactions)

with col4:
    st.metric("💵 Avg Transaction", f"${avg_transaction:,.2f}")

st.divider()

# ==========================
# Chart 1
# Transactions
# ==========================

transactions = (
    filtered_df
    .groupby("Payment Method")["Order ID"]
    .nunique()
    .sort_values(ascending=False)
    .reset_index(name="Transactions")
)

fig1 = px.bar(
    transactions,
    x="Payment Method",
    y="Transactions",
    color="Transactions",
    text_auto=True,
    color_continuous_scale="Purples"
)

fig1.update_layout(
    title="Transactions by Payment Method",
    xaxis_title="Payment Method",
    yaxis_title="Transactions",
    coloraxis_showscale=False,
    xaxis={"categoryorder": "total descending"}
)

# ==========================
# Chart 2
# Revenue
# ==========================

revenue = (
    filtered_df
    .groupby("Payment Method")["Total price"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    revenue,
    names="Payment Method",
    values="Total price",
    hole=0.45
)

fig2.update_traces(textposition="inside", textinfo="percent+label")

fig2.update_layout(
    title="Revenue by Payment Method"
)

# ==========================
# Display Charts
# ==========================

col1,col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1,use_container_width=True)

with col2:
    st.plotly_chart(fig2,use_container_width=True)