"""Command-line reporting for daily, weekly, and monthly business summaries."""

from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import datetime, timedelta
from .database import DB_PATH


def _metrics(connection: sqlite3.Connection, start: str, end: str) -> tuple[int, float, int]:
    return connection.execute("""SELECT COUNT(DISTINCT order_id), COALESCE(SUM(revenue), 0), COUNT(DISTINCT customer_id) FROM order_line_revenue WHERE date(order_date) BETWEEN date(?) AND date(?)""", (start, end)).fetchone()


def generate_report(report_type: str, start: str, end: str, db_path=DB_PATH) -> str:
    if report_type not in {"daily", "weekly", "monthly"}:
        raise ValueError("report type must be daily, weekly, or monthly")
    try:
        start_date, end_date = datetime.fromisoformat(start).date(), datetime.fromisoformat(end).date()
    except ValueError as error:
        raise ValueError("dates must use YYYY-MM-DD") from error
    if end_date < start_date:
        raise ValueError("end date cannot be before start date")
    span = (end_date - start_date).days + 1
    previous_end, previous_start = start_date - timedelta(days=1), start_date - timedelta(days=span)
    with sqlite3.connect(db_path) as connection:
        orders, revenue, customers = _metrics(connection, start, end)
        prior_orders, prior_revenue, prior_customers = _metrics(connection, str(previous_start), str(previous_end))
        top = connection.execute("""SELECT product_name, ROUND(SUM(revenue), 2) AS revenue FROM order_line_revenue WHERE date(order_date) BETWEEN date(?) AND date(?) GROUP BY product_id, product_name ORDER BY revenue DESC LIMIT 3""", (start, end)).fetchall()
    change = "N/A" if prior_revenue == 0 else f"{((revenue - prior_revenue) * 100 / prior_revenue):.2f}%"
    products = "\n".join(f"  {index}. {name} - Rs. {value:,.2f}" for index, (name, value) in enumerate(top, 1)) or "  No products found"
    return (f"{report_type.title()} CommercePulse Report ({start} to {end})\n"
            f"{'=' * 55}\nTotal orders: {orders}\nRevenue: Rs. {revenue:,.2f}\nUnique customers: {customers}\n"
            f"Revenue change vs previous comparable period: {change}\nTop 3 products:\n{products}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an e-commerce summary report.")
    parser.add_argument("--report", required=True, choices=["daily", "weekly", "monthly"])
    parser.add_argument("--start", required=True, help="Start date: YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="End date: YYYY-MM-DD")
    args = parser.parse_args()
    try:
        print(generate_report(args.report, args.start, args.end))
    except (ValueError, sqlite3.Error) as error:
        print(f"Report failed: {error}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
