import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# Page Config
# ==========================
st.set_page_config(
    page_title="Product Analysis",
    page_icon="🍕",
    layout="wide"
)

# ==========================
# Title
# ==========================
st.title("🍕 Product Analysis")
st.markdown("### Analyze Products Performance")

# ==========================
# Read Data
# ==========================
df = pd.read_csv("restaurant_sales_cleaned.csv")

df["Order Date"] = pd.to_datetime(df["Order Date"])

# ==========================
# Sidebar
# ==========================
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
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

selected_month = st.sidebar.selectbox(
    "Select Month",
    months
)

month_map = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}

# ==========================
# Filtering
# ==========================
filtered_df = df[df["Order Date"].dt.year == selected_year]

if selected_month != "All Year":
    filtered_df = filtered_df[
        filtered_df["Order Date"].dt.month == month_map[selected_month]
    ]
best_item = (
    filtered_df.groupby("Item")["Total price"]
    .sum()
    .idxmax()
)

best_sales = (
    filtered_df.groupby("Item")["Total price"]
    .sum()
    .max()
)
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🏆 Best Selling Item",
        best_item
    )

with col2:
    st.metric(
        "💰 Sales",
        f"${best_sales:,.0f}"
    )
    
st.divider()

st.subheader("📊 Top 10 Best Selling Products")
top_products = (
    filtered_df
    .groupby("Item")["Total price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig = px.bar(
    top_products,
    x="Total price",
    y="Item",
    orientation="h",
    text_auto=".2s",
    color="Total price"
)

fig.update_layout(
    yaxis=dict(categoryorder="total ascending"),
    xaxis_title="Sales ($)",
    yaxis_title="Product",
    coloraxis_showscale=False
)

st.plotly_chart(fig, use_container_width=True)