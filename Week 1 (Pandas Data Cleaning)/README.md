# E-Commerce Data Cleaning with Pandas 

## Objective
A foundational Python project focused on performing basic data exploration, cleaning, and feature engineering using the `pandas` library within a Jupyter Notebook environment.

## Dataset
The project utilizes the [Shopping Dataset](https://www.kaggle.com/datasets/anvitkumar/shopping-dataset) from Kaggle, consisting of real-world e-commerce product data. 

## Key Operations Performed
* **Data Ingestion:** Loaded raw CSV data into a Pandas DataFrame.
* **Data Exploration:** Audited data structures using `.head()`, `.tail()`, `.info()`, and shape analysis.
* **Data Cleaning (Nulls):** Identified missing values, dropped records missing critical data (`title`, `final_price`), and imputed remaining missing categorical fields with `'Unknown'`.
* **Data Deduplication:** Removed redundant records using `.drop_duplicates()`.
* **Transformations & Filtering:** Filtered the dataset to isolate highly-rated products (`rating > 4.0`) and selected specific columns for analysis.
* **Feature Engineering:** Derived a new `product_summary` text column by concatenating existing string columns.
* **Export:** Saved the processed and cleaned dataset to a new CSV file for downstream modeling or visualization.