# KPI Definitions

## Table Grain

**1 Row = 1 Customer Order**

---

## Total Orders

**Definition**

COUNT(DISTINCT order_id)

---

## Total Customers

**Definition**

COUNT(DISTINCT customer_id)

---

## Total Revenue

**Definition**

SUM(order_total)

---

## Total Profit

**Definition**

SUM(profit)

---

## Overall Profit Margin

**Definition**

Total Profit
/
Total Revenue

× 100

---

## Average Order Value (AOV)

**Definition**

Total Revenue
/
Total Orders

---

## Revenue by Product Category

**Definition**

SUM(order_total)

GROUP BY category

---

## Profit by Market

**Definition**

SUM(profit)

GROUP BY market

---

## Shipping Mode Performance

**Definition**

Revenue, Profit, Average Shipping Days and Late Delivery Rate grouped by Shipping Mode.

---

## Monthly Revenue Trend

**Definition**

Monthly Revenue and Profit grouped by Order Month.

---

## Shipping Performance

**Definition**

Revenue, Profit and Average Shipping Days grouped by Shipping Performance (Early, On Time and Late).

---

## Customer Segment Performance

**Definition**

Revenue, Profit and Average Order Value grouped by Customer Segment.

---

## Top Products

**Definition**

Revenue, Profit and Quantity Sold grouped by Product Name.
