"""SQLite warehouse setup, curated-data loading, and SQL analysis execution."""

from __future__ import annotations

import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "commercepulse.db"
SCHEMA = """
PRAGMA foreign_keys = ON;
DROP VIEW IF EXISTS order_line_revenue;
DROP TABLE IF EXISTS order_items; DROP TABLE IF EXISTS orders; DROP TABLE IF EXISTS products; DROP TABLE IF EXISTS customers;
CREATE TABLE customers (customer_id TEXT PRIMARY KEY, customer_name TEXT NOT NULL, email TEXT NOT NULL, registration_date TEXT NOT NULL, customer_type TEXT NOT NULL);
CREATE TABLE products (product_id TEXT PRIMARY KEY, product_name TEXT NOT NULL, category TEXT NOT NULL, subcategory TEXT NOT NULL, cost_price REAL NOT NULL CHECK(cost_price >= 0));
CREATE TABLE orders (order_id TEXT PRIMARY KEY, customer_id TEXT, order_date TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('PLACED','SHIPPED','DELIVERED','CANCELLED','RETURNED')), region_code TEXT NOT NULL, FOREIGN KEY(customer_id) REFERENCES customers(customer_id));
CREATE TABLE order_items (item_id TEXT PRIMARY KEY, order_id TEXT NOT NULL, product_id TEXT NOT NULL, quantity INTEGER NOT NULL, unit_price REAL NOT NULL CHECK(unit_price >= 0), discount_percent REAL NOT NULL CHECK(discount_percent BETWEEN 0 AND 100), FOREIGN KEY(order_id) REFERENCES orders(order_id), FOREIGN KEY(product_id) REFERENCES products(product_id));
CREATE INDEX idx_orders_date ON orders(order_date); CREATE INDEX idx_orders_customer ON orders(customer_id); CREATE INDEX idx_items_order ON order_items(order_id); CREATE INDEX idx_items_product ON order_items(product_id);
CREATE VIEW order_line_revenue AS SELECT oi.item_id, oi.order_id, oi.product_id, oi.quantity, oi.unit_price, oi.discount_percent, o.customer_id, o.order_date, o.status, o.region_code, p.product_name, p.category, (oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS revenue FROM order_items oi JOIN orders o ON o.order_id = oi.order_id JOIN products p ON p.product_id = oi.product_id;
"""


def build_database(cleaned_dir: Path | None = None, db_path: Path | None = None) -> Path:
    cleaned_dir = cleaned_dir or ROOT / "data" / "cleaned"
    db_path = db_path or DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    frames = {name: pd.read_csv(cleaned_dir / f"{name}.csv") for name in ("customers", "products", "orders", "order_items")}
    frames["orders"]["customer_id"] = frames["orders"]["customer_id"].where(frames["orders"]["customer_id"].notna(), None)
    with sqlite3.connect(db_path) as connection:
        connection.executescript(SCHEMA)
        for table in ("customers", "products", "orders", "order_items"):
            frames[table].to_sql(table, connection, if_exists="append", index=False)
        connection.commit()
    return db_path


def run_analyses(db_path: Path | None = None, output_dir: Path | None = None) -> list[Path]:
    db_path = db_path or DB_PATH
    output_dir = output_dir or ROOT / "reports" / "sql_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)
    sql = (ROOT / "src" / "analytics.sql").read_text(encoding="utf-8")
    blocks = [block.strip() for block in sql.split("-- QUERY:") if block.strip()]
    outputs: list[Path] = []
    with sqlite3.connect(db_path) as connection:
        for block in blocks:
            name, query = block.split("\n", 1)
            frame = pd.read_sql_query(query, connection)
            target = output_dir / f"{name.strip()}.csv"
            frame.to_csv(target, index=False)
            outputs.append(target)
    return outputs
