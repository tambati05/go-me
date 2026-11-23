"""Tests cover validation, reconciliation, and safe reruns."""

import csv
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from analytics_pipeline import run_pipeline
from analytics_pipeline.pipeline import money_to_cents, normalized_date


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.orders = self.base / "orders.csv"
        self.customers = self.base / "customers.csv"
        self.db = self.base / "warehouse.db"
        self.reports = self.base / "reports"
        self.customers.write_text("customer_id,segment\nC001,Small Business\n", encoding="utf-8")

    def run_it(self):
        return run_pipeline(self.orders, self.customers, self.db, self.reports)

    def test_accept_reject_and_revenue(self):
        self.orders.write_text(
            "order_id,order_date,customer_id,region,product_category,quantity,unit_price\n"
            "A1,10/01/2026,C001,South,Software,2,12.50\n"
            "A1,2026-10-01,C001,South,Software,2,12.50\n"
            "A2,2026-10-03,C001,South,Hardware,0,10.00\n"
            "A3,2026-10-04,C404,South,Software,1,5.00\n"
            "A4,2026-10-05,C001,North,Services,1,2.25\n",
            encoding="utf-8",
        )
        result = self.run_it()
        self.assertEqual((result["source_records"], result["accepted_records"], result["rejected_records"]), (5, 2, 3))
        self.assertEqual(result["total_revenue_usd"], "27.25")
        with sqlite3.connect(self.db) as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0], 2)
            self.assertEqual(conn.execute("SELECT order_date FROM orders WHERE order_id='A1'").fetchone()[0], "2026-10-01")
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM rejected_orders").fetchone()[0], 3)
        with (self.reports / "rejected_orders.csv").open(newline="") as f:
            reasons = {row["reason"] for row in csv.DictReader(f)}
        self.assertEqual(reasons, {"duplicate order_id", "quantity must be positive", "unknown customer_id"})
        self.assertIn("Next steps", (self.reports / "status_report.md").read_text())
        self.assertEqual(json.loads((self.reports / "summary.json").read_text())["accepted_records"], 2)

    def test_idempotent_full_refresh(self):
        self.orders.write_text(
            "order_id,order_date,customer_id,region,product_category,quantity,unit_price\n"
            "A1,2026-10-01,C001,South,Software,1,10.00\n",
            encoding="utf-8",
        )
        self.run_it()
        self.run_it()
        with sqlite3.connect(self.db) as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0], 1)

    def test_missing_schema_prevents_database_creation(self):
        self.orders.write_text("order_id,order_date\nA1,2026-10-01\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "missing columns"):
            self.run_it()
        self.assertFalse(self.db.exists())

    def test_money_and_date_validation(self):
        self.assertEqual(money_to_cents("12.50"), 1250)
        self.assertEqual(normalized_date("10/03/2026"), "2026-10-03")
        for bad in ("NaN", "0", "-1", "1.234", "notmoney"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                money_to_cents(bad)
        with self.assertRaises(ValueError):
            normalized_date("2026-13-99")


if __name__ == "__main__":
    unittest.main()
