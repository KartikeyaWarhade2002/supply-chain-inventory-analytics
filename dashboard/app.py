"""
Supply Chain & Inventory Analytics Dashboard
Built with Streamlit
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Supply Chain & Inventory Analytics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "supply_chain_clean.csv"
)

# =====================================================
# Load Data
# =====================================================

@st.cache_data(show_spinner="Loading dataset...")
def load_data(path: Path):

    df = pd.read_csv(path)

    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(
            df["order_date"],
            errors="coerce"
        )

    if "shipping_date" in df.columns:
        df["shipping_date"] = pd.to_datetime(
            df["shipping_date"],
            errors="coerce"
        )

    return df


if not DATA_FILE.exists():

    st.error(
        f"""
Dataset not found.

Expected:

{DATA_FILE}

Place supply_chain_clean.csv inside:

data/processed/
"""
    )

    st.stop()

df = load_data(DATA_FILE)

# =====================================================
# Sidebar Filters
# =====================================================

st.sidebar.title("📦 Dashboard Filters")

selected_market = st.sidebar.multiselect(
    "Market",
    sorted(df["market"].dropna().unique()),
    default=sorted(df["market"].dropna().unique()),
)

selected_department = st.sidebar.multiselect(
    "Department",
    sorted(df["department"].dropna().unique()),
    default=sorted(df["department"].dropna().unique()),
)

selected_shipping = st.sidebar.multiselect(
    "Shipping Performance",
    sorted(df["shipping_performance"].dropna().unique()),
    default=sorted(df["shipping_performance"].dropna().unique()),
)

selected_status = st.sidebar.multiselect(
    "Order Status",
    sorted(df["order_status"].dropna().unique()),
    default=sorted(df["order_status"].dropna().unique()),
)

year_options = sorted(df["order_year"].dropna().unique())

selected_year = st.sidebar.multiselect(
    "Order Year",
    year_options,
    default=year_options,
)

df = df[
    (df["market"].isin(selected_market))
    &
    (df["department"].isin(selected_department))
    &
    (df["shipping_performance"].isin(selected_shipping))
    &
    (df["order_status"].isin(selected_status))
    &
    (df["order_year"].isin(selected_year))
]

if df.empty:

    st.warning(
        "No records match the selected filters."
    )

    st.stop()

# =====================================================
# KPI Calculations
# =====================================================

total_orders = df["order_id"].nunique()

total_sales = df["sales"].sum()

total_profit = df["profit"].sum()

total_customers = df["customer_id"].nunique()

average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)

average_shipping_days = (
    df["shipping_days"].mean()
)

late_shipments = (
    (
        df["shipping_performance"] == "Late"
    ).sum()
)

late_percentage = (
    late_shipments /
    len(df)
    * 100
    if len(df) > 0
    else 0
)

# =====================================================
# Dashboard Header
# =====================================================

st.title("📦 Supply Chain & Inventory Analytics")

st.caption(
    "Interactive Supply Chain Dashboard built using Python, Pandas, Plotly and Streamlit"
)

# =====================================================
# KPI Cards
# =====================================================

k1, k2, k3 = st.columns(3)

k4, k5, k6 = st.columns(3)

k1.metric(
    "Total Sales",
    f"${total_sales:,.0f}"
)

k2.metric(
    "Total Orders",
    f"{total_orders:,}"
)

k3.metric(
    "Total Profit",
    f"${total_profit:,.0f}"
)

k4.metric(
    "Customers",
    f"{total_customers:,}"
)

k5.metric(
    "Average Order Value",
    f"${average_order_value:,.2f}"
)

k6.metric(
    "Late Shipments",
    f"{late_percentage:.1f}%"
)

st.divider()

# =====================================================
# Dashboard Tabs
# =====================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "📊 Executive Overview",
        "📦 Inventory",
        "🚚 Shipping",
        "🌍 Markets",
        "💰 Sales & Profit",
        "📄 Raw Data",
    ]
)

# =====================================================
# Executive Overview
# =====================================================

with tab1:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Sales by Year")

        yearly = (
            df.groupby("order_year")
            .agg(
                Sales=("sales", "sum")
            )
            .reset_index()
        )

        fig = px.bar(
            yearly,
            x="order_year",
            y="Sales",
            color="order_year",
            title="Sales by Year"
        )

        fig.update_layout(
            template="plotly_white",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("Shipping Performance")

        shipping = (
            df.groupby("shipping_performance")
            .size()
            .reset_index(name="Orders")
        )

        fig = px.pie(
            shipping,
            names="shipping_performance",
            values="Orders",
            hole=0.45,
            title="Shipping Performance"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Monthly Sales Trend")

    monthly = (
        df.groupby("order_month_name")
        .agg(
            Sales=("sales", "sum")
        )
        .reset_index()
    )

    month_order = [
        "January","February","March","April",
        "May","June","July","August",
        "September","October","November","December"
    ]

    monthly["order_month_name"] = pd.Categorical(
        monthly["order_month_name"],
        categories=month_order,
        ordered=True
    )

    monthly = monthly.sort_values("order_month_name")

    fig = px.line(
        monthly,
        x="order_month_name",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Order Status")

    status = (
        df.groupby("order_status")
        .size()
        .reset_index(name="Orders")
    )

    fig = px.bar(
        status,
        x="order_status",
        y="Orders",
        color="order_status",
        title="Orders by Status"
    )

    fig.update_layout(
        template="plotly_white",
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# Inventory
# =====================================================

with tab2:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Sales by Category")

        category_sales = (
            df.groupby("category")
            .agg(
                Sales=("sales", "sum")
            )
            .sort_values("Sales", ascending=False)
            .head(15)
            .reset_index()
        )

        fig = px.bar(
            category_sales,
            x="Sales",
            y="category",
            orientation="h",
            color="Sales",
            title="Top Categories by Sales"
        )

        fig.update_layout(
            template="plotly_white",
            yaxis={"categoryorder": "total ascending"},
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("Profit by Category")

        category_profit = (
            df.groupby("category")
            .agg(
                Profit=("profit", "sum")
            )
            .sort_values("Profit", ascending=False)
            .head(15)
            .reset_index()
        )

        fig = px.bar(
            category_profit,
            x="Profit",
            y="category",
            orientation="h",
            color="Profit",
            title="Top Categories by Profit"
        )

        fig.update_layout(
            template="plotly_white",
            yaxis={"categoryorder": "total ascending"},
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Inventory by Category")

    inventory = (
        df.groupby("category")
        .agg(
            Inventory=("quantity", "sum")
        )
        .sort_values("Inventory", ascending=False)
        .head(20)
        .reset_index()
    )

    fig = px.bar(
        inventory,
        x="category",
        y="Inventory",
        color="Inventory",
        title="Inventory Distribution"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_tickangle=-45,
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Top Products by Sales")

    products = (
        df.groupby("product_name")
        .agg(
            Sales=("sales", "sum")
        )
        .sort_values("Sales", ascending=False)
        .head(15)
        .reset_index()
    )

    fig = px.bar(
        products,
        x="Sales",
        y="product_name",
        orientation="h",
        color="Sales",
        title="Best Selling Products"
    )

    fig.update_layout(
        template="plotly_white",
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# Shipping
# =====================================================

with tab3:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Shipping Performance")

        shipping = (
            df.groupby("shipping_performance")
            .size()
            .reset_index(name="Orders")
        )

        fig = px.pie(
            shipping,
            names="shipping_performance",
            values="Orders",
            hole=0.45,
            title="On-Time vs Late Deliveries"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("Shipping Mode")

        mode = (
            df.groupby("shipping_mode")
            .size()
            .reset_index(name="Orders")
        )

        fig = px.bar(
            mode,
            x="shipping_mode",
            y="Orders",
            color="shipping_mode",
            title="Orders by Shipping Mode"
        )

        fig.update_layout(
            template="plotly_white",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Average Shipping Days")

    shipping_summary = (
    df.groupby("shipping_mode")
    .agg(
        Average_Days=("shipping_days", "mean")
    )
    .reset_index()
    )

    fig = px.bar(
    shipping_summary,
    x="shipping_mode",
    y="Average_Days",
    color="Average_Days",
    title="Average Shipping Days by Mode"
    )

    fig.update_layout(
    template="plotly_white",
    coloraxis_showscale=False
    )

    st.plotly_chart(
    fig,
    use_container_width=True
   )
    st.subheader("Late Delivery Distribution")

    fig = px.histogram(
        df,
        x="late_delivery_risk",
        color="shipping_performance",
        nbins=25,
        title="Late Delivery Risk Distribution"
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
    # =====================================================
# Market Analysis
# =====================================================

with tab4:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Sales by Market")

        market_sales = (
            df.groupby("market")
            .agg(
                Sales=("sales", "sum")
            )
            .reset_index()
            .sort_values("Sales", ascending=False)
        )

        fig = px.bar(
            market_sales,
            x="market",
            y="Sales",
            color="Sales",
            title="Sales by Market"
        )

        fig.update_layout(
            template="plotly_white",
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("Profit by Market")

        market_profit = (
            df.groupby("market")
            .agg(
                Profit=("profit", "sum")
            )
            .reset_index()
            .sort_values("Profit", ascending=False)
        )

        fig = px.bar(
            market_profit,
            x="market",
            y="Profit",
            color="Profit",
            title="Profit by Market"
        )

        fig.update_layout(
            template="plotly_white",
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Sales vs Profit")

    compare = (
        df.groupby("market")
        .agg(
            Sales=("sales","sum"),
            Profit=("profit","sum")
        )
        .reset_index()
    )

    fig = px.scatter(
        compare,
        x="Sales",
        y="Profit",
        size="Sales",
        color="market",
        hover_name="market",
        title="Sales vs Profit by Market"
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
# =====================================================
# Sales & Profit
# =====================================================

with tab5:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Sales by Department")

        sales_dept = (
            df.groupby("department")
            .agg(Sales=("sales", "sum"))
            .reset_index()
            .sort_values("Sales", ascending=False)
        )

        fig = px.bar(
            sales_dept,
            x="department",
            y="Sales",
            color="Sales",
            title="Sales by Department",
        )

        fig.update_layout(
            template="plotly_white",
            coloraxis_showscale=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with col2:

        st.subheader("Profit by Department")

        profit_dept = (
            df.groupby("department")
            .agg(Profit=("profit", "sum"))
            .reset_index()
            .sort_values("Profit", ascending=False)
        )

        fig = px.bar(
            profit_dept,
            x="department",
            y="Profit",
            color="Profit",
            title="Profit by Department",
        )

        fig.update_layout(
            template="plotly_white",
            coloraxis_showscale=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.subheader("Profit Margin by Market")

    margin = (
        df.groupby("market")
        .agg(Profit_Margin=("profit_margin", "mean"))
        .reset_index()
    )

    fig = px.bar(
        margin,
        x="market",
        y="Profit_Margin",
        color="Profit_Margin",
        title="Average Profit Margin by Market",
    )

    fig.update_layout(
        template="plotly_white",
        coloraxis_showscale=False,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )
    
# =====================================================
# Raw Data
# =====================================================

with tab6:

    st.subheader("Filtered Dataset")

    st.dataframe(
        df,
        use_container_width=True,
        height=600,
    )

    @st.cache_data
    def convert_csv(dataframe):
        return dataframe.to_csv(index=False).encode("utf-8")

    csv = convert_csv(df)

    st.download_button(
        "⬇ Download Filtered Data",
        csv,
        "filtered_supply_chain.csv",
        "text/csv",
    )