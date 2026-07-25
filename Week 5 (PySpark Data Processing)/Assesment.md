# Apache Spark DataFrame Assessment -- Celebal Technologies

## Q1. What are the key limitations of traditional MapReduce that make Spark a preferred choice for modern big data processing?

### Answer

**1. Disk I/O Bottleneck** - MapReduce writes intermediate results to
HDFS after every Map and Reduce phase. - This frequent disk read/write
operation makes processing slow. - Spark stores intermediate data in
**RAM (in-memory)**, making processing up to **100× faster** for many
workloads.

**2. High Latency** - MapReduce is designed for batch processing and is
not suitable for real-time analytics, streaming, or interactive
queries. - Spark supports **real-time processing**, interactive
analytics, streaming, and machine learning.

**3. Complex APIs** - MapReduce requires a large amount of boilerplate
Java code. - Spark provides simple, high-level APIs in **Python
(PySpark), Scala, Java, SQL, and R**, making development easier.

------------------------------------------------------------------------

## Q2. Explain how Spark uses In-Memory Computing to speed up iterative machine learning algorithms compared to disk-based systems.

### Answer

Spark stores intermediate data in memory (RAM) instead of repeatedly
reading and writing data to disk. Iterative machine learning algorithms
repeatedly access the same dataset, so caching data in memory eliminates
expensive disk I/O, significantly reducing execution time and improving
overall performance.

------------------------------------------------------------------------

## Q3. Remove duplicate rows based on `user_id` and `transaction_date`.

--- Q3: Deduplicated Data ---
+-------+----------------+------+----------------+-----------+---+------------+----+
|user_id|transaction_date|region|product_category|sale_amount|age|subscription|city|
+-------+----------------+------+----------------+-----------+---+------------+----+
|      1|      2026-01-01|  West|     Electronics|      200.0| 25|     Premium|  ny|
|      2|      2026-01-02|  East|       Furniture|       NULL| 35|       Basic|  la|
|      3|      2026-01-03|  West|        Clothing|      150.0| 19|     Premium|  ny|
|      4|      2026-01-04|  West|     Electronics|      300.0| 45|       Basic|  sf|
+-------+----------------+------+----------------+-----------+---+------------+----+

------------------------------------------------------------------------

## Q4. Filter rows where region is `'West'` and find the average `sale_amount` grouped by `product_category`.

--- Q4: Average sale amount for region 'West' ---
+----------------+------------------+                                           
|product_category|   avg_sale_amount|
+----------------+------------------+
|     Electronics|233.33333333333334|
|        Clothing|             150.0|
+----------------+------------------+

------------------------------------------------------------------------

## Q5. Difference between `.na.drop()` and `.na.fill()`.

### Answer

  Method         Purpose
  -------------- ----------------------------------------------
  `.na.drop()`   Removes rows containing null values.
  `.na.fill()`   Replaces null values with a specified value.

### Example

``` python
df = df.na.fill({"status": "Unknown"})
```

------------------------------------------------------------------------

## Q6. Find cities having more than 100 records.

--- Q6: Count of records for each city ---
+----+----------+                                                               
|city|city_count|
+----+----------+
|  ny|         3|
|  la|         1|
|  sf|         1|
+----+----------+

------------------------------------------------------------------------

## Q7. How does DataFrame immutability affect data cleaning?

### Answer

Spark DataFrames are **immutable**, meaning they cannot be modified
after creation. Every cleaning operation (such as dropping columns,
renaming columns, filtering rows, or replacing null values) creates and
returns a **new DataFrame**, leaving the original DataFrame unchanged.

Example:

``` python
new_df = df.drop("age")
new_df = new_df.withColumnRenamed("fname", "first_name")
```

------------------------------------------------------------------------

## Q8. Filter users aged 18--30 with Premium subscription.

--- Q8: Filter Age [18, 30] & Premium Subscription ---
+-------+----------------+------+----------------+-----------+---+------------+----+
|user_id|transaction_date|region|product_category|sale_amount|age|subscription|city|
+-------+----------------+------+----------------+-----------+---+------------+----+
|      1|      2026-01-01|  West|     Electronics|      200.0| 25|     Premium|  ny|
|      1|      2026-01-01|  West|     Electronics|      200.0| 25|     Premium|  ny|
|      3|      2026-01-03|  West|        Clothing|      150.0| 19|     Premium|  ny|
+-------+----------------+------+----------------+-----------+---+------------+----+

------------------------------------------------------------------------

## Q9. Why handle null values before aggregation?

### Answer

Handling null values before performing aggregations helps: - Produce
accurate results. - Prevent missing values from affecting
calculations. - Avoid unexpected outputs when filling missing numeric
values with appropriate defaults.

------------------------------------------------------------------------

## Q10. Cast `raw_timestamp` to `TimestampType` and rename it.

--- Q10: Modify Schema (Cast & Rename) ---
root
 |-- event_time: timestamp (nullable = true)


--- Q12: Data Cleaning (Null emails / Empty usernames) ---
+---+-----------------+--------+                                                
| id|            email|username|
+---+-----------------+--------+
|  1|alice@example.com|alice123|
+---+-----------------+--------+

------------------------------------------------------------------------

## Q11. Explain Shuffle and why it is a wide transformation.

### Answer

A **Shuffle** is the process of redistributing data across partitions so
that records with the same key are brought together. Operations such as
`groupBy()`, `join()`, and `reduceByKey()` require shuffling.

It is considered a **wide transformation** because data moves between
different partitions across the cluster, involving network communication
and disk usage, making it more expensive than narrow transformations.

------------------------------------------------------------------------

## Q12. Remove rows where email is null OR username is empty.

``` python
from pyspark.sql.functions import col

clean_df = df.filter(
    col("email").isNotNull() &
    (col("username") != "")
)
```

------------------------------------------------------------------------

## Q13. Calculate minimum, maximum, and mean of `price`.

--- Q13: Aggregate Multiple Statistics ---
+---------+---------+----------+                                                
|min_price|max_price|mean_price|
+---------+---------+----------+
|     10.0|     40.0|      25.0|
+---------+---------+----------+

------------------------------------------------------------------------

## Q14. Risk of using `inferSchema=True` with inconsistent date formats.

### Answer

When source data contains inconsistent or messy date formats, Spark may
incorrectly infer the column type as **StringType** or produce incorrect
date parsing. This can lead to errors during filtering, sorting,
aggregations, and timestamp operations. Explicitly defining the schema
is more reliable for production datasets.

------------------------------------------------------------------------

## Q15. Final processing pipeline.

--- Q15: Final Complete Pipeline Output ---
+--------+-------------+                                                        
|store_id|total_revenue|
+--------+-------------+
|     101|        150.0|
|     102|        200.0|
+--------+-------------+

------------------------------------------------------------------------

## Summary

This document covers: - Spark advantages over MapReduce - In-memory
computing - DataFrame cleaning - Filtering - Aggregations - Handling
null values - Wide transformations (Shuffle) - PySpark DataFrame
operations commonly used in data engineering and analytics.
