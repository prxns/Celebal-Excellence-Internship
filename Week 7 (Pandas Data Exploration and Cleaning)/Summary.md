# Celebal Week 7 Assignment Summary

## Week 7 - Pandas Data Exploration and Cleaning

### Objective

The objective of this assignment was to learn the basics of the Pandas library and perform data exploration and data cleaning on a CSV dataset.

### Summary

In this assignment, the **Sample - Superstore** dataset was loaded into a Pandas DataFrame using the `read_csv()` function. The dataset was explored by displaying the first and last five rows, checking its dimensions, listing the column names, and examining the data types of each column.

Missing values were identified using `isnull().sum()` and handled using the `fillna()` method. Basic data manipulation operations were performed, including filtering rows based on sales values and selecting specific columns from the dataset. Duplicate records were removed using `drop_duplicates()` to improve data quality.

A new derived column named **total_amount** was created by multiplying the **Sales** and **Quantity** columns. Finally, the cleaned dataset was exported as **cleaned_superstore.csv** for future analysis.

### Learning Outcomes

- Learned how to load a CSV file using Pandas.
- Explored dataset structure and information.
- Identified and handled missing values.
- Filtered rows and selected required columns.
- Removed duplicate records.
- Created a new calculated column.
- Exported the cleaned dataset to a new CSV file.

### Conclusion

This assignment provided practical experience with fundamental data preprocessing techniques using the Pandas library. These operations are essential for preparing datasets before performing data analysis, visualization, or machine learning tasks.