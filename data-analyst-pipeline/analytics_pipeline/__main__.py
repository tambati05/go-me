"""Command-line entry point for the demonstration pipeline."""

import argparse
import json
from .pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the sample data analyst ETL pipeline")
    parser.add_argument("--orders", default="sample_data/orders.csv")
    parser.add_argument("--customers", default="sample_data/customers.csv")
    parser.add_argument("--db", default="output/reporting.db")
    parser.add_argument("--reports", default="output/reports")
    args = parser.parse_args()
    result = run_pipeline(args.orders, args.customers, args.db, args.reports)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
