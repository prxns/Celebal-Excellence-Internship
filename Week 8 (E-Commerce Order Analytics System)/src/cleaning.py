"""Pandas cleaning, validation, and data-quality reporting."""

from __future__ import annotations

import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def clean_orders(orders: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    cleaned = orders.copy()
    issues: list[dict] = []
    cleaned["customer_id"] = cleaned["customer_id"].replace(r"^\s*$", pd.NA, regex=True)
    missing = cleaned["customer_id"].isna()
    for order_id in cleaned.loc[missing, "order_id"]:
        issues.append({"table": "orders", "record_id": order_id, "issue": "missing_customer_id", "severity": "warning"})
    parsed = pd.to_datetime(cleaned["order_date"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
    alternate_format = parsed.isna()
    fallback = pd.to_datetime(cleaned.loc[alternate_format, "order_date"], format="%d-%m-%Y %H:%M:%S", errors="coerce")
    parsed.loc[parsed.isna()] = fallback
    for order_id in cleaned.loc[alternate_format & parsed.notna(), "order_id"]:
        issues.append({"table": "orders", "record_id": order_id, "issue": "nonstandard_date_format_corrected", "severity": "warning"})
    invalid = parsed.isna()
    for order_id in cleaned.loc[invalid, "order_id"]:
        issues.append({"table": "orders", "record_id": order_id, "issue": "unparseable_order_date", "severity": "error"})
    cleaned["order_date"] = parsed.dt.strftime("%Y-%m-%d %H:%M:%S")
    return cleaned, issues


def clean_products(products: pd.DataFrame) -> pd.DataFrame:
    cleaned = products.copy()
    cleaned["product_name"] = cleaned["product_name"].astype(str).str.strip().str.title()
    return cleaned


def validate_emails(customers: pd.DataFrame) -> list[str]:
    return customers.loc[~customers["email"].fillna("").str.match(EMAIL_PATTERN), "customer_id"].tolist()


def check_referential_integrity(order_items: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    valid_order_ids = set(orders["order_id"])
    return order_items.loc[~order_items["order_id"].isin(valid_order_ids)].copy()


def validate_business_rules(order_items: pd.DataFrame, orders: pd.DataFrame) -> list[dict]:
    issues: list[dict] = []
    for _, row in order_items.loc[order_items["discount_percent"].notna() & ((order_items["discount_percent"] < 0) | (order_items["discount_percent"] > 100))].iterrows():
        issues.append({"table": "order_items", "record_id": row["item_id"], "issue": "discount_out_of_range", "severity": "error"})
    for _, row in order_items.loc[order_items["quantity"] == 0].iterrows():
        issues.append({"table": "order_items", "record_id": row["item_id"], "issue": "zero_quantity", "severity": "warning"})
    dates = pd.to_datetime(orders["order_date"], errors="coerce")
    for order_id in orders.loc[dates > pd.Timestamp.now(), "order_id"]:
        issues.append({"table": "orders", "record_id": order_id, "issue": "future_order_date", "severity": "error"})
    return issues


def clean_and_validate(raw_dir: Path | None = None, cleaned_dir: Path | None = None, reports_dir: Path | None = None) -> dict:
    raw_dir = raw_dir or ROOT / "data" / "raw"
    cleaned_dir = cleaned_dir or ROOT / "data" / "cleaned"
    reports_dir = reports_dir or ROOT / "reports"
    cleaned_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    orders = pd.read_csv(raw_dir / "orders.csv", dtype={"customer_id": "string"})
    items = pd.read_csv(raw_dir / "order_items.csv")
    products = pd.read_csv(raw_dir / "products.csv")
    customers = pd.read_csv(raw_dir / "customers.csv")
    clean_order_data, issues = clean_orders(orders)
    clean_product_data = clean_products(products)
    invalid_emails = validate_emails(customers)
    issues.extend({"table": "customers", "record_id": cid, "issue": "invalid_email", "severity": "warning"} for cid in invalid_emails)
    orphan_items = check_referential_integrity(items, clean_order_data)
    issues.extend({"table": "order_items", "record_id": row.item_id, "issue": "orphan_order_id", "severity": "error"} for row in orphan_items.itertuples())
    issues.extend(validate_business_rules(items, clean_order_data))
    for name, frame in {"orders": clean_order_data, "order_items": items, "products": clean_product_data, "customers": customers}.items():
        frame.to_csv(cleaned_dir / f"{name}.csv", index=False)
    issue_frame = pd.DataFrame(issues, columns=["table", "record_id", "issue", "severity"])
    issue_frame.to_csv(reports_dir / "data_quality_issues.csv", index=False)
    return {"issues": len(issue_frame), "invalid_emails": len(invalid_emails), "orphan_items": len(orphan_items)}
