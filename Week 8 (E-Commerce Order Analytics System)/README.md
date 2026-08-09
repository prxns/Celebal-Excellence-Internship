# CommercePulse - E-Commerce Order Analytics System

> **Week 8 Internship Mini Project Submission** - Celebal Technologies

An end-to-end local analytics project completed as part of the Week 8 Celebal Technologies internship mini project. It generates deliberately imperfect e-commerce data, cleans and validates it with Python/Pandas, loads curated data into SQLite, and serves business reports through SQL and a command-line interface.

## Submission details

| Field | Details |
|---|---|
| Submitted by | Pranshu Rawat |
| College / University | DIT University |
| Program / Branch | B.Tech (CSE) |
| Student Id | CT_CSI_DE_1095 |
| Internship Organization | Celebal Technologies |
| Project Type | Week 8 Internship Mini Project |
| Submission Date | 10 August 2026 |

## Project overview

CommercePulse simulates the work of a data analyst or data engineer handling e-commerce orders from multiple imperfect source systems. The project transforms raw CSV data into clean, validated, analytics-ready tables and uses SQL to derive customer, revenue, retention, and product insights.

## Features and assignment coverage

- Four realistic CSV sources with 500+ rows each and intentional data-quality issues.
- Pandas cleaning for dates, customer IDs, product names, and emails.
- Referential-integrity and business-rule validation with an issue report.
- SQLite warehouse with keys, indexes, SQL joins, CTEs, window functions, ranking, segmentation, cohort retention, and market-basket analysis.
- CLI summaries for daily, weekly, and monthly date ranges.
- Edge-case tests for invalid references, discounts, zero quantities, and future dates.

## Technology stack

- **Python** - Data generation, workflow orchestration, CLI reporting, and tests
- **Pandas** - Data cleaning and validation
- **SQLite / SQL** - Relational data storage and business analytics
- **Git** - Version control

## Quick start

```powershell
python -m pip install -r requirements.txt
python -m src.pipeline
python -m src.cli --report monthly --start 2025-01-01 --end 2025-12-31
python -m unittest discover -s tests -v
```

Running the pipeline writes raw CSV files to `data/raw/`, cleaned data to `data/cleaned/`, issue reports to `reports/`, and the SQLite database to `data/commercepulse.db`.

## Project layout

```text
src/generate_data.py     Synthetic source data with intentional defects
src/cleaning.py          Cleaning and validation functions
src/database.py          SQLite schema, curated load, and analysis runner
src/analytics.sql        Required SQL analysis queries
src/cli.py               Dynamic reporting command-line tool
src/pipeline.py          One-command end-to-end execution
tests/test_edge_cases.py Assignment-required edge-case tests
```

## Data pipeline

```text
Raw CSV data
    -> Pandas cleaning and validation
    -> Cleaned CSV data + data-quality issue report
    -> SQLite analytics database
    -> SQL business analysis reports + CLI summary
```

## Important design choices

Revenue is calculated as `quantity * unit_price * (1 - discount_percent / 100)`. Negative quantities represent returned items and are retained for auditability; return-rate queries use them separately from purchased items. Orders whose customer ID is missing remain `NULL` rather than being assigned to a fake customer.

## Example CLI command

```powershell
python -m src.cli --report weekly --start 2025-06-01 --end 2025-06-30
```

The CLI returns total orders, revenue, unique customers, top three products, and percentage changes from an equivalent preceding period. Invalid dates and empty ranges are handled safely.

## Validation and test coverage

The project includes automated tests for the following critical edge cases:

- An `order_item` references an order that does not exist.
- A discount percentage is greater than 100.
- An order item has quantity equal to zero.
- An order has a future date.

Run all tests with:

```powershell
python -m unittest discover -s tests -v
```

## Key business insights generated

- Revenue contribution by product category
- Top customers by total order value
- Monthly order volume and year-over-year revenue comparison
- Regional running revenue totals
- Customer order gaps and at-risk customers
- Customer value segmentation and LTV quartiles
- Product return rates and products bought together
- Registration-cohort retention for months 0 through 3

## Author

- **Pranshu Rawat**
- **DIT University**
- **Week 8 Internship Mini Project - Celebal Technologies**
