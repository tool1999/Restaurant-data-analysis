import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# Page Config
# ==========================
st.set_page_config(
    page_title="Restaurant Sales Dashboard",
    page_icon="🍔",
    layout="wide"
)

# ==========================
# Title
# ==========================
st.title("🍔 Restaurant Sales Dashboard")
st.markdown("### Sales Analysis Dashboard")

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

# ==========================
# مكان فاضي للـ KPIs
# ==========================
kpi_container = st.container()

# مكان فاضي للـ Slider
slider_container = st.container()

# ==========================
# Month Slider
# ==========================
with slider_container:

    st.subheader("📅 Select Month")

    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        "All Year"
    ]

    selected_month = st.select_slider(
        "",
        options=months,
        value="All Year"
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

# ==========================
# KPIs
# ==========================
total_sales = filtered_df["Total price"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()
total_items = filtered_df["Item"].nunique()
avg_order = total_sales / total_orders if total_orders > 0 else 0
# ==========================
# Display KPIs
# ==========================
with kpi_container:

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("💰 Total Sales", f"${total_sales:,.0f}")

    with col2:
        st.metric("📦 Orders", total_orders)

    with col3:
        st.metric("👥 Customers", total_customers)

    with col4:
        st.metric("🍔 Items", total_items)
    with col5:
        st.metric("🧾 Avg Order", f"${avg_order:,.2f}")
# ==========================
# Sales Chart
# ==========================
st.divider()
st.subheader("📈 Sales Overview")

if selected_month == "All Year":

    chart_data = (
        filtered_df
        .groupby(filtered_df["Order Date"].dt.month_name())["Total price"]
        .sum()
        .reset_index()
    )

    month_order = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    chart_data["Order Date"] = pd.Categorical(
        chart_data["Order Date"],
        categories=month_order,
        ordered=True
    )

    chart_data = chart_data.sort_values("Order Date")

    fig = px.bar(
        chart_data,
        x="Order Date",
        y="Total price",
        color="Total price",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Sales ($)",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)
    st.divider()

    

else:

    chart_data = (
        filtered_df
        .groupby(filtered_df["Order Date"].dt.day)["Total price"]
        .sum()
        .reset_index(name="Sales")
    )

    fig = px.line(
        chart_data,
        x="Order Date",
        y="Sales",
        markers=True
    )

    fig.update_layout(
        title=f"Daily Sales - {selected_month}",
        xaxis_title="Day",
        yaxis_title="Sales ($)"
    )

    st.plotly_chart(fig, use_container_width=True)