# Data Formats

DataCheck supports multiple data formats out of the box.

## CSV Files

```bash
datacheck validate users.csv --config rules.yaml
```

Features:
- Automatic encoding detection (UTF-8, UTF-8-BOM)
- Header row detection
- Comma-separated values

Example `users.csv`:
```csv
user_id,email,age,status
1,john@example.com,25,active
2,jane@example.com,30,active
3,bob@example.com,45,inactive
```

## Parquet Files

Efficient columnar format for large datasets.

```bash
datacheck validate data.parquet --config rules.yaml
```

Benefits:
- Faster for large files
- Compressed by default
- Type-safe columns

## SQLite Databases

Validate tables directly from SQLite databases.

```bash
# Validate entire table
datacheck validate database.db::users --config rules.yaml
```

Format: `database.db::table_name`

## DuckDB (Optional)

High-performance analytical database.

```bash
# Install with DuckDB support (Linux/macOS only)
pip install datacheck-cli[duckdb]

# Validate DuckDB table
datacheck validate data.duckdb::analytics --config rules.yaml
```

::: warning
DuckDB is not available on Windows
:::

## File Size Recommendations

| Format | Best For | Max Recommended Size |
|--------|----------|---------------------|
| CSV | Small to medium datasets | < 1 GB |
| Parquet | Large datasets | < 10 GB |
| SQLite | Structured data queries | < 2 GB |
| DuckDB | Analytics, large datasets | < 100 GB |

## Performance Tips

### Large CSV Files
Use Parquet instead for 10x faster validation:
```bash
# Convert to Parquet first
python -c "import pandas as pd; pd.read_csv('large.csv').to_parquet('large.parquet')"

# Then validate
datacheck validate large.parquet --config rules.yaml
```

### Database Tables
Only validate the columns you need by selecting specific columns in your rules:
```yaml
checks:
  - name: id_check
    column: id
    rules:
      not_null: true

  # Don't add checks for columns you don't care about
```

### Memory Issues
If you hit memory limits, validate in chunks or use DuckDB.

## Switching Formats

Same validation rules work across all formats:

```yaml
# rules.yaml works for CSV, Parquet, and databases
checks:
  - name: email_check
    column: email
    rules:
      not_null: true
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"
```

```bash
# Use with any format
datacheck validate data.csv --config rules.yaml
datacheck validate data.parquet --config rules.yaml
datacheck validate data.db::users --config rules.yaml
```
