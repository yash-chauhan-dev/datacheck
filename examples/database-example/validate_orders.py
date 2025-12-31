#!/usr/bin/env python3
"""Example script to validate SQLite database tables."""

from pathlib import Path

from datacheck.engine import ValidationEngine
from datacheck.loader import LoaderFactory

# Paths
DB_PATH = Path(__file__).parent / "orders.db"
CONFIG_PATH = Path(__file__).parent / "validation_config.yaml"


def main() -> None:
    """Validate orders database table."""
    print("📊 Loading orders from database...")

    # Load data from SQLite database
    df = LoaderFactory.load(
        DB_PATH,
        table_name="orders"  # Specify table to load
    )

    print(f"   Loaded {len(df)} orders\n")

    print("🔍 Running validation checks...")

    # Validate the data
    engine = ValidationEngine(config_path=CONFIG_PATH)
    summary = engine.validate(df=df)

    print()

    # Display results
    if summary.all_passed:
        print(f"✅ All {summary.total_rules} validation rules passed!")
    else:
        print(f"❌ {summary.failed_count} of {summary.total_rules} validation rules failed\n")

        for result in summary.get_failed_results():
            print(f"  - {result.rule_name}:")
            print(f"      Failed rows: {result.failure_details.failed_count}")
            print(f"      Failure rate: {result.failure_details.failure_rate:.1f}%")


if __name__ == "__main__":
    main()
