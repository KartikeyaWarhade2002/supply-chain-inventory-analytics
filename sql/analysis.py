import sqlite3
import pandas as pd

# =====================================================
# Database Connection
# =====================================================

DATABASE = "data/supply_chain.db"

conn = sqlite3.connect(DATABASE)

print("=" * 100)
print("SUPPLY CHAIN & INVENTORY ANALYSIS")
print("=" * 100)

# =====================================================
# Query 1
# Overall Supply Chain KPIs
# =====================================================

query_1 = """
SELECT

COUNT(DISTINCT order_id) AS total_orders,

COUNT(DISTINCT customer_id) AS total_customers,

ROUND(SUM(order_total),2) AS total_revenue,

ROUND(SUM(profit),2) AS total_profit,

ROUND(
100.0 * SUM(profit) / SUM(order_total),
2
) AS overall_profit_margin

FROM supply_chain;
"""

df = pd.read_sql(query_1, conn)

print("\nOVERALL SUPPLY CHAIN PERFORMANCE")
print("-"*80)
print(df)

# =====================================================
# Query 2
# Revenue by Category
# =====================================================

query_2 = """
SELECT

category,

COUNT(DISTINCT order_id) AS orders,

ROUND(SUM(order_total),2) AS revenue,

ROUND(SUM(profit),2) AS profit

FROM supply_chain

GROUP BY category

ORDER BY revenue DESC

LIMIT 10;
"""

df = pd.read_sql(query_2, conn)

print("\nTOP 10 PRODUCT CATEGORIES")
print("-"*80)
print(df)

# =====================================================
# Query 3
# Revenue by Market
# =====================================================

query_3 = """
SELECT

market,

COUNT(DISTINCT order_id) AS orders,

ROUND(SUM(order_total),2) AS revenue,

ROUND(SUM(profit),2) AS profit,

ROUND(
100.0 * SUM(profit) / SUM(order_total),
2
) AS overall_profit_margin

FROM supply_chain

GROUP BY market

ORDER BY revenue DESC;
"""

df = pd.read_sql(query_3, conn)

print("\nMARKET PERFORMANCE")
print("-"*80)
print(df)

# =====================================================
# Query 4
# Shipping Mode Performance
# =====================================================

query_4 = """
SELECT

shipping_mode,

COUNT(DISTINCT order_id) AS orders,

ROUND(SUM(order_total),2) AS revenue,

ROUND(SUM(profit),2) AS profit,

ROUND(AVG(shipping_days),2) AS average_shipping_days,

ROUND(100.0*AVG(late_delivery),2) AS late_delivery_rate

FROM supply_chain

GROUP BY shipping_mode

ORDER BY revenue DESC;
"""

df = pd.read_sql(query_4, conn)

print("\nSHIPPING MODE PERFORMANCE")
print("-"*80)
print(df)

# =====================================================
# Query 5
# Monthly Revenue Trend
# =====================================================

query_5 = """
SELECT

order_month_number,

order_month_name,

COUNT(DISTINCT order_id) AS orders,

ROUND(SUM(order_total),2) AS revenue,

ROUND(SUM(profit),2) AS profit

FROM supply_chain

GROUP BY
order_month_number,
order_month_name

ORDER BY
order_month_number;
"""

df = pd.read_sql(query_5, conn)

print("\nMONTHLY REVENUE TREND")
print("-"*80)
print(df)

# =====================================================
# Query 6
# Shipping Performance
# =====================================================

query_6 = """
SELECT

shipping_performance,

COUNT(DISTINCT order_id) AS orders,

ROUND(SUM(order_total),2) AS revenue,

ROUND(SUM(profit),2) AS profit,

ROUND(AVG(shipping_days),2) AS average_shipping_days

FROM supply_chain

GROUP BY shipping_performance

ORDER BY revenue DESC;
"""

df = pd.read_sql(query_6, conn)

print("\nSHIPPING PERFORMANCE")
print("-"*80)
print(df)

# =====================================================
# Query 7
# Customer Segment Performance
# =====================================================

query_7 = """
SELECT

customer_segment,

COUNT(DISTINCT customer_id) AS customers,

COUNT(DISTINCT order_id) AS orders,

ROUND(SUM(order_total),2) AS revenue,

ROUND(SUM(profit),2) AS profit,

ROUND(AVG(order_total),2) AS average_order_value

FROM supply_chain

GROUP BY customer_segment

ORDER BY revenue DESC;
"""

df = pd.read_sql(query_7, conn)

print("\nCUSTOMER SEGMENT PERFORMANCE")
print("-"*80)
print(df)

# =====================================================
# Query 8
# Top 10 Products
# =====================================================

query_8 = """
SELECT

product_name,

SUM(quantity) AS quantity_sold,

ROUND(SUM(order_total),2) AS revenue,

ROUND(SUM(profit),2) AS profit

FROM supply_chain

GROUP BY product_name

ORDER BY revenue DESC

LIMIT 10;
"""

df = pd.read_sql(query_8, conn)

print("\nTOP 10 PRODUCTS")
print("-"*80)
print(df)

# =====================================================
# Finish
# =====================================================

print("\nAnalysis Complete.")

conn.close()