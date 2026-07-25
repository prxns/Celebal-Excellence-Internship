import sys
import os

# Tell PySpark exactly which Python executable to use for workers
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, count, max, min, sum as _sum
from pyspark.sql.types import TimestampType

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, count, max, min, sum as _sum
from pyspark.sql.types import TimestampType

# Initialize Spark Session
spark = SparkSession.builder.appName("SparkFundamentals").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

print("--- 1. Generating Dummy Datasets ---")
# Sample data for transactions & sales
data_sales = [
    (1, "2026-01-01", "West", "Electronics", 200.0, 25, "Premium", "ny"),
    (1, "2026-01-01", "West", "Electronics", 200.0, 25, "Premium", "ny"),  # Duplicate
    (2, "2026-01-02", "East", "Furniture", None, 35, "Basic", "la"),
    (3, "2026-01-03", "West", "Clothing", 150.0, 19, "Premium", "ny"),
    (4, "2026-01-04", "West", "Electronics", 300.0, 45, "Basic", "sf"),
]
schema_sales = [
    "user_id",
    "transaction_date",
    "region",
    "product_category",
    "sale_amount",
    "age",
    "subscription",
    "city",
]

df_sales = spark.createDataFrame(data_sales, schema_sales)

# Q3: Remove duplicate rows based on user_id and transaction_date
print("\n--- Q3: Deduplicated Data ---")
df_dedup = df_sales.dropDuplicates(["user_id", "transaction_date"])
df_dedup.show()

# Q4: Filter region=='West' and group by product_category for avg sale_amount
print("\n--- Q4: Average sale amount for region 'West' ---")
df_sales.filter(col("region") == "West").groupBy("product_category").agg(
    avg("sale_amount").alias("avg_sale_amount")
).show()

# Q6: Total count of records for each city (> 100 count logic demonstrated)
print("\n--- Q6: Count of records for each city ---")
df_sales.groupBy("city").agg(count("*").alias("city_count")).filter(
    col("city_count") > 0
).show()

# Q8: Filter age between 18 and 30 (inclusive) and subscription == 'Premium'
print("\n--- Q8: Filter Age [18, 30] & Premium Subscription ---")
df_sales.filter(
    (col("age") >= 18) & (col("age") <= 30) & (col("subscription") == "Premium")
).show()

# Q10: Cast raw_timestamp to TimestampType and rename to event_time
print("\n--- Q10: Modify Schema (Cast & Rename) ---")
df_time = spark.createDataFrame([("2026-07-20 10:00:00",)], ["raw_timestamp"])
df_time_transformed = df_time.withColumn(
    "event_time", col("raw_timestamp").cast(TimestampType())
).drop("raw_timestamp")
df_time_transformed.printSchema()

# Q12: Filter out null emails OR empty string usernames
print("\n--- Q12: Data Cleaning (Null emails / Empty usernames) ---")
data_users = [
    (1, "alice@example.com", "alice123"),
    (2, None, "bob_user"),
    (3, "charlie@example.com", ""),
]
df_users = spark.createDataFrame(data_users, ["id", "email", "username"])
df_users_clean = df_users.filter(
    col("email").isNotNull() & (col("username") != "") & col("username").isNotNull()
)
df_users_clean.show()

# Q13: Multiple statistics using agg() on price column
print("\n--- Q13: Aggregate Multiple Statistics ---")
data_prices = [(10.0,), (20.0,), (30.0,), (40.0,)]
df_prices = spark.createDataFrame(data_prices, ["price"])
df_prices.agg(
    min("price").alias("min_price"),
    max("price").alias("max_price"),
    avg("price").alias("mean_price"),
).show()

# Q15: Final Complete Processing Pipeline
# 1. Filters out duplicates.
# 2. Fills null prices with 0.
# 3. Groups by store_id to calculate total revenue.
print("\n--- Q15: Final Complete Pipeline Output ---")
pipeline_data = [
    (101, 150.0),
    (101, 150.0),  # Duplicate
    (101, None),  # Null price
    (102, 200.0),
    (102, None),
]
df_pipeline_raw = spark.createDataFrame(pipeline_data, ["store_id", "price"])

pipeline_result = (
    df_pipeline_raw.dropDuplicates()
    .na.fill({"price": 0})
    .groupBy("store_id")
    .agg(_sum("price").alias("total_revenue"))
)

pipeline_result.show()

spark.stop()