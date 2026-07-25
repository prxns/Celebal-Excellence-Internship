Section A — SQL Basics (SELECT, Constraints, Primary Keys) 
-- Q1
SELECT * FROM customers;

-- Q2
SELECT first_name,last_name,city
FROM customers;

-- Q3
SELECT DISTINCT category
FROM products;

-- Q4

Table	        Primary Key
customers	    customer_id
products	    product_id
orders	        order_id
order_items	    item_id

* A Primary Key uniquely identifies every record. It cannot contain duplicate or NULL values, ensuring data integrity. 

-- Q5
Constraints on email

1. UNIQUE
2. NOT NULL

If a duplicate email is inserted, the database returns a UNIQUE constraint violation and rejects the insert.

-- Q6
INSERT INTO products
VALUES
(209,'Test Product','Electronics','ABC',-50,10);

The database rejects the insert because of:

CHECK (unit_price > 0)

Error: CHECK constraint violated.

-- Q7
SELECT *
FROM orders
WHERE status='Delivered';

-- Q8
SELECT *
FROM products
WHERE category='Electronics'
AND unit_price>2000;

-- Q9
SELECT *
FROM customers
WHERE state='Maharashtra'
AND join_date BETWEEN '2024-01-01' AND '2024-12-31';

-- Q10
SELECT *
FROM orders
WHERE order_date
BETWEEN '2024-08-10'
AND '2024-08-25'
AND status<>'Cancelled';

-- Q11
SELECT *
FROM orders
WHERE order_date BETWEEN '2024-08-01'
AND '2024-08-31';

-- Q12
No.

YEAR(join_date)

applies a function to the indexed column, making the query non-SARGable, so the index typically won't be used efficiently.

Better query:

SELECT *
FROM customers
WHERE join_date
BETWEEN '2024-01-01'
AND '2024-12-31';

-- Q13
SELECT COUNT(*) AS total_orders
FROM orders;

Answer: 10

-- Q14
SELECT SUM(total_amount)
FROM orders
WHERE status='Delivered';

Answer: 17191

-- Q15
SELECT
category,
AVG(unit_price) AS avg_price
FROM products
GROUP BY category;

-- Q16
SELECT
status,
COUNT(*) AS total_orders,
SUM(total_amount) AS revenue
FROM orders
GROUP BY status
ORDER BY revenue DESC;

-- Q17
SELECT
category,
MAX(unit_price) AS highest_price,
MIN(unit_price) AS lowest_price
FROM products
GROUP BY category;

-- Q18
SELECT
category,
AVG(unit_price) AS average_price
FROM products
GROUP BY category
HAVING AVG(unit_price)>2000;

-- Q19
SELECT
o.order_id,
o.order_date,
c.first_name,
c.last_name,
o.total_amount
FROM orders o
INNER JOIN customers c
ON o.customer_id=c.customer_id;

-- Q20
SELECT
c.customer_id,
c.first_name,
o.order_id,
o.order_date
FROM customers c
LEFT JOIN orders o
ON c.customer_id=o.customer_id;

-- Q21
SELECT
o.order_id,
p.product_name,
oi.quantity,
oi.unit_price,
oi.discount_pct
FROM orders o
JOIN order_items oi
ON o.order_id=oi.order_id
JOIN products p
ON oi.product_id=p.product_id;

-- Q22
LEFT JOIN returns all rows from the left table and matching rows from the right table.

RIGHT JOIN returns all rows from the right table and matching rows from the left table.

FULL OUTER JOIN returns all rows from both tables, matching where possible and filling non-matches with NULLs. It is useful when you need every customer and every order, even if there is no corresponding match.

-- Q23
Foreign Keys

orders.customer_id → customers.customer_id
order_items.order_id → orders.order_id
order_items.product_id → products.product_id

If you insert:

customer_id=999

the insert fails because it violates the foreign key constraint.

-- Q24
SELECT
product_name,
unit_price,
CASE
WHEN unit_price<1000 THEN 'Budget'
WHEN unit_price BETWEEN 1000 AND 3000 THEN 'Mid-Range'
ELSE 'Premium'
END AS price_tier
FROM products;

-- Q25
SELECT
SUM(CASE WHEN status='Delivered' THEN 1 ELSE 0 END) AS Delivered,
SUM(CASE WHEN status<>'Delivered' THEN 1 ELSE 0 END) AS Not_Delivered
FROM orders;

Output: Delivered = 6

        Not Delivered = 4

-- Q26
Atomicity: A transaction completes entirely or not at all.

Consistency: Data remains valid before and after a transaction.

Isolation: Concurrent transactions do not interfere with each other.

Durability: Once committed, changes are permanently stored even after a crash.

Example: During a bank transfer, money is debited from one account and credited to another. If the credit step fails, Atomicity rolls back the debit. Consistency ensures balances remain valid, Isolation prevents simultaneous transfers from causing conflicts, and Durability guarantees the completed transfer is not lost after a system failure.

-- Q27
START TRANSACTION;

INSERT INTO orders
VALUES
(
1011,
102,
CURDATE(),
'Pending',
1598.00
);

INSERT INTO order_items
VALUES
(5016,1011,206,1,1299.00,0);

INSERT INTO order_items
VALUES
(5017,1011,208,1,299.00,0);

UPDATE products
SET stock_qty=stock_qty-1
WHERE product_id=206;

UPDATE products
SET stock_qty=stock_qty-1
WHERE product_id=208;

COMMIT;

If any statement fails, execute: ROLLBACK;