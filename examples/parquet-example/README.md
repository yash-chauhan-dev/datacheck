# Parquet Format Example

This example demonstrates how to validate **Parquet files** using DataCheck.

## Overview

Parquet is a columnar storage file format optimized for big data processing. DataCheck can validate Parquet files just as easily as CSV files, with full support for all data types.

## Files

- `product_inventory.parquet` - Sample product inventory data in Parquet format
- `validation_config.yaml` - Validation rules for the inventory data

## Dataset Description

The `product_inventory.parquet` file contains 5 products with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| product_id | string | Unique product identifier (SKU format) |
| product_name | string | Product name |
| category | string | Product category |
| price | float | Product price in USD |
| stock_quantity | int | Current inventory count |
| supplier_id | string | Supplier identifier |
| last_updated | datetime | Last update timestamp |

## Validation Rules

The configuration validates:

1. **Product ID**: Not null, unique, matches pattern `SKU###`
2. **Product Name**: Not null, at least 3 characters
3. **Category**: Must be one of: Electronics, Accessories, Furniture, Office Supplies
4. **Price**: Not null, between $0.01 and $10,000
5. **Stock Quantity**: Not null, between 0 and 10,000 units
6. **Supplier ID**: Not null, matches pattern `SUP###`
7. **Last Updated**: Not null

## Running the Example

### Basic Validation

```bash
# From the project root
datacheck validate examples/parquet-example/product_inventory.parquet \
  --config examples/parquet-example/validation_config.yaml
```

### JSON Output

```bash
datacheck validate examples/parquet-example/product_inventory.parquet \
  --config examples/parquet-example/validation_config.yaml \
  --format json \
  --json-output validation_results.json
```

## Expected Output

All validations should pass:

```
╭──────────────────────────────╮
│ DataCheck Validation Results │
╰──────────────────────────────╯

✓ ALL CHECKS PASSED

 Metric       Value
 Total Rules     10
 Passed          10
 Failed           0
 Errors           0
```

## Why Parquet?

Parquet files offer several advantages:

- **Efficient storage**: Columnar format with compression
- **Fast queries**: Read only required columns
- **Type safety**: Preserves data types (dates, integers, floats)
- **Big data ready**: Used by Spark, Dask, and other big data tools

DataCheck validates Parquet files efficiently by leveraging pandas and pyarrow, the same libraries used by modern data platforms.

## Integration Example

Use in a data pipeline:

```python
from datacheck.engine import ValidationEngine

# Validate Parquet file
engine = ValidationEngine(config_path="validation_config.yaml")
summary = engine.validate(file_path="product_inventory.parquet")

if not summary.all_passed:
    raise ValueError(f"Validation failed: {summary.failed_count} checks failed")
```

## Learn More

- See `examples/basic/` for CSV examples
- See `examples/database-example/` for SQLite database validation
- Check the main README for more format options
