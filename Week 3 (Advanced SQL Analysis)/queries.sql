CREATE DATABASE IF NOT EXISTS superstore_db;

-- WEEK 3 ASSIGNMENT: SUPERSTORE SALES ANALYSIS

USE superstore_db;

-- 1. Setup Data (Normalization)

-- 1.1 Create Tables: Customers
CREATE TABLE IF NOT EXISTS customers (
    Customer_ID VARCHAR(50) PRIMARY KEY,
    Customer_Name VARCHAR(100),
    Segment VARCHAR(50)
);

-- 1.2 Create Tables: Products
CREATE TABLE IF NOT EXISTS products (
    Product_ID VARCHAR(50) PRIMARY KEY,
    Category VARCHAR(50),
    Sub_Category VARCHAR(50),
    Product_Name TEXT
);

-- 1.3 Create Tables: Orders
CREATE TABLE IF NOT EXISTS orders (
    Row_ID INT PRIMARY KEY,
    Order_ID VARCHAR(50),
    Order_Date DATE,
    Ship_Date DATE,
    Ship_Mode VARCHAR(50),
    Customer_ID VARCHAR(50),
    Product_ID VARCHAR(50),
    Sales DECIMAL(10,4),
    Quantity INT,
    Discount DECIMAL(4,2),
    Profit DECIMAL(10,4),
    FOREIGN KEY (Customer_ID) REFERENCES customers(Customer_ID),
    FOREIGN KEY (Product_ID) REFERENCES products(Product_ID)
);

-- 2. Insert data using SELECT DISTINCT
INSERT IGNORE INTO customers (Customer_ID, Customer_Name, Segment)
SELECT DISTINCT `Customer ID`, `Customer Name`, `Segment`
FROM superstore_raw;

-- Using GROUP BY because some Product_IDs map to multiple slight name variations
INSERT IGNORE INTO products (Product_ID, Category, Sub_Category, Product_Name)
SELECT `Product ID`, MAX(`Category`), MAX(`Sub-Category`), MAX(`Product Name`)
FROM superstore_raw
GROUP BY `Product ID`;

-- Parse dates appropriately assuming standard CSV MM/DD/YYYY format
INSERT IGNORE INTO orders (Row_ID, Order_ID, Order_Date, Ship_Date, Ship_Mode, Customer_ID, Product_ID, Sales, Quantity, Discount, Profit)
SELECT DISTINCT 
    `Row ID`, 
    `Order ID`, 
    STR_TO_DATE(`Order Date`, '%m/%d/%Y'), 
    STR_TO_DATE(`Ship Date`, '%m/%d/%Y'), 
    `Ship Mode`, 
    `Customer ID`, 
    `Product ID`, 
    `Sales`, 
    `Quantity`, 
    `Discount`, 
    `Profit`
FROM superstore_raw;


-- 3. Apply Subqueries to filter data

-- 3.1 Filter Data: Above Average Sales
SELECT Order_ID, Sales 
FROM orders
WHERE Sales > (SELECT AVG(Sales) FROM orders);

-- 3.2 Filter Data: Highest Order per Customer
SELECT o1.Customer_ID, o1.Order_ID, o1.Sales AS Highest_Line_Item_Sale
FROM orders o1
WHERE o1.Sales = (
    SELECT MAX(o2.Sales)
    FROM orders o2
    WHERE o2.Customer_ID = o1.Customer_ID
);

-- 4. Use CTEs to compute aggregations: Total sales per customer
WITH CustomerTotalSales AS (
    SELECT Customer_ID, SUM(Sales) AS Total_Sales
    FROM orders
    GROUP BY Customer_ID
)
SELECT c.Customer_Name, cte.Total_Sales
FROM CustomerTotalSales cte
JOIN customers c ON cte.Customer_ID = c.Customer_ID;

-- 5. Customers whose total sales are above average (CTE + Subquery)
WITH CustomerTotalSales AS (
    SELECT Customer_ID, SUM(Sales) AS Total_Sales
    FROM orders
    GROUP BY Customer_ID
)
SELECT c.Customer_Name, cte.Total_Sales
FROM CustomerTotalSales cte
JOIN customers c ON cte.Customer_ID = c.Customer_ID
WHERE cte.Total_Sales > (SELECT AVG(Total_Sales) FROM CustomerTotalSales);

-- 6. Apply Window Functions for ranking and analysis

-- 6.1 Rank all customers based on total sales (Window Function)
SELECT c.Customer_Name, 
       SUM(o.Sales) AS Total_Sales,
       RANK() OVER (ORDER BY SUM(o.Sales) DESC) AS Sales_Rank
FROM orders o
JOIN customers c ON o.Customer_ID = c.Customer_ID
GROUP BY c.Customer_ID, c.Customer_Name;

-- 6.2 Assign row numbers to each order within a customer (Window Function)
SELECT Customer_ID, Order_ID, Order_Date,
       ROW_NUMBER() OVER (PARTITION BY Customer_ID ORDER BY Order_Date ASC) AS Order_Sequence
FROM orders;

-- 6.3 Display top 3 customers based on total sales (Window Function)
WITH RankedCustomers AS (
    SELECT c.Customer_Name, 
           SUM(o.Sales) AS Total_Sales,
           RANK() OVER (ORDER BY SUM(o.Sales) DESC) AS Sales_Rank
    FROM orders o
    JOIN customers c ON o.Customer_ID = c.Customer_ID
    GROUP BY c.Customer_ID, c.Customer_Name
)
SELECT Customer_Name, Total_Sales, Sales_Rank 
FROM RankedCustomers 
WHERE Sales_Rank <= 3;

-- 7. Displays: Customer Name, Total Sales, Rank (JOIN + CTE + Window Function)

WITH CustomerSalesCTE AS (
    SELECT c.Customer_Name, SUM(o.Sales) AS Total_Sales
    FROM customers c
    JOIN orders o ON c.Customer_ID = o.Customer_ID
    GROUP BY c.Customer_ID, c.Customer_Name
)
SELECT Customer_Name, 
       Total_Sales,
       RANK() OVER(ORDER BY Total_Sales DESC) AS Customer_Rank
FROM CustomerSalesCTE;


-- MINI PROJECT: CUSTOMER SALES INSIGHTS

-- 1. Who are the top 5 customers?
SELECT c.Customer_Name, SUM(o.Sales) AS Total_Sales
FROM customers c
JOIN orders o ON c.Customer_ID = o.Customer_ID
GROUP BY c.Customer_ID, c.Customer_Name
ORDER BY Total_Sales DESC
LIMIT 5;

-- 2. Who are the bottom 5 customers?
SELECT c.Customer_Name, SUM(o.Sales) AS Total_Sales
FROM customers c
JOIN orders o ON c.Customer_ID = o.Customer_ID
GROUP BY c.Customer_ID, c.Customer_Name
ORDER BY Total_Sales ASC
LIMIT 5;

-- 3. Which customers made only one order?
SELECT c.Customer_Name, COUNT(DISTINCT o.Order_ID) AS Total_Unique_Orders
FROM customers c
JOIN orders o ON c.Customer_ID = o.Customer_ID
GROUP BY c.Customer_ID, c.Customer_Name
HAVING COUNT(DISTINCT o.Order_ID) = 1;

-- 4. Which customers have above-average sales?
WITH CustomerTotals AS (
    SELECT Customer_ID, SUM(Sales) as Total_Sales
    FROM orders
    GROUP BY Customer_ID
)
SELECT c.Customer_Name, ct.Total_Sales
FROM CustomerTotals ct
JOIN customers c ON ct.Customer_ID = c.Customer_ID
WHERE ct.Total_Sales > (SELECT AVG(Total_Sales) FROM CustomerTotals)
ORDER BY ct.Total_Sales DESC;

-- 5. What is the highest order value per customer?
SELECT c.Customer_Name, MAX(Order_Total) AS Highest_Order_Value
FROM customers c
JOIN (
    SELECT Customer_ID, Order_ID, SUM(Sales) AS Order_Total
    FROM orders
    GROUP BY Customer_ID, Order_ID
) o ON c.Customer_ID = o.Customer_ID
GROUP BY c.Customer_ID, c.Customer_Name;

