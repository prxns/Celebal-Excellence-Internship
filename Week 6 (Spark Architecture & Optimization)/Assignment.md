# Week 6 Assignment — Apache Spark Architecture & Data Processing

## Objective

The objective of this assignment is to understand Apache Spark architecture and perform efficient data processing using DataFrames, transformations, filtering, schema handling, optimized file formats, and performance optimization techniques.

---

## Q1. Explain the roles of the Driver, Cluster Manager, and Executor in a Spark application.

Apache Spark follows a distributed architecture consisting primarily of the **Driver**, **Cluster Manager**, and **Executors**.

### Driver

The Driver is the main process of a Spark application. It is responsible for:

* Running the main application code.
* Creating and maintaining the `SparkSession`/`SparkContext`.
* Building execution plans for Spark jobs.
* Dividing work into jobs, stages, and tasks.
* Scheduling tasks for execution on executors.
* Tracking the status of the application and coordinating execution.

### Cluster Manager

The Cluster Manager manages and allocates computing resources across the cluster. It provides resources such as CPU and memory to Spark applications.

Spark can work with cluster managers such as:

* Spark Standalone
* Hadoop YARN
* Kubernetes

### Executor

Executors are processes launched for a Spark application on worker nodes. Their responsibilities include:

* Executing tasks assigned by the Driver.
* Performing transformations and computations on partitions of data.
* Storing cached or persisted data.
* Returning task results and status information to the Driver.

Therefore, the Driver coordinates the application, the Cluster Manager allocates resources, and Executors perform the distributed computation.

---

## Q2. How does Spark's Lazy Evaluation strategy improve performance when chain-processing large datasets?

Spark uses **Lazy Evaluation**, which means transformations are not executed immediately when they are defined.

For example:

```python
filtered_df = df.filter(df.amount > 1000)
selected_df = filtered_df.select("customer_id", "amount")
```

Spark does not immediately execute either transformation. Instead, it records the sequence of transformations and builds a logical execution plan.

Execution starts only when an **action** such as:

```python
selected_df.show()
```

is called.

Lazy Evaluation improves performance because Spark can examine the complete chain of transformations before executing it. Spark SQL's optimizer can then optimize the query plan, including operations such as pushing filters closer to the data source and eliminating unnecessary work.

It also prevents unnecessary computation when a transformed DataFrame is created but never used by an action.

Thus, Lazy Evaluation allows Spark to optimize the entire processing pipeline before performing expensive distributed computation.

---

## Q3. Write a Spark command to read a CSV file located at `"data/source.csv"`, ensuring the first row is treated as a header and `inferSchema` is enabled.

```python
df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv("data/source.csv")
)
```

Alternatively:

```python
df = spark.read.csv(
    "data/source.csv",
    header=True,
    inferSchema=True
)
```

Here:

* `header=True` treats the first row as column names.
* `inferSchema=True` asks Spark to determine column data types from the input data instead of reading every column as a string.

For large production datasets, explicitly defining the schema is generally preferable because schema inference requires Spark to inspect the input to determine data types.

---

## Q4. What is the difference between CSV and Parquet in terms of storage (row-based vs. columnar) and why does it matter for performance?

**CSV** is a text-based format that stores records row by row.

Example:

```text
101,Laptop,75000
102,Phone,40000
103,Keyboard,3000
```

**Parquet** is a binary **columnar storage format**, meaning values belonging to the same columns are organized together.

This distinction has an important effect on analytical workloads.

### CSV

* Text-based and human-readable.
* Does not inherently preserve a rich schema in the same way Parquet does.
* Often requires parsing text during reads.
* Reading a subset of columns may still involve processing significant input data.
* Usually produces larger files than compressed columnar formats for analytical datasets.

### Parquet

* Binary and column-oriented.
* Stores schema information.
* Supports efficient column pruning.
* Supports predicate/filter pushdown.
* Supports efficient compression and encoding.

For example, if a dataset contains 50 columns but an analysis requires only 3, Parquet allows Spark to read only the required columns rather than processing all columns.

Therefore, Parquet is generally more efficient for large-scale analytical processing, whereas CSV remains useful for simple data exchange and interoperability.

---

## Q5. Given a DataFrame `df`, write a query to select the columns `product_id` and `price` where the category is `'Electronics'`.

```python
from pyspark.sql.functions import col

electronics_df = (
    df
    .filter(col("category") == "Electronics")
    .select("product_id", "price")
)

electronics_df.show()
```

The `filter()` transformation keeps only records belonging to the `Electronics` category, while `select()` retains only the required columns.

---

## Q6. Write the code to "revise" a DataFrame by renaming the column `old_name` to `new_name` and casting the `price` column from a String to a Double.

```python
from pyspark.sql.functions import col

revised_df = (
    df
    .withColumnRenamed("old_name", "new_name")
    .withColumn("price", col("price").cast("double"))
)
```

`withColumnRenamed()` changes the column name, while `withColumn()` replaces the existing `price` column with its `DoubleType` representation.

The original DataFrame is not modified in place because Spark DataFrames are immutable. Instead, a new DataFrame is returned.

---

## Q7. How does Spark use the Lineage Graph (DAG) to provide fault tolerance if a worker node fails?

Spark maintains information about the transformations used to derive distributed data. This dependency information forms a **lineage graph**, represented as a Directed Acyclic Graph (DAG).

For example:

```text
Input Data
    |
  Filter
    |
  Select
    |
 GroupBy
    |
  Result
```

Instead of relying only on replicated intermediate data, Spark can use this lineage information to determine how lost partitions were produced.

If a worker or executor fails and a required partition is lost, Spark can:

1. Identify the missing partition.
2. Examine its lineage/dependencies.
3. Re-run the necessary tasks and transformations.
4. Recompute the lost partition from available source data or earlier dependencies.

This provides fault tolerance without requiring every intermediate result to be permanently stored.

---

## Q8. Write a query to filter a DataFrame `df_orders` for rows where the status is `'Completed'` AND the amount is greater than `1000`.

```python
from pyspark.sql.functions import col

completed_orders = df_orders.filter(
    (col("status") == "Completed") &
    (col("amount") > 1000)
)

completed_orders.show()
```

Both conditions are combined using the PySpark `&` operator, and each comparison is enclosed in parentheses.

---

## Q9. Explain the concept of Predicate Pushdown in Parquet and how it affects the amount of data loaded into memory.

**Predicate Pushdown** is an optimization where Spark pushes supported filtering conditions toward the data source instead of first reading all available data and filtering it afterward.

Consider:

```python
df = spark.read.parquet("sales.parquet")

filtered_df = df.filter(
    col("region") == "North"
)
```

With Parquet filter pushdown, Spark can use Parquet metadata/statistics to avoid reading data blocks or row groups that cannot satisfy the filter.

Conceptually:

```text
Without Predicate Pushdown:

Parquet File
     |
Read large amount of data
     |
Load/process data
     |
Apply Filter
     |
Result


With Predicate Pushdown:

Parquet File
     |
Evaluate applicable filter using metadata
     |
Skip irrelevant data
     |
Read relevant data
     |
Result
```

This can reduce:

* Disk I/O.
* Data that needs to be decoded and processed.
* Memory pressure.
* Overall query execution time.

Predicate Pushdown is one reason Parquet is highly effective for large analytical workloads.

---

## Q10. Write a code snippet to add a new column `final_price` which is the `base_price` multiplied by `1.18` (18% tax).

```python
from pyspark.sql.functions import col

df = df.withColumn(
    "final_price",
    col("base_price") * 1.18
)
```

The resulting value represents:

```text
final_price = base_price + 18% tax
```

which is equivalent to:

```text
final_price = base_price × 1.18
```

---

## Q11. What is the difference between Transformations and Actions? Provide two examples of each.

Spark operations can broadly be classified into **Transformations** and **Actions**.

### Transformations

Transformations create a new distributed dataset/DataFrame from an existing one.

They are evaluated lazily, meaning Spark records the operation but normally does not execute the full computation immediately.

Examples:

```python
df.filter(col("age") > 18)
```

```python
df.select("name", "age")
```

Other examples include `withColumn()`, `groupBy()`, `join()`, `distinct()`, and `orderBy()`.

### Actions

Actions trigger execution of the transformations required to produce a result.

Examples:

```python
df.show()
```

```python
df.count()
```

Another important example is:

```python
df.collect()
```

which returns all rows to the Driver and should therefore be used carefully with large datasets.

### Difference

| Transformations                  | Actions                                  |
| -------------------------------- | ---------------------------------------- |
| Create a new DataFrame/RDD       | Trigger computation                      |
| Evaluated lazily                 | Cause the required execution plan to run |
| Build the processing plan        | Produce/display/return results           |
| Examples: `filter()`, `select()` | Examples: `show()`, `count()`            |

---

## Q12. Write the Spark command to load a Parquet file from `"path/to/input"`, filter out any rows where `user_id` is null, and save the result as a CSV at `"path/to/output"`.

```python
from pyspark.sql.functions import col

df = spark.read.parquet("path/to/input")

clean_df = df.filter(
    col("user_id").isNotNull()
)

(
    clean_df.write
    .mode("overwrite")
    .option("header", "true")
    .csv("path/to/output")
)
```

This pipeline performs three operations:

1. Reads the Parquet dataset.
2. Removes records where `user_id` is null.
3. Writes the cleaned result as CSV.

`mode("overwrite")` allows an existing output directory to be replaced.

Spark normally writes distributed output as a directory containing one or more `part-*` files rather than as a single CSV file.

---

## Q13. In Spark Architecture, what is the difference between Client Mode and Cluster Mode?

Client Mode and Cluster Mode describe where the Spark **Driver** runs when an application is submitted to a cluster.

### Client Mode

In Client Mode, the Driver runs on the machine/process from which the Spark application is submitted, while executors run on cluster worker nodes.

```text
Client Machine
     |
   Driver
     |
Cluster Manager
     |
 Executors
```

Client Mode is useful for interactive workloads because the Driver remains close to the submitting client and application output is easily accessible.

However, the client must generally remain available while the application runs.

### Cluster Mode

In Cluster Mode, the Driver is launched within the cluster rather than remaining on the submitting client.

```text
Submission Client
       |
Cluster Manager
       |
     Driver
       |
   Executors
```

The submitting client can disconnect after successful submission without hosting the Driver for the lifetime of the application.

Cluster Mode is therefore commonly suited to long-running or production jobs.

### Main Difference

| Client Mode                                     | Cluster Mode                                       |
| ----------------------------------------------- | -------------------------------------------------- |
| Driver runs on/with the submitting client       | Driver runs inside the cluster                     |
| Convenient for interactive use and debugging    | Better suited to production/batch execution        |
| Client connectivity is important for the Driver | Submission client does not host the running Driver |

---

## Q14. Write a query to filter a dataset for rows where the region is `'North'` OR the priority is `'High'`.

```python
from pyspark.sql.functions import col

filtered_df = df.filter(
    (col("region") == "North") |
    (col("priority") == "High")
)

filtered_df.show()
```

The PySpark `|` operator represents the logical **OR** condition between the two column expressions.

A row is retained if either:

* `region == "North"`

**OR**

* `priority == "High"`

is true.

---

## Q15. When exploring a dataset, why is it safer to use `.show(5)` instead of `.collect()` on a multi-terabyte dataset?

`.collect()` returns **all rows of the DataFrame to the Driver process**.

For a multi-terabyte dataset:

```python
df.collect()
```

would attempt to transfer a potentially enormous result from executors to the Driver. This can cause:

* Excessive network transfer.
* Very high Driver memory consumption.
* Driver out-of-memory errors.
* Application failure.

For dataset exploration:

```python
df.show(5)
```

is much safer because it displays only a small number of rows required for inspection instead of returning the complete dataset to the Driver.

Therefore:

```python
df.show(5)
```

should be preferred for quick inspection of large distributed datasets.

`collect()` should only be used when the programmer knows that the complete result is sufficiently small to fit safely in Driver memory.

---

# Conclusion

This assignment demonstrates the fundamental concepts required to build efficient Apache Spark data-processing pipelines.

The major concepts covered include:

* Spark Driver, Cluster Manager, and Executors.
* Client and Cluster execution modes.
* Lazy Evaluation.
* DAG and lineage-based fault tolerance.
* Transformations and Actions.
* DataFrame filtering and column selection.
* Schema inference and explicit schema handling.
* Column renaming and type casting.
* Null-value handling.
* CSV and Parquet processing.
* Columnar storage.
* Predicate Pushdown.
* Safe handling of large distributed datasets.
* End-to-end read → transform → filter → write pipelines.

Understanding these concepts is essential for developing Spark applications that are scalable, fault-tolerant, and efficient when processing large datasets.
