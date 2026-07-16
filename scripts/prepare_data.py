import sqlite3
from pathlib import Path

import pandas as pd

print("=" * 100)
print("SUPPLY CHAIN ETL")
print("=" * 100)

# =====================================================
# Paths
# =====================================================

RAW_DATA = Path("data/raw/DataCoSupplyChainDataset.csv")
PROCESSED_DATA = Path("data/processed/supply_chain_clean.csv")
DATABASE = Path("data/supply_chain.db")

PROCESSED_DATA.parent.mkdir(parents=True, exist_ok=True)

# =====================================================
# Load Dataset
# =====================================================

df = pd.read_csv(
    RAW_DATA,
    encoding="latin1"
)

# =====================================================
# Remove Unnecessary Columns
# =====================================================

columns_to_drop = [
    "Product Description",
    "Order Zipcode",
    "Customer Email",
    "Customer Password",
    "Product Status"
]

df.drop(
    columns=columns_to_drop,
    inplace=True,
    errors="ignore"
)

# =====================================================
# Rename Columns
# =====================================================

df.rename(columns={

    "Type":"payment_type",
    "Days for shipping (real)":"shipping_days",
    "Days for shipment (scheduled)":"scheduled_shipping_days",
    "Benefit per order":"benefit_per_order",
    "Sales per customer":"sales_per_customer",
    "Delivery Status":"delivery_status",
    "Late_delivery_risk":"late_delivery_risk",

    "Category Id":"category_id",
    "Category Name":"category",

    "Customer City":"customer_city",
    "Customer Country":"customer_country",
    "Customer Fname":"customer_first_name",
    "Customer Id":"customer_id",
    "Customer Lname":"customer_last_name",
    "Customer Segment":"customer_segment",
    "Customer State":"customer_state",
    "Customer Street":"customer_street",
    "Customer Zipcode":"customer_zipcode",

    "Department Id":"department_id",
    "Department Name":"department",

    "Latitude":"latitude",
    "Longitude":"longitude",

    "Market":"market",

    "Order City":"order_city",
    "Order Country":"order_country",
    "Order Customer Id":"order_customer_id",

    "order date (DateOrders)":"order_date",

    "Order Id":"order_id",

    "Order Item Cardprod Id":"product_card_id",
    "Order Item Discount":"discount",
    "Order Item Discount Rate":"discount_rate",
    "Order Item Id":"order_item_id",
    "Order Item Product Price":"product_price",
    "Order Item Profit Ratio":"profit_ratio",
    "Order Item Quantity":"quantity",

    "Sales":"sales",
    "Order Item Total":"order_total",
    "Order Profit Per Order":"profit",

    "Order Region":"order_region",
    "Order State":"order_state",
    "Order Status":"order_status",

    "Product Card Id":"product_card_id_master",
    "Product Category Id":"product_category_id",
    "Product Image":"product_image",
    "Product Name":"product_name",
    "Product Price":"catalog_price",

    "shipping date (DateOrders)":"shipping_date",

    "Shipping Mode":"shipping_mode"

}, inplace=True)

# =====================================================
# Remove Duplicate Product ID
# =====================================================

df.drop(
    columns=["product_card_id_master"],
    inplace=True,
    errors="ignore"
)

# =====================================================
# Missing Values
# =====================================================

df["customer_last_name"] = df["customer_last_name"].fillna("Unknown")

df["customer_zipcode"] = (
    df["customer_zipcode"]
    .fillna(df["customer_zipcode"].median())
    .astype(int)
)

# =====================================================
# Date Features
# =====================================================

df["order_date"] = pd.to_datetime(df["order_date"])

df["shipping_date"] = pd.to_datetime(df["shipping_date"])

df["order_year"] = df["order_date"].dt.year

df["order_month_number"] = df["order_date"].dt.month

df["order_month_name"] = df["order_date"].dt.strftime("%B")

df["order_quarter"] = df["order_date"].dt.quarter

df["order_day"] = df["order_date"].dt.day

df["order_day_name"] = df["order_date"].dt.day_name()

df["is_weekend"] = (
    df["order_date"]
      .dt.dayofweek
      .isin([5, 6])
      .astype(int)
)

# =====================================================
# Feature Engineering
# =====================================================

df["shipping_delay"] = (
    df["shipping_days"] -
    df["scheduled_shipping_days"]
)

df["late_delivery"] = (
    df["shipping_delay"] > 0
).astype(int)

df["shipping_performance"] = df["shipping_delay"].apply(
    lambda x: "Early" if x < 0 else ("On Time" if x == 0 else "Late")
)

df["profit_margin"] = (
    df["profit"] / df["sales"]
).fillna(0)

# =====================================================
# Round Numeric Columns
# =====================================================

float_columns = [
    "benefit_per_order",
    "sales_per_customer",
    "discount",
    "discount_rate",
    "product_price",
    "profit_ratio",
    "sales",
    "order_total",
    "profit",
    "catalog_price",
    "profit_margin"
]

df[float_columns] = df[float_columns].round(2)

# =====================================================
# Save Clean CSV
# =====================================================

df.to_csv(
    PROCESSED_DATA,
    index=False
)

# =====================================================
# SQLite Database
# =====================================================

conn = sqlite3.connect(DATABASE)

df.to_sql(
    "supply_chain",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

# =====================================================
# Summary
# =====================================================

print("\nDataset Summary")
print("-" * 40)

print(f"Rows                 : {len(df):,}")
print(f"Columns              : {len(df.columns)}")
print(f"Orders               : {df['order_id'].nunique():,}")
print(f"Customers            : {df['customer_id'].nunique():,}")
print(f"Unique Products      : {df['product_name'].nunique():,}")
print(f"Markets              : {df['market'].nunique()}")
print(f"Categories           : {df['category'].nunique()}")

print("\nMissing Values")
print("-" * 40)

print(df.isna().sum())

print("\nFiles Created")
print("-" * 40)

print(PROCESSED_DATA)
print(DATABASE)

print("\nETL Completed Successfully.")