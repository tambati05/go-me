"""CSV -> validation -> SQLite -> reporting pipeline (Python standard library only)."""

from __future__ import annotations

import csv
import json
import sqlite3
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

CUSTOMER_COLUMNS = {"customer_id", "segment"}
ORDER_COLUMNS = {
    "order_id", "order_date", "customer_id", "region", "product_category",
    "quantity", "unit_price",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    segment TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    order_date TEXT NOT NULL,
    customer_id TEXT NOT NULL REFERENCES customers(customer_id),
    region TEXT NOT NULL,
    product_category TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents > 0)
);
CREATE TABLE IF NOT EXISTS rejected_orders (
    source_row INTEGER NOT NULL,
    order_id TEXT,
    reason TEXT NOT NULL
);
"""


def read_csv(path: Path, required_columns: set[str]):
    """Read rows and reject malformed schemas (instead of silently losing fields)."""
    with path.open("r", newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        headers = set(reader.fieldnames or [])
        missing = required_columns - headers
        if missing:
            raise ValueError(f"{path.name} is missing columns: {', '.join(sorted(missing))}")
        for source_row, row in enumerate(reader, start=2):
            yield source_row, row


def normalized_date(raw: str) -> str:
    """Normalize two accepted date formats into an ISO date."""
    for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            pass
    raise ValueError("invalid order_date")


def money_to_cents(raw: str) -> int:
    try:
        amount = Decimal(raw)
    except (InvalidOperation, TypeError):
        raise ValueError("invalid unit_price") from None
    if not amount.is_finite() or amount <= 0 or amount.as_tuple().exponent < -2:
        raise ValueError("unit_price must be a positive amount with at most two decimals")
    return int(amount * 100)


def validate_order(row: dict, customers: set[str], seen_orders: set[str]) -> tuple:
    """Validate each source row before loading it into the reporting database."""
    order_id = (row.get("order_id") or "").strip()
    customer_id = (row.get("customer_id") or "").strip()
    region = (row.get("region") or "").strip()
    category = (row.get("product_category") or "").strip()

    if not order_id:
        raise ValueError("missing order_id")
    if order_id in seen_orders:
        raise ValueError("duplicate order_id")
    if customer_id not in customers:
        raise ValueError("unknown customer_id")
    if not region or not category:
        raise ValueError("missing region or product_category")

    date = normalized_date((row.get("order_date") or "").strip())
    try:
        quantity = int((row.get("quantity") or "").strip())
    except ValueError:
        raise ValueError("invalid quantity") from None
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    unit_price_cents = money_to_cents((row.get("unit_price") or "").strip())
    return (order_id, date, customer_id, region, category, quantity, unit_price_cents)


def export_csv(path: Path, headers: list[str], rows: list[tuple | dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)


def run_pipeline(orders_csv: str | Path, customers_csv: str | Path,
                 db_path: str | Path, reports_dir: str | Path) -> dict:
    """Load synthetic records and generate auditable metrics; safe to rerun."""
    orders_csv = Path(orders_csv)
    customers_csv = Path(customers_csv)
    db_path = Path(db_path)
    reports_dir = Path(reports_dir)

    # Validate source files in memory before changing any database tables.
    customer_records = {}
    for _, row in read_csv(customers_csv, CUSTOMER_COLUMNS):
        customer_id = (row["customer_id"] or "").strip()
        segment = (row["segment"] or "").strip()
        if not customer_id or not segment:
            raise ValueError("customer data contains a blank id or segment")
        if customer_id in customer_records:
            raise ValueError(f"duplicate customer_id: {customer_id}")
        customer_records[customer_id] = segment

    accepted: list[tuple] = []
    rejected: list[tuple] = []
    seen_orders: set[str] = set()
    for source_row, row in read_csv(orders_csv, ORDER_COLUMNS):
        order_id = (row.get("order_id") or "").strip()
        try:
            record = validate_order(row, set(customer_records), seen_orders)
        except ValueError as error:
            rejected.append((source_row, order_id, str(error)))
            continue
        accepted.append(record)
        seen_orders.add(order_id)

    db_path.parent.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA)
        # Full-refresh demo pipeline: reruns don't multiply rows.
        with connection:
            connection.execute("DELETE FROM rejected_orders")
            connection.execute("DELETE FROM orders")
            connection.execute("DELETE FROM customers")
            connection.executemany(
                "INSERT INTO customers (customer_id, segment) VALUES (?, ?)",
                sorted(customer_records.items()),
            )
            connection.executemany(
                """INSERT INTO orders (
                    order_id, order_date, customer_id, region, product_category,
                    quantity, unit_price_cents
                ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                accepted,
            )
            connection.executemany(
                "INSERT INTO rejected_orders (source_row, order_id, reason) VALUES (?, ?, ?)",
                rejected,
            )
        revenue_rows = connection.execute("""
            SELECT product_category, COUNT(*) AS order_count,
                   SUM(quantity) AS units_sold,
                   SUM(quantity * unit_price_cents) AS revenue_cents
            FROM orders
            GROUP BY product_category
            ORDER BY product_category
        """).fetchall()
        total_revenue_cents = connection.execute(
            "SELECT COALESCE(SUM(quantity * unit_price_cents), 0) FROM orders"
        ).fetchone()[0]

    total = len(accepted) + len(rejected)
    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_records": total,
        "accepted_records": len(accepted),
        "rejected_records": len(rejected),
        "acceptance_rate_percent": round((100 * len(accepted) / total), 2) if total else 0,
        "total_revenue_usd": f"{Decimal(total_revenue_cents) / 100:.2f}",
        "status": "completed_with_rejections" if rejected else "completed",
    }

    export_csv(reports_dir / "rejected_orders.csv",
               ["source_row", "order_id", "reason"], rejected)
    export_csv(reports_dir / "revenue_by_category.csv",
               ["product_category", "order_count", "units_sold", "revenue_usd"],
               [(category, count, units, f"{Decimal(cents) / 100:.2f}")
                for category, count, units, cents in revenue_rows])
    (reports_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    issues = (f"{len(rejected)} row(s) rejected; see rejected_orders.csv" if rejected
              else "No data quality issues detected")
    (reports_dir / "status_report.md").write_text(
        "# Data Processing Status Report\n\n"
        "Synthetic sample data — not an employer work record.\n\n"
        f"- **Status:** {summary['status']}\n"
        f"- **Completed:** Ingested {total} source orders; validated and loaded "
        f"{len(accepted)} orders into SQLite.\n"
        f"- **Data quality:** {issues}.\n"
        f"- **Reporting:** Revenue by product category generated; "
        f"total validated revenue ${summary['total_revenue_usd']}.\n"
        "- **Next steps:** Review rejected rows and correct source data before rerunning.\n",
        encoding="utf-8",
    )
    return summary
