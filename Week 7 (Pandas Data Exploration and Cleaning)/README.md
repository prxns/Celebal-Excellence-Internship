# Week 7 - Pandas Data Exploration and Cleaning

## Objective

The objective of this assignment is to learn the basics of Python programming using the Pandas library and perform basic data exploration and data cleaning operations on a CSV dataset.

---

## Dataset Used

- **Dataset Name:** Sample - Superstore.csv
- **Format:** CSV (Comma Separated Values)

---

## Tools and Technologies

- Python 3.11
- Pandas Library
- Jupyter Notebook (.ipynb)
- Visual Studio Code

---

## Tasks Performed

### 1. Load Dataset
- Imported the Pandas library.
- Loaded the CSV dataset into a Pandas DataFrame using `read_csv()`.

### 2. Explore the Dataset
- Displayed the first five rows using `head()`.
- Displayed the last five rows using `tail()`.
- Checked the dataset shape.
- Listed all column names.
- Displayed data types of all columns.

### 3. Handle Missing Values
- Identified missing values using `isnull().sum()`.
- Filled missing values using `fillna()`.

### 4. Perform Basic Operations
- Filtered rows based on Sales value.
- Selected specific columns from the dataset.

### 5. Remove Duplicate Records
- Removed duplicate rows using `drop_duplicates()`.

### 6. Create a Derived Column
- Created a new column named **total_amount** using the formula:

```
total_amount = Sales × Quantity
```

### 7. Save Cleaned Dataset
- Exported the cleaned DataFrame as **cleaned_superstore.csv**.

---

## Files Included

```
Week7_Pandas_Assignment/
│
├── Week7_Assignment.ipynb
├── Sample - Superstore.csv
├── cleaned_superstore.csv
└── README.md
```

---

## Expected Output

- Jupyter Notebook containing all code and outputs.
- Cleaned CSV dataset.
- Proper data exploration and cleaning.
- Derived column (`total_amount`) added successfully.

---

## Conclusion

This assignment demonstrates the basic use of the Pandas library for data loading, exploration, cleaning, filtering, duplicate removal, feature creation, and exporting processed data. It provides a practical understanding of fundamental data preprocessing techniques commonly used in data analysis and machine learning workflows.