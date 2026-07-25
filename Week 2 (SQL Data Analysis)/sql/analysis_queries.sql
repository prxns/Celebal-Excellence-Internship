-- 2.1. Explore Table Schema
SHOW TABLES;

DESCRIBE customers;

DESCRIBE products;

DESCRIBE orders;

DESCRIBE order_items;

-- 2.2. Display Sample Data
SELECT * FROM customers LIMIT 5;

SELECT * FROM products LIMIT 5;

SELECT * FROM orders LIMIT 5;

SELECT * FROM order_items LIMIT 5;

-- 3.1 WHERE Filtering: Region-Based Customer Filtering
SELECT *
FROM customers
WHERE state='Maharashtra';

-- 3.2 WHERE Filtering: Category-Based Product Filtering
SELECT *
FROM products
WHERE category='Electronics';

-- 3.3 WHERE Filtering: Date-Based Order Filtering
SELECT *
FROM orders
WHERE order_date
BETWEEN '2024-08-10'
AND '2024-08-25';

-- 3.4 WHERE Filtering: Sales-Based Order Filtering
SELECT *
FROM orders
WHERE total_amount>3000;

-- 4.1 GROUP BY Aggregation: Sales
SELECT
status,
SUM(total_amount)
FROM orders
GROUP BY status;

--4.2 GROUP BY Aggregation: Quantity
SELECT
status,
COUNT(*)
FROM orders
GROUP BY status;

-- 4.3 GROUP BY Aggregation: Average
SELECT
status,
AVG(total_amount)
FROM orders
GROUP BY status;

-- 5.1 SORT and Limit Results: Product Sales
SELECT
product_id,
SUM(quantity)
AS TotalSold
FROM order_items
GROUP BY product_id;

-- 5.2 SORT and Limit Results: Category Revenue
SELECT
p.category,
SUM(o.total_amount)
AS Revenue
FROM products p
JOIN order_items oi
ON p.product_id=oi.product_id
JOIN orders o
ON oi.order_id=o.order_id
GROUP BY p.category;

-- 5.3 Sorting: Top Expensive Products
SELECT *
FROM products
ORDER BY unit_price DESC;

-- 5.4 Limit: Top 3 Products
SELECT *
FROM products
ORDER BY unit_price DESC
LIMIT 3;

-- 6.1 Use Cases: Monthly Trends
SELECT
MONTH(order_date) Month,
SUM(total_amount) Sales
FROM orders
GROUP BY MONTH(order_date);

-- 6.2 Use Cases: Top Customers
SELECT
customer_id,
SUM(total_amount)
AS TotalSpent
FROM orders
GROUP BY customer_id
ORDER BY TotalSpent DESC;

-- 6.3 Use Cases: Duplicate Emails
SELECT
email,
COUNT(*)
FROM customers
GROUP BY email
HAVING COUNT(*)>1;

-- 7.1 Validate Results: Data Quality (Null Values)
SELECT *
FROM customers
WHERE email IS NULL;

-- 7.2 Validate Results: Data Quality (Negative Prices)
SELECT *
FROM products
WHERE unit_price<0;
 
-- 7.3 Validate Results: Data Quality (Cancelled Orders)
SELECT *
FROM orders
WHERE status='Cancelled';

