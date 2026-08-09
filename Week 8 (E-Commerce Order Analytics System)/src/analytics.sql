-- QUERY: 01_revenue_by_category
SELECT category, ROUND(SUM(revenue), 2) AS total_revenue FROM order_line_revenue GROUP BY category ORDER BY total_revenue DESC;

-- QUERY: 02_top_10_customers
SELECT customer_id, ROUND(SUM(revenue), 2) AS total_order_value FROM order_line_revenue WHERE customer_id IS NOT NULL GROUP BY customer_id ORDER BY total_order_value DESC LIMIT 10;

-- QUERY: 03_monthly_order_count_last_12_months
SELECT strftime('%Y-%m', order_date) AS month, COUNT(*) AS order_count FROM orders WHERE order_date >= datetime('now', '-12 months') GROUP BY month ORDER BY month;

-- QUERY: 04_customers_without_delivered_items
SELECT c.customer_id, c.customer_name FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id) AND NOT EXISTS (SELECT 1 FROM order_line_revenue r WHERE r.customer_id = c.customer_id AND r.status = 'DELIVERED') ORDER BY c.customer_id;

-- QUERY: 05_products_more_returns_than_purchases
SELECT product_id, product_name, SUM(CASE WHEN quantity < 0 THEN ABS(quantity) ELSE 0 END) AS returned_units, SUM(CASE WHEN quantity > 0 THEN quantity ELSE 0 END) AS purchased_units FROM order_line_revenue GROUP BY product_id, product_name HAVING returned_units > purchased_units ORDER BY returned_units DESC;

-- QUERY: 06_return_rate_by_category
SELECT category, SUM(CASE WHEN quantity < 0 THEN ABS(quantity) ELSE 0 END) AS returned_items, SUM(ABS(quantity)) AS total_items, ROUND(100.0 * SUM(CASE WHEN quantity < 0 THEN ABS(quantity) ELSE 0 END) / NULLIF(SUM(ABS(quantity)), 0), 2) AS return_rate_percent FROM order_line_revenue GROUP BY category ORDER BY return_rate_percent DESC;

-- QUERY: 07_running_revenue_by_region
WITH daily AS (SELECT region_code, date(order_date) AS order_date, SUM(revenue) AS daily_revenue FROM order_line_revenue GROUP BY region_code, date(order_date)) SELECT region_code, order_date, ROUND(daily_revenue, 2) AS daily_revenue, ROUND(SUM(daily_revenue) OVER (PARTITION BY region_code ORDER BY order_date), 2) AS running_total FROM daily ORDER BY region_code, order_date;

-- QUERY: 08_product_rank_in_category
WITH totals AS (SELECT category, product_name, SUM(revenue) AS total_revenue FROM order_line_revenue GROUP BY category, product_name) SELECT category, product_name, ROUND(total_revenue, 2) AS total_revenue, DENSE_RANK() OVER (PARTITION BY category ORDER BY total_revenue DESC) AS rank_in_category FROM totals ORDER BY category, rank_in_category, product_name;

-- QUERY: 09_customer_order_gaps_and_risk
WITH gaps AS (SELECT customer_id, order_date, LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS previous_order_date FROM orders WHERE customer_id IS NOT NULL), calculated AS (SELECT customer_id, order_date, previous_order_date, julianday(order_date) - julianday(previous_order_date) AS days_gap FROM gaps) SELECT customer_id, order_date, previous_order_date, ROUND(days_gap, 1) AS days_gap, CASE WHEN AVG(days_gap) OVER (PARTITION BY customer_id) > 30 THEN 'At Risk' ELSE 'Active' END AS customer_status FROM calculated ORDER BY customer_id, order_date;

-- QUERY: 10_monthly_customer_value_segments
WITH monthly AS (SELECT customer_id, strftime('%Y-%m', order_date) AS month, SUM(revenue) AS monthly_revenue FROM order_line_revenue WHERE customer_id IS NOT NULL GROUP BY customer_id, month), categorized AS (SELECT month, customer_id, CASE WHEN monthly_revenue > 10000 THEN 'High' WHEN monthly_revenue >= 5000 THEN 'Medium' ELSE 'Low' END AS segment FROM monthly) SELECT month, segment, COUNT(*) AS customer_count FROM categorized GROUP BY month, segment ORDER BY month, segment;

-- QUERY: 11_ltv_quartiles
WITH ltv AS (SELECT customer_id, SUM(revenue) AS total_value FROM order_line_revenue WHERE customer_id IS NOT NULL GROUP BY customer_id), ranked AS (SELECT customer_id, total_value, NTILE(4) OVER (ORDER BY total_value DESC) AS quartile FROM ltv) SELECT customer_id, ROUND(total_value, 2) AS total_value, quartile, CASE quartile WHEN 1 THEN 'Platinum' WHEN 2 THEN 'Gold' WHEN 3 THEN 'Silver' ELSE 'Bronze' END AS quartile_label FROM ranked ORDER BY quartile, total_value DESC;

-- QUERY: 12_yoy_revenue
WITH monthly AS (SELECT CAST(strftime('%Y', order_date) AS INTEGER) AS year, CAST(strftime('%m', order_date) AS INTEGER) AS month, SUM(revenue) AS revenue FROM order_line_revenue GROUP BY year, month) SELECT current.year, current.month, ROUND(current.revenue, 2) AS revenue, ROUND(previous.revenue, 2) AS prev_year_revenue, CASE WHEN previous.revenue IS NULL OR previous.revenue = 0 THEN NULL ELSE ROUND((current.revenue - previous.revenue) * 100.0 / previous.revenue, 2) END AS yoy_growth_percent FROM monthly current LEFT JOIN monthly previous ON previous.year = current.year - 1 AND previous.month = current.month ORDER BY current.year, current.month;

-- QUERY: 13_first_last_category_shift
WITH customer_categories AS (SELECT customer_id, category, order_date, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, item_id) AS first_rn, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, item_id DESC) AS last_rn FROM order_line_revenue WHERE customer_id IS NOT NULL AND quantity > 0), summary AS (SELECT customer_id, MAX(CASE WHEN first_rn = 1 THEN category END) AS first_purchased_category, MAX(CASE WHEN last_rn = 1 THEN category END) AS recent_purchased_category FROM customer_categories GROUP BY customer_id) SELECT *, CASE WHEN first_purchased_category = recent_purchased_category THEN 'No' ELSE 'Yes' END AS category_shift FROM summary ORDER BY customer_id;

-- QUERY: 14_cumulative_customer_revenue
WITH customer_revenue AS (SELECT customer_id, SUM(revenue) AS revenue FROM order_line_revenue WHERE customer_id IS NOT NULL GROUP BY customer_id), cumulative AS (SELECT customer_id, revenue, SUM(revenue) OVER (ORDER BY revenue DESC) AS cumulative_revenue, SUM(revenue) OVER () AS total_revenue FROM customer_revenue) SELECT customer_id, ROUND(revenue, 2) AS revenue, ROUND(cumulative_revenue, 2) AS cumulative_revenue, ROUND(100.0 * cumulative_revenue / NULLIF(total_revenue, 0), 2) AS cumulative_percent FROM cumulative ORDER BY revenue DESC;

-- QUERY: 15_cohort_retention
WITH cohort AS (SELECT customer_id, strftime('%Y-%m', registration_date) AS cohort_month FROM customers), activity AS (SELECT o.customer_id, strftime('%Y-%m', o.order_date) AS activity_month FROM orders o WHERE o.customer_id IS NOT NULL GROUP BY o.customer_id, activity_month), indexed AS (SELECT c.cohort_month, a.customer_id, (CAST(strftime('%Y', a.activity_month || '-01') AS INTEGER) - CAST(strftime('%Y', c.cohort_month || '-01') AS INTEGER)) * 12 + (CAST(strftime('%m', a.activity_month || '-01') AS INTEGER) - CAST(strftime('%m', c.cohort_month || '-01') AS INTEGER)) AS month_number FROM cohort c JOIN activity a ON a.customer_id = c.customer_id), sizes AS (SELECT cohort_month, COUNT(*) AS cohort_size FROM cohort GROUP BY cohort_month) SELECT s.cohort_month, s.cohort_size, COUNT(DISTINCT CASE WHEN i.month_number = 0 THEN i.customer_id END) AS month_0_customers, COUNT(DISTINCT CASE WHEN i.month_number = 1 THEN i.customer_id END) AS month_1_customers, COUNT(DISTINCT CASE WHEN i.month_number = 2 THEN i.customer_id END) AS month_2_customers, COUNT(DISTINCT CASE WHEN i.month_number = 3 THEN i.customer_id END) AS month_3_customers, ROUND(100.0 * COUNT(DISTINCT CASE WHEN i.month_number = 1 THEN i.customer_id END) / s.cohort_size, 2) AS month_1_retention_percent, ROUND(100.0 * COUNT(DISTINCT CASE WHEN i.month_number = 2 THEN i.customer_id END) / s.cohort_size, 2) AS month_2_retention_percent, ROUND(100.0 * COUNT(DISTINCT CASE WHEN i.month_number = 3 THEN i.customer_id END) / s.cohort_size, 2) AS month_3_retention_percent FROM sizes s LEFT JOIN indexed i ON i.cohort_month = s.cohort_month GROUP BY s.cohort_month, s.cohort_size ORDER BY s.cohort_month;

-- QUERY: 16_products_bought_together
SELECT a.product_name AS product_a, b.product_name AS product_b, COUNT(DISTINCT a.order_id) AS times_bought_together FROM order_line_revenue a JOIN order_line_revenue b ON a.order_id = b.order_id AND a.product_id < b.product_id WHERE a.quantity > 0 AND b.quantity > 0 GROUP BY a.product_id, b.product_id, a.product_name, b.product_name ORDER BY times_bought_together DESC, product_a, product_b LIMIT 50;
