import streamlit as st
import pandas as pd
import numpy as np

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Sales KPI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Advanced Sales KPI Dashboard")
st.markdown("Interactive KPI dashboard with multiple filters and insights.")

# --------------------------------------------------
# GENERATE SAMPLE DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    np.random.seed(42)

    dates = pd.date_range("2024-01-01", "2025-12-31")

    data = pd.DataFrame({
        "Order Date": np.random.choice(dates, 3000),
        "Region": np.random.choice(
            ["North", "South", "East", "West"], 3000
        ),
        "Category": np.random.choice(
            ["Furniture", "Technology", "Office Supplies"], 3000
        ),
        "Sub-Category": np.random.choice(
            ["Chairs", "Tables", "Phones", "Accessories", "Paper", "Storage"], 3000
        ),
        "Segment": np.random.choice(
            ["Consumer", "Corporate", "Home Office"], 3000
        ),
        "Ship Mode": np.random.choice(
            ["Standard", "Second Class", "First Class", "Same Day"], 3000
        ),
        "Product Name": np.random.choice(
            ["Laptop", "Phone", "Chair", "Table", "Notebook", "Printer"], 3000
        ),
        "Sales": np.random.randint(100, 5000, 3000),
        "Profit": np.random.randint(-500, 1500, 3000),
        "Quantity": np.random.randint(1, 15, 3000),
        "Discount": np.round(np.random.uniform(0, 0.50, 3000), 2)
    })

    data["Order Date"] = pd.to_datetime(data["Order Date"])
    return data

df = load_data()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("🔍 Dashboard Filters")

# Date Range
start_date = st.sidebar.date_input(
    "Start Date",
    df["Order Date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Order Date"].max()
)

df = df[
    (df["Order Date"] >= pd.to_datetime(start_date)) &
    (df["Order Date"] <= pd.to_datetime(end_date))
]

# Region Filter
region = st.sidebar.multiselect(
    "Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

# Category Filter
category = st.sidebar.multiselect(
    "Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Sub Category Filter
sub_category = st.sidebar.multiselect(
    "Sub-Category",
    options=df["Sub-Category"].unique(),
    default=df["Sub-Category"].unique()
)

# Segment Filter
segment = st.sidebar.multiselect(
    "Segment",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)

# Ship Mode Filter
ship_mode = st.sidebar.multiselect(
    "Ship Mode",
    options=df["Ship Mode"].unique(),
    default=df["Ship Mode"].unique()
)

# Apply Filters
df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Sub-Category"].isin(sub_category)) &
    (df["Segment"].isin(segment)) &
    (df["Ship Mode"].isin(ship_mode))
]

# Sales Filter
sales_range = st.sidebar.slider(
    "Sales Range",
    int(df["Sales"].min()),
    int(df["Sales"].max()),
    (
        int(df["Sales"].min()),
        int(df["Sales"].max())
    )
)

df = df[
    (df["Sales"] >= sales_range[0]) &
    (df["Sales"] <= sales_range[1])
]

# Profit Filter
profit_range = st.sidebar.slider(
    "Profit Range",
    int(df["Profit"].min()),
    int(df["Profit"].max()),
    (
        int(df["Profit"].min()),
        int(df["Profit"].max())
    )
)

df = df[
    (df["Profit"] >= profit_range[0]) &
    (df["Profit"] <= profit_range[1])
]

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = len(df)
total_quantity = df["Quantity"].sum()

avg_order_value = (
    total_sales / total_orders
    if total_orders > 0 else 0
)

profit_margin = (
    total_profit / total_sales * 100
    if total_sales > 0 else 0
)

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
st.subheader("📌 Key Performance Indicators")

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("💰 Total Sales", f"${total_sales:,.0f}")
k2.metric("📈 Total Profit", f"${total_profit:,.0f}")
k3.metric("🛒 Orders", f"{total_orders:,}")
k4.metric("📦 Quantity", f"{total_quantity:,}")
k5.metric("📊 Margin", f"{profit_margin:.2f}%")

st.divider()

# --------------------------------------------------
# SALES TREND
# --------------------------------------------------
st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

st.line_chart(monthly_sales)

# --------------------------------------------------
# CHARTS
# --------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("🏷 Category Sales")
    st.bar_chart(
        df.groupby("Category")["Sales"].sum()
    )

with c2:
    st.subheader("🌍 Region Sales")
    st.bar_chart(
        df.groupby("Region")["Sales"].sum()
    )

# --------------------------------------------------
# SECOND ROW
# --------------------------------------------------
c3, c4 = st.columns(2)

with c3:
    st.subheader("👥 Segment Sales")
    st.bar_chart(
        df.groupby("Segment")["Sales"].sum()
    )

with c4:
    st.subheader("🚚 Ship Mode Sales")
    st.bar_chart(
        df.groupby("Ship Mode")["Sales"].sum()
    )

# --------------------------------------------------
# TOP PRODUCTS
# --------------------------------------------------
st.subheader("🏆 Top 10 Products")

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(top_products)

# --------------------------------------------------
# PROFIT VS SALES
# --------------------------------------------------
st.subheader("📉 Profit vs Sales")

scatter_data = df[["Sales", "Profit"]]

st.scatter_chart(scatter_data)

# --------------------------------------------------
# MONTHLY PROFIT
# --------------------------------------------------
st.subheader("📈 Monthly Profit Trend")

monthly_profit = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Profit"]
    .sum()
)

monthly_profit.index = monthly_profit.index.astype(str)

st.line_chart(monthly_profit)

# --------------------------------------------------
# RAW DATA
# --------------------------------------------------
with st.expander("📋 View Dataset"):
    st.dataframe(df, use_container_width=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.success("Dashboard Loaded Successfully ✅")