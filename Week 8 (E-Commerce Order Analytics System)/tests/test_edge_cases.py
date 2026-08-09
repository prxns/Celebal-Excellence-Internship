import unittest
import pandas as pd
from src.cleaning import check_referential_integrity, validate_business_rules


class EdgeCaseTests(unittest.TestCase):
    def setUp(self):
        self.orders = pd.DataFrame({"order_id": ["O1"], "order_date": ["2025-01-01 10:00:00"]})

    def test_orphan_order_item_is_found(self):
        items = pd.DataFrame({"item_id": ["I1"], "order_id": ["MISSING"], "quantity": [1], "discount_percent": [0]})
        self.assertEqual(check_referential_integrity(items, self.orders)["item_id"].tolist(), ["I1"])

    def test_discount_greater_than_100_is_flagged(self):
        items = pd.DataFrame({"item_id": ["I1"], "order_id": ["O1"], "quantity": [1], "discount_percent": [110]})
        self.assertIn("discount_out_of_range", [issue["issue"] for issue in validate_business_rules(items, self.orders)])

    def test_zero_quantity_is_flagged(self):
        items = pd.DataFrame({"item_id": ["I1"], "order_id": ["O1"], "quantity": [0], "discount_percent": [0]})
        self.assertIn("zero_quantity", [issue["issue"] for issue in validate_business_rules(items, self.orders)])

    def test_future_order_is_flagged(self):
        future_orders = pd.DataFrame({"order_id": ["O1"], "order_date": ["2099-01-01 10:00:00"]})
        items = pd.DataFrame({"item_id": ["I1"], "order_id": ["O1"], "quantity": [1], "discount_percent": [0]})
        self.assertIn("future_order_date", [issue["issue"] for issue in validate_business_rules(items, future_orders)])


if __name__ == "__main__":
    unittest.main()
