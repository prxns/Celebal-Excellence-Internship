# CELEBAL Week-3 Assignment

## SQL Sales Analysis using Subqueries, CTEs & Window Functions

## Project Overview

This project analyzes the Sample Superstore dataset using MySQL by applying advanced SQL concepts such as Subqueries, Common Table Expressions (CTEs), Window Functions, JOINs, and Aggregate Functions.

The objective is to transform raw sales data into a normalized database structure and answer real-world business questions through SQL queries.

---

## Objectives

- Import and normalize the Superstore dataset
- Create relational tables for Customers, Orders, and Products
- Eliminate duplicate records using SELECT DISTINCT and INSERT IGNORE
- Analyze sales data using:
  - Subqueries
  - Common Table Expressions (CTEs)
  - Window Functions
  - JOIN operations
- Generate customer sales insights

---

## Technologies Used

- MySQL 8.0
- MySQL Workbench
- Visual Studio Code
- Git & GitHub

---

## Dataset

Dataset Used:
- Sample Superstore Dataset

The dataset contains information about:

- Orders
- Customers
- Products
- Sales
- Quantity
- Discount
- Profit
- Shipping Information
- Regional Information

---

## Database Design

The raw dataset was normalized into three relational tables.

### Customers

| Column |
|---------|
| Customer_ID |
| Customer_Name |
| Segment |

---

### Products

| Column |
|---------|
| Product_ID |
| Category |
| Sub_Category |
| Product_Name |

---

### Orders

| Column |
|---------|
| Row_ID |
| Order_ID |
| Order_Date |
| Ship_Date |
| Ship_Mode |
| Customer_ID |
| Product_ID |
| Sales |
| Quantity |
| Discount |
| Profit |

Foreign Keys

- Customer_ID → customers
- Product_ID → products

---

## Data Preparation

The following preprocessing steps were performed before analysis:

- Imported the Sample Superstore dataset into `superstore_raw`
- Converted string dates into MySQL DATE format using `STR_TO_DATE()`
- Inserted unique customer records using `SELECT DISTINCT`
- Inserted unique products using `GROUP BY Product_ID`
- Used `INSERT IGNORE` to prevent duplicate insertions
- Established relationships using foreign keys

---

## SQL Concepts Implemented

### Subqueries

- Orders with above-average sales
- Highest sales line item for each customer

### Common Table Expressions (CTEs)

- Customer total sales
- Above-average customers

### Window Functions

- RANK()
- ROW_NUMBER()
- PARTITION BY

### Aggregate Functions

- SUM()
- AVG()
- MAX()
- COUNT()

### JOIN Operations

- INNER JOIN
- JOIN + CTE + Window Functions

---

## Business Questions Solved

- Orders with sales above the average
- Highest sales line item per customer
- Total sales for each customer
- Customers with above-average sales
- Rank customers by total sales
- Assign row numbers to customer orders
- Top 3 customers by revenue
- Top 5 customers
- Bottom 5 customers
- Customers with only one unique order
- Highest order value for each customer

---

## Project Structure

```
week3-sql-analysis/
│
├── queries.sql
├── README.md
├── results
├── insights.md
└── Sample - Superstore.csv
```

---

## Learning Outcomes

This project helped strengthen practical SQL skills by learning how to:

- Normalize raw datasets
- Create relational database schemas
- Work with foreign keys
- Write correlated subqueries
- Build reusable CTEs
- Apply Window Functions for ranking
- Perform analytical reporting using SQL
- Solve real-world business problems through data analysis

---

## Author

**Pranshu Rawat**

B.Tech Computer Science Engineering

DIT University