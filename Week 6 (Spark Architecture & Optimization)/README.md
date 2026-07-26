# Week 6 — Spark Architecture & Data Processing

## Celebal Technologies — Celebal Summer Internship 2026

This repository contains the implementation and documentation for the **Week 6 assignment on Apache Spark Architecture and Data Processing**.

The assignment focuses on understanding Spark's distributed architecture and applying PySpark concepts such as DataFrame transformations, filtering, schema handling, lazy evaluation, execution plans, partitioning, Parquet processing, and performance optimization.

---

## Assignment Objectives

The practical implementation covers:

- Spark architecture and execution concepts
- Driver, Cluster Manager, and Executors
- Client Mode vs Cluster Mode
- Lazy Evaluation
- DAG and Spark execution plans
- CSV data loading
- Schema handling and type casting
- Null value handling
- Filtering and column selection
- DataFrame transformations
- Transformations vs Actions
- Wide transformations and shuffle
- Partitioning concepts
- CSV vs Parquet
- Predicate Pushdown
- Data processing pipelines
- Safe exploration of large datasets using `show()` instead of `collect()`

---

## Project Structure

```text
Week 6 (Spark Architecture & Optimization)/
│
├── Assignment.md
│
├── README.md
├── Brief Insights.md
│
├── data/
│   └── source.csv
│
├── src/
│   └── week6_spark_assignment.py
│
└── results/
    ├── 00_spark_setup.png
    ├── 01_data_loading.png
    ├── 02a_schema_handling.png
    ├── 02b_null_handling.png
    ├── 03_filtering_and_column_selection.png
    ├── 04_dataframe_transformations.png
    ├── 05_transformations_and_actions.png
    ├── 06_lazy_evaluation.png
    ├── 07a_logical_plan.png
    ├── 07b_physical_plan.png
    ├── 08_wide_transformation.png
    ├── 09_parquet_write.png
    ├── 10a_partitioning_output.png
    ├── 10b_partitioning_execution_plan.png
    ├── 11_transformations_vs_actions.png
    ├── 12_parquet_null_handling_csv_output.png
    ├── 13_client_vs_cluster_mode.png
    ├── 14_north_or_high_filter.png
    └── 15_show_vs_collect.png
```

---

## Dataset

The assignment uses a sample product dataset containing fields such as:

- Product ID
- Product Name
- Category
- Base Price
- User ID
- Region
- Priority
- Status
- Amount

The dataset is loaded into Spark and processed using PySpark DataFrame operations.

---

## Technologies Used

- Apache Spark
- PySpark
- Databricks
- Spark SQL / DataFrame API
- Python
- CSV
- Parquet
- Visual Studio Code
- Git & GitHub

---

## Implementation

The practical implementation follows a typical Spark processing pipeline:

```text
Source Data
     ↓
Read Dataset
     ↓
Schema Handling
     ↓
Null Handling
     ↓
Transformations
     ↓
Filtering
     ↓
Column Selection
     ↓
Aggregation / Partitioning
     ↓
Execution Plan Analysis
     ↓
Output Preparation
```

Spark's execution plans were also inspected to understand how transformations are optimized before execution.

---

## Databricks Environment Limitations

The practical implementation was executed using **Databricks Free Edition with Serverless Compute**.

Some operations normally available in a standard or dedicated Apache Spark environment are restricted in this environment. Because of these restrictions, a few parts of the assignment were demonstrated using equivalent supported approaches.

### Parquet Output Restriction

Direct creation of a managed table using the Parquet format was restricted because the Databricks environment supports **Delta as the managed table format**.

Writing directly to the public DBFS root was also unavailable in the Serverless environment.

Therefore, the assignment demonstrates Parquet concepts using the available Spark/Databricks execution information and DataFrame operations where direct filesystem-based Parquet output was restricted.

The execution plan still demonstrates Spark's interaction with columnar storage and the relevant optimization concepts.

### RDD Restriction

Databricks Serverless Compute does not support direct custom PySpark RDD operations such as:

```python
df.rdd.getNumPartitions()
```

Therefore, partitioning was demonstrated using the supported DataFrame API:

```python
df.repartition("category")
```

The resulting DataFrame and Spark execution plan were inspected to demonstrate the repartitioning/shuffle operation without relying on unsupported RDD APIs.

### Why These Alternatives Were Used

These changes were caused by restrictions of the execution environment rather than limitations of Apache Spark itself.

Where an operation was unavailable, the closest supported Spark DataFrame or execution-plan-based approach was used so that the underlying concept could still be demonstrated correctly.

---

## Execution Results

The `results/` directory contains screenshots from the Databricks notebook showing the execution and output of the practical implementation.

The screenshots provide evidence for:

- Data loading
- Schema inspection
- Null handling
- Filtering
- DataFrame transformations
- Lazy Evaluation
- Logical and Physical Plans
- Wide transformations
- Parquet processing
- Partitioning
- Transformations and Actions
- Client vs Cluster Mode
- Conditional filtering
- `show()` vs `collect()`

---

## Assignment Questions

The answers to the **15 theoretical and coding questions** provided with the Week 6 assignment are available in:

```text
Assignment.md
```

---

## Conclusion

This assignment demonstrates how Apache Spark processes data through distributed DataFrame operations while optimizing execution through Lazy Evaluation, DAG-based execution, query optimization, columnar storage, and distributed transformations.

The practical work also demonstrates how Spark concepts can be implemented within a managed cloud environment while adapting to platform-specific restrictions.