"""Generate realistic e-commerce CSV data with intentional inconsistencies."""

from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
STATUSES = ["PLACED", "SHIPPED", "DELIVERED", "CANCELLED", "RETURNED"]
REGIONS = ["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"]
CATEGORIES = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers"],
    "Home": ["Cookware", "Lighting", "Furniture", "Decor"],
    "Books": ["Fiction", "Business", "Science", "Biography"],
}
FIRST_NAMES = ["Aarav", "Vivaan", "Aditya", "Arjun", "Ishaan", "Ananya", "Diya", "Kavya", "Meera", "Riya"]
LAST_NAMES = ["Sharma", "Verma", "Patel", "Reddy", "Gupta", "Iyer", "Khan", "Singh", "Das", "Nair"]
WORDS = ["Nova", "Urban", "Prime", "Swift", "Aura", "Elite", "Classic", "Eco", "Fusion", "Zen"]


def _write_csv(path: Path, headers: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def generate_data(seed: int = 42, customers_count: int = 600, products_count: int = 550,
                  orders_count: int = 1400, items_count: int = 4200) -> dict[str, int]:
    """Create four source files. Each table has at least 500 records."""
    random.seed(seed)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now().replace(microsecond=0)
    start = now - timedelta(days=760)

    customers = []
    for i in range(1, customers_count + 1):
        first_name, last_name = random.choice(FIRST_NAMES), random.choice(LAST_NAMES)
        email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
        if i <= round(customers_count * 0.02):
            email = email.replace("@", "", 1) if i % 2 else email.split("@")[0] + "@"
        customers.append({
            "customer_id": f"C{i:05d}", "customer_name": f"{first_name} {last_name}", "email": email,
            "registration_date": (start - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
            "customer_type": random.choices(["REGULAR", "PREMIUM", "VIP"], [0.70, 0.23, 0.07])[0],
        })

    products = []
    category_pairs = [(category, subcategory) for category, subs in CATEGORIES.items() for subcategory in subs]
    for i in range(1, products_count + 1):
        category, subcategory = category_pairs[(i - 1) % len(category_pairs)]
        product_name = f"{random.choice(WORDS)} {subcategory}"
        if i % 23 == 0:
            product_name = f"  {product_name.upper()}  "
        elif i % 31 == 0:
            product_name = product_name.swapcase()
        products.append({"product_id": f"P{i:05d}", "product_name": product_name,
                         "category": category, "subcategory": subcategory,
                         "cost_price": round(random.uniform(80, 5000), 2)})

    order_ids = [f"O{i:06d}" for i in range(1, orders_count + 1)]
    orders = []
    for i, order_id in enumerate(order_ids, start=1):
        order_date = start + timedelta(days=random.randint(0, 759), seconds=random.randint(0, 86399))
        date_value = order_date.strftime("%d-%m-%Y %H:%M:%S") if i % 47 == 0 else order_date.strftime("%Y-%m-%d %H:%M:%S")
        customer_id = "" if i <= round(orders_count * 0.05) else random.choice(customers)["customer_id"]
        orders.append({"order_id": order_id, "customer_id": customer_id, "order_date": date_value,
                       "status": random.choices(STATUSES, [0.08, 0.13, 0.64, 0.08, 0.07])[0],
                       "region_code": random.choice(REGIONS)})

    items = []
    for i in range(1, items_count + 1):
        product = random.choice(products)
        quantity = random.randint(1, 5)
        if i <= round(items_count * 0.03):
            quantity = -quantity
        items.append({"item_id": f"I{i:07d}", "order_id": random.choice(order_ids),
                      "product_id": product["product_id"], "quantity": quantity,
                      "unit_price": round(random.uniform(1.2, 1.8) * float(product["cost_price"]), 2),
                      "discount_percent": round(random.choice([0, 0, 5, 10, 15, 20, 25]), 2)})

    _write_csv(RAW_DIR / "customers.csv", list(customers[0]), customers)
    _write_csv(RAW_DIR / "products.csv", list(products[0]), products)
    _write_csv(RAW_DIR / "orders.csv", list(orders[0]), orders)
    _write_csv(RAW_DIR / "order_items.csv", list(items[0]), items)
    return {"customers": len(customers), "products": len(products), "orders": len(orders), "order_items": len(items)}


if __name__ == "__main__":
    print(generate_data())
