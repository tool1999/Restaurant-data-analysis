import streamlit as st

st.set_page_config(
    page_title="Restaurant Sales Dashboard",
    page_icon="🍔",
    layout="wide"
)

st.title("🍔 Restaurant Sales Dashboard")

st.markdown("""
# Restaurant Sales Analysis (2022–2023)

Welcome!

This interactive dashboard provides comprehensive insights into restaurant sales data collected during 2022 and 2023.

### 📊 Dashboard Sections

- 📈 Sales Performance
- 🍕 Product Analysis
- 👥 Customer Analysis
- 💳 Payment Analysis
- 📅 Time Analysis

👈 Use the **sidebar** to navigate between dashboard pages.
""")