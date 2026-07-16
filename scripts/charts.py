import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px

# =====================================================
# PATHS
# =====================================================

DATABASE = "data/supply_chain.db"

CHARTS = Path("charts")
CHARTS.mkdir(exist_ok=True)

# =====================================================
# DATABASE CONNECTION
# =====================================================

conn = sqlite3.connect(DATABASE)

print("=" * 70)
print("CREATING PLOTLY CHARTS")
print("=" * 70)

# =====================================================
# GLOBAL STYLING FUNCTION
# =====================================================

def style_chart(
    fig,
    title,
    x_title,
    y_title,
    currency=False,
    rotate_labels=False
):

    fig.update_layout(

        template="plotly_white",

        title=dict(
            text=title,
            x=0.5,
            xanchor="center",
            font=dict(size=24)
        ),

        font=dict(
            family="Arial",
            size=15
        ),

        xaxis_title=x_title,

        yaxis_title=y_title,

        xaxis_title_font=dict(size=18),

        yaxis_title_font=dict(size=18),

        xaxis_tickfont=dict(size=13),

        yaxis_tickfont=dict(size=13),

        bargap=0.25,

        margin=dict(
            l=70,
            r=40,
            t=80,
            b=70
        )

    )

    if rotate_labels:

        fig.update_layout(

            xaxis_tickangle=-25

        )

    if currency:

        fig.update_yaxes(
            tickprefix="$"
        )

    return fig


# =====================================================
# CHART 1
# TOP 10 CATEGORIES BY REVENUE
# =====================================================

query = """

SELECT

category,

ROUND(
SUM(order_total),
2
) AS revenue

FROM supply_chain

GROUP BY category

ORDER BY revenue DESC

LIMIT 10;

"""

df = pd.read_sql(query, conn)

fig = px.bar(

    df,

    x="category",

    y="revenue",

    text="revenue"

)

fig.update_traces(

    texttemplate="$%{text:,.0f}",

    textposition="outside"

)

style_chart(

    fig,

    title="Top 10 Categories by Revenue",

    x_title="Category",

    y_title="Revenue",

    currency=True,

    rotate_labels=True

)

fig.write_image(

    CHARTS / "01_category_revenue.png",

    width=1400,

    height=800

)

# =====================================================
# CHART 2
# REVENUE BY MARKET
# =====================================================

query = """

SELECT

market,

ROUND(
SUM(order_total),
2
) AS revenue

FROM supply_chain

GROUP BY market

ORDER BY revenue DESC;

"""

df = pd.read_sql(query, conn)

fig = px.bar(

    df,

    x="market",

    y="revenue",

    text="revenue"

)

fig.update_traces(

    texttemplate="$%{text:,.0f}",

    textposition="outside"

)

style_chart(

    fig,

    title="Revenue by Market",

    x_title="Market",

    y_title="Revenue",

    currency=True

)

fig.write_image(

    CHARTS / "02_market_revenue.png",

    width=1400,

    height=800

)

# =====================================================
# CHART 3
# REVENUE BY SHIPPING MODE
# =====================================================

query = """

SELECT

shipping_mode,

ROUND(
SUM(order_total),
2
) AS revenue

FROM supply_chain

GROUP BY shipping_mode

ORDER BY revenue DESC;

"""

df = pd.read_sql(query, conn)

fig = px.bar(

    df,

    x="shipping_mode",

    y="revenue",

    text="revenue"

)

fig.update_traces(

    texttemplate="$%{text:,.0f}",

    textposition="outside"

)

style_chart(

    fig,

    title="Revenue by Shipping Mode",

    x_title="Shipping Mode",

    y_title="Revenue",

    currency=True

)

fig.write_image(

    CHARTS / "03_shipping_mode.png",

    width=1400,

    height=800

)

# =====================================================
# CHART 4
# MONTHLY REVENUE TREND
# =====================================================

query = """

SELECT

order_month_number,

order_month_name,

ROUND(
SUM(order_total),
2
) AS revenue

FROM supply_chain

GROUP BY
order_month_number,
order_month_name

ORDER BY
order_month_number;

"""

df = pd.read_sql(query, conn)

fig = px.line(

    df,

    x="order_month_name",

    y="revenue",

    markers=True

)

fig.update_traces(

    line=dict(width=4),

    marker=dict(size=8)

)

style_chart(

    fig,

    title="Monthly Revenue Trend",

    x_title="Month",

    y_title="Revenue",

    currency=True

)

fig.write_image(

    CHARTS / "04_monthly_revenue.png",

    width=1400,

    height=800

)

# =====================================================
# CHART 5
# LATE DELIVERY RATE BY SHIPPING MODE
# =====================================================

query = """

SELECT

shipping_mode,

ROUND(
100.0 * AVG(late_delivery),
2
) AS late_delivery_rate

FROM supply_chain

GROUP BY shipping_mode

ORDER BY late_delivery_rate DESC;

"""

df = pd.read_sql(query, conn)

fig = px.bar(

    df,

    x="shipping_mode",

    y="late_delivery_rate",

    text="late_delivery_rate"

)

fig.update_traces(

    texttemplate="%{text:.2f}%",

    textposition="outside"

)

style_chart(

    fig,

    title="Late Delivery Rate by Shipping Mode",

    x_title="Shipping Mode",

    y_title="Late Delivery Rate (%)"

)

fig.write_image(

    CHARTS / "05_shipping_performance.png",

    width=1400,

    height=800

)

# =====================================================
# CHART 6
# REVENUE BY CUSTOMER SEGMENT
# =====================================================

query = """

SELECT

customer_segment,

ROUND(
SUM(order_total),
2
) AS revenue

FROM supply_chain

GROUP BY customer_segment

ORDER BY revenue DESC;

"""

df = pd.read_sql(query, conn)

fig = px.bar(

    df,

    x="customer_segment",

    y="revenue",

    text="revenue"

)

fig.update_traces(

    texttemplate="$%{text:,.0f}",

    textposition="outside"

)

style_chart(

    fig,

    title="Revenue by Customer Segment",

    x_title="Customer Segment",

    y_title="Revenue",

    currency=True

)

fig.write_image(

    CHARTS / "06_customer_segment.png",

    width=1400,

    height=800

)

# =====================================================
# CLOSE DATABASE
# =====================================================

conn.close()

# =====================================================
# FINISH
# =====================================================

print("\n" + "=" * 70)
print("PLOTLY CHARTS CREATED SUCCESSFULLY")
print("=" * 70)

print("01_category_revenue.png")
print("02_market_revenue.png")
print("03_shipping_mode.png")
print("04_monthly_revenue.png")
print("05_shipping_performance.png")
print("06_customer_segment.png")