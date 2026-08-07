import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# Page Config
# ==========================
st.set_page_config(
    page_title="Customer Analysis",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Customer Analysis")
st.markdown("### Analyze Customer Behavior")

# ==========================
# Read Data
# ==========================
df = pd.read_csv("restaurant_sales_cleaned.csv")
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

# Filter by Year
filtered_df = df[df["Order Date"].dt.year == selected_year]

# Filter by Month
if selected_month != "All Year":
    filtered_df = filtered_df[
        filtered_df["Order Date"].dt.month == month_map[selected_month]
    ]
# ==========================
total_customers = filtered_df["Customer ID"].nunique()

total_orders = filtered_df["Order ID"].nunique()

avg_spending = (
    filtered_df.groupby("Customer ID")["Total price"]
    .sum()
    .mean()
)

top_customer = (
    filtered_df.groupby("Customer ID")["Total price"]
    .sum()
    .idxmax()
)

# ==========================
# Display KPIs
# ==========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Total Customers", total_customers)

with col2:
    st.metric("🧾 Total Orders", total_orders)

with col3:
    st.metric("💰 Avg Spending", f"${avg_spending:,.0f}")

with col4:
    st.metric("🏆 Top Customer", top_customer)

# ==========================
# Top 10 Customers by Orders
# ==========================
top_orders = (
    filtered_df
    .groupby("Customer ID")["Order ID"]
    .nunique()
    .sort_values(ascending=False)
    .head(10)
    .reset_index(name="Number of Orders")
)

fig1 = px.bar(
    top_orders,
    x="Customer ID",
    y="Number of Orders",
    color="Number of Orders",
    text_auto=True,
    color_continuous_scale="Oranges"
)

fig1.update_layout(
    title="Top 10 Customers by Number of Orders",
    xaxis_title="Customer ID",
    yaxis_title="Orders",
    coloraxis_showscale=False
)

# ==========================
# Top 10 Customers by Spending
# ==========================
top_spending = (
    filtered_df
    .groupby("Customer ID")["Total price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index(name="Total Spending")
)

fig2 = px.bar(
    top_spending,
    x="Customer ID",
    y="Total Spending",
    color="Total Spending",
    text_auto=".2s",
    color_continuous_scale="Blues"
)

fig2.update_layout(
    title="Top 10 Customers by Total Spending",
    xaxis_title="Customer ID",
    yaxis_title="Total Spending ($)",
    coloraxis_showscale=False
)

# ==========================
# Display Charts
# ==========================
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)