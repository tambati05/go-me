# Data Analyst ETL & Quality Reporting — Portfolio Demo

A **Python + SQL** data-processing project demonstrating common Data Analyst responsibilities: source ingestion, cleaning, data validation, reconciliation, repeatable loading, reporting, and status communication.

> **Portfolio disclosure:** This is an independent demonstration using fictional sales/customer records. It is **not** Pivotal Technologies source code, an internal deliverable, or evidence that these exact tasks were performed for an employer. No company or personal data is used.

## What it does

1. **Ingest:** Load synthetic customer and order records from CSV sources.
2. **Validate & clean:** Normalize dates; reject duplicate IDs, unknown customer IDs, invalid quantities/prices, and missing fields. Document each rejected row and reason.
3. **Transform:** Convert money to integer cents to prevent floating-point errors.
4. **Load:** Refresh a SQLite database with foreign-key relationships, so rerunning the workflow does not duplicate data.
5. **Report:** Export revenue by category, validation metrics, rejected records, and a concise status report.
6. **Test:** Run unit tests for data quality, revenue reconciliation, schema validation, and idempotent reruns.

## Quick start (Python 3.11+; no third-party dependencies)

From the repository root:

```bash
cd data-analyst-pipeline
python -m analytics_pipeline
```

By default the pipeline reads `sample_data/customers.csv` and `sample_data/orders.csv` and writes:

```text
output/reporting.db
output/reports/summary.json
output/reports/revenue_by_category.csv
output/reports/rejected_orders.csv
output/reports/status_report.md
```

To use custom paths:

```bash
python -m analytics_pipeline --customers sample_data/customers.csv --orders sample_data/orders.csv --db output/reporting.db --reports output/reports
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Expected sample output

The fictional example contains **12 order rows**: **8 accepted**, **4 rejected** (unknown customer, zero quantity, duplicate order ID, invalid price). The rejected-row audit lists the source row and reason. All dollar totals derive from accepted rows only.

Example SQL queries are available in [`sql/reporting_queries.sql`](sql/reporting_queries.sql). Load `output/reporting.db` in SQLite or a compatible editor to run them.

## Architecture

```text
CSV sources → schema checks → row-level validation → SQLite tables
                                              ↘ rejected_orders audit
SQLite → SQL aggregation → report CSV + JSON + Markdown status report
```

## How this maps to real Data Analyst work

| Skill area | Demonstrated here |
| --- | --- |
| Data ingestion | Read and validate records from separate source files |
| Data preparation | Clean formats and enforce business rules |
| Data quality & reconciliation | Track accepted/rejected records and resolve causes |
| SQL analysis | Aggregate and query a relational database |
| Pipeline automation | One-command repeatable ETL with deterministic refresh |
| Stakeholder reporting | Export analytics and a concise status report |

**Next enhancements:** add a real API adapter with mocked tests, scheduling (e.g., Airflow), structured logs, and an interactive BI dashboard. These are roadmap items, not implemented features.
