"""
Celebal Technologies - Celebal Excellence Internship 2026
Week 6: Apache Spark Architecture & Data Processing

Objective:
Understand Spark architecture and perform efficient data processing using
transformations, filtering, schema handling, optimized file formats, and
performance-aware Spark practices.

Pipeline:
CSV -> Schema Handling -> Transformations -> Filtering -> Null Handling
-> Parquet -> Predicate Pushdown Demonstration -> CSV Output
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round as spark_round
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
)

# 1. CREATE SPARK SESSIO

spark = (
    SparkSession.builder
    .appName("Celebal_Week6_Spark_Assignment")
    .getOrCreate()
)

# Reduce unnecessary console output.
spark.sparkContext.setLogLevel("WARN")


print("\n" + "=" * 70)
print("CELEBAL TECHNOLOGIES - WEEK 6 SPARK ASSIGNMENT")
print("=" * 70)

# 2. READ CSV USING HEADER AND INFER SCHEMA 

print("\n[1] Reading CSV using header=True and inferSchema=True")

df_inferred = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv("data/source.csv")
)

print("\nInferred Schema:")
df_inferred.printSchema()

print("\nSample Records:")
df_inferred.show(5, truncate=False)

# 3. DEFINE AN EXPLICIT SCHEMA ()

print("\n[2] Reading the same dataset using an explicit schema")

product_schema = StructType([
    StructField("product_id", StringType(), False),
    StructField("product_name", StringType(), True),
    StructField("category", StringType(), True),
    StructField("base_price", DoubleType(), True),
    StructField("user_id", StringType(), True),
    StructField("region", StringType(), True),
    StructField("priority", StringType(), True),
    StructField("status", StringType(), True),
    StructField("amount", DoubleType(), True),
])

df = (
    spark.read
    .option("header", "true")
    .schema(product_schema)
    .csv("data/source.csv")
)

print("\nExplicit Schema:")
df.printSchema()

# 4. SELECT AND FILTER REQUIRED COLUMN (product_id, base_price) FOR ELECTRONICS CATEGORY

print("\n[3] Electronics products - product_id and price")

electronics_df = (
    df
    .filter(col("category") == "Electronics")
    .select(
        "product_id",
        col("base_price").alias("price")
    )
)

electronics_df.show(truncate=False)

# 5. MODIFY DATAFRAM (Renaming, Casting, Adding Calculated Column)

print("\n[4] Modifying DataFrame")

transformed_df = (
    df
    .withColumnRenamed("product_name", "product")
    .withColumn("base_price", col("base_price").cast(DoubleType()))
    .withColumn(
        "final_price",
        spark_round(col("base_price") * 1.18, 2)
    )
)

transformed_df.select(
    "product_id",
    "product",
    "base_price",
    "final_price"
).show(truncate=False)

# 6. FILTER COMPLETED ORDERS WITH AMOUNT > 100

print("\n[5] Completed orders with amount greater than 1000")

completed_orders_df = transformed_df.filter(
    (col("status") == "Completed") &
    (col("amount") > 1000)
)

completed_orders_df.select(
    "product_id",
    "product",
    "status",
    "amount"
).show(truncate=False)

# 7. FILTER REGION = NORTH OR PRIORITY = HIG

print("\n[6] Records where region is North OR priority is High")

north_or_high_df = transformed_df.filter(
    (col("region") == "North") |
    (col("priority") == "High")
)

north_or_high_df.select(
    "product_id",
    "product",
    "region",
    "priority"
).show(truncate=False)

# 8. HANDLE NULL VALUE

print("\n[7] Checking records containing NULL user_id")

transformed_df.filter(
    col("user_id").isNull()
).select(
    "product_id",
    "product",
    "user_id"
).show(truncate=False)


print("\nRemoving records where user_id is NULL")

clean_df = transformed_df.filter(
    col("user_id").isNotNull()
)

clean_df.show(truncate=False)

# 9. TRANSFORMATION VS ACTION / LAZY EVALUATION

print("\n[8] Demonstrating Lazy Evaluation")

lazy_filtered_df = clean_df.filter(
    col("category") == "Electronics"
)

lazy_selected_df = lazy_filtered_df.select(
    "product_id",
    "product",
    "final_price"
)

print("Transformations have been defined.")
print("Calling show() now triggers execution.")

lazy_selected_df.show(5, truncate=False)

# 10. INSPECT EXECUTION PLA

print("\n[9] Spark Execution Plan")

lazy_selected_df.explain(mode="formatted")

# 11. WRITE CLEAN DATA TO PARQUE

print("\n[10] Writing cleaned dataset to Parquet")

parquet_output_path = "output/parquet/clean_products"

(
    clean_df.write
    .mode("overwrite")
    .parquet(parquet_output_path)
)

print(f"Parquet output written to: {parquet_output_path}")

# 12. READ PARQUET AND APPLY FILTE

print("\n[11] Reading Parquet and filtering region = North")

parquet_df = spark.read.parquet(parquet_output_path)

north_parquet_df = (
    parquet_df
    .filter(col("region") == "North")
    .select(
        "product_id",
        "product",
        "region",
        "final_price"
    )
)

north_parquet_df.show(truncate=False)

# 13. INSPECT PARQUET FILTER EXECUTION PLA

print("\n[12] Parquet Filter Execution Plan")

north_parquet_df.explain(mode="formatted")

# 14. WRITE PROCESSED DATA TO CS

print("\n[13] Writing processed data to CSV")

csv_output_path = "output/csv/processed_products"

(
    clean_df.write
    .mode("overwrite")
    .option("header", "true")
    .csv(csv_output_path)
)

print(f"CSV output written to: {csv_output_path}")

# 15. WRITE FINAL PROCESSED DATA TO PARQUE

print("\n[14] Writing processed data to Parquet")

final_parquet_path = "output/parquet/processed_products"

(
    clean_df.write
    .mode("overwrite")
    .parquet(final_parquet_path)
)

print(f"Final Parquet output written to: {final_parquet_path}")

# 16. SAFE DATASET EXPLORATIO

print("\n[15] Safe dataset exploration using show(5)")

clean_df.show(5, truncate=False)

# 17. BASIC EXECUTION RESULT

print("\n[16] Pipeline Summary")

input_count = df.count()
clean_count = clean_df.count()
electronics_count = lazy_filtered_df.count()

print(f"Input records             : {input_count}")
print(f"Records after null removal: {clean_count}")
print(f"Electronics records       : {electronics_count}")

# 18. STOP SPARK SESSIO

print("\n" + "=" * 70)
print("WEEK 6 SPARK PIPELINE EXECUTED SUCCESSFULLY")
print("=" * 70)

spark.stop()