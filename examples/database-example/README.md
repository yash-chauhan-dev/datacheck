# SQLite Database Example

This example demonstrates how to validate **SQLite database tables** using DataCheck's Python API.

## Overview

DataCheck can validate data directly from SQLite databases without requiring you to export to CSV or other formats. This is useful for validating application databases, data warehouses, or any SQLite-based storage.

> **Note**: Database validation currently requires using the Python API. CLI support for `--table` and `--query` options is planned for a future release.

## Files

- `orders.db` - Sample SQLite database with an orders table
- `validation_config.yaml` - Validation rules for the orders data
- `validate_orders.py` - Example Python script for validation

## Database Schema

The `orders.db` database contains an `orders` table with 5 sample orders:

```sql
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_email TEXT NOT NULL,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    total_amount REAL NOT NULL,
    order_status TEXT NOT NULL,
    order_date TEXT NOT NULL
)
```

## Dataset Description

| Column | Type | Description |
|--------|------|-------------|
| order_id | TEXT | Unique order identifier (ORD format) |
| customer_email | TEXT | Customer email address |
| product_name | TEXT | Name of ordered product |
| quantity | INTEGER | Number of items ordered |
| unit_price | REAL | Price per item |
| total_amount | REAL | Total order amount |
| order_status | TEXT | Order processing status |
| order_date | TEXT | Date order was placed |

## Validation Rules

The configuration validates:

1. **Order ID**: Not null, unique, matches pattern `ORD###`
2. **Customer Email**: Not null, valid email format
3. **Product Name**: Not null, at least 3 characters
4. **Quantity**: Not null, between 1 and 1,000 units
5. **Unit Price**: Not null, between $0.01 and $100,000
6. **Total Amount**: Not null, between $0.01 and $100,000
7. **Order Status**: Must be one of: pending, processing, shipped, completed, cancelled
8. **Order Date**: Not null

## Running the Example

Create a Python script to validate the database:

```python
# validate_orders.py
from datacheck.loader import LoaderFactory
from datacheck.engine import ValidationEngine

# Load data from SQLite database
df = LoaderFactory.load(
    "examples/database-example/orders.db",
    table_name="orders"  # Specify table to load
)

# Validate the data
engine = ValidationEngine(config_path="examples/database-example/validation_config.yaml")
summary = engine.validate(df=df)

# Display results
if summary.all_passed:
    print(f"✅ All {summary.total_rules} validation rules passed!")
else:
    print(f"❌ {summary.failed_count} validation rules failed")
    for result in summary.get_failed_results():
        print(f"  - {result.rule_name}: {result.failure_details.failed_count} failures")
```

Run the script:

```bash
poetry run python validate_orders.py
```

## Expected Output

All validations should pass:

```
╭──────────────────────────────╮
│ DataCheck Validation Results │
╰──────────────────────────────╯

✓ ALL CHECKS PASSED

 Metric       Value
 Total Rules     11
 Passed          11
 Failed           0
 Errors           0
```

## Inspecting the Database

You can inspect the database using sqlite3:

```bash
# View table schema
sqlite3 examples/database-example/orders.db ".schema orders"

# View all orders
sqlite3 examples/database-example/orders.db "SELECT * FROM orders"

# Count orders by status
sqlite3 examples/database-example/orders.db \
  "SELECT order_status, COUNT(*) FROM orders GROUP BY order_status"
```

## Python Integration Example

Use DataCheck with SQLite in your Python applications:

```python
from datacheck.engine import ValidationEngine
from datacheck.loader import LoaderFactory

# Load data from database table
df = LoaderFactory.load("orders.db", table_name="orders")

# Validate the data
engine = ValidationEngine(config_path="validation_config.yaml")
summary = engine.validate(df=df)

if not summary.all_passed:
    print(f"❌ {summary.failed_count} validation rules failed")
    for result in summary.get_failed_results():
        print(f"  - {result.rule_name}: {result.failure_details.failed_count} failures")
else:
    print("✅ All validations passed!")
```

## Advanced Query Example

Validate only recent orders using a custom SQL query:

```python
from datacheck.engine import ValidationEngine
from datacheck.loader import LoaderFactory

# Load data with custom SQL query
df = LoaderFactory.load(
    "orders.db",
    query="SELECT * FROM orders WHERE order_date >= '2024-01-14'"
)

# Validate the filtered data
engine = ValidationEngine(config_path="validation_config.yaml")
summary = engine.validate(df=df)
```

## Database Support

DataCheck supports:

- **SQLite** (.db, .sqlite, .sqlite3) - ✅ Built-in, works on all platforms
- **DuckDB** (.duckdb) - ⚠️ Optional, Linux/macOS only (install with `pip install 'datacheck[duckdb]'`)

SQLite is perfect for:
- Application databases
- Data exports from web apps
- Small to medium datasets
- Embedded databases
- Testing and development

## Learn More

- See `examples/parquet-example/` for Parquet file validation
- See `examples/basic/` for CSV examples
- Check the main README for CLI options and Python API
