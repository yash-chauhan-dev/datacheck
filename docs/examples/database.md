# Database Validation Examples

## SQLite Database

Validate tables directly from SQLite databases.

**Format:** `database.db::table_name`

### Example 1: Users Table

```bash
datacheck validate myapp.db::users --config user-validation.yaml
```

**user-validation.yaml:**
```yaml
checks:
  - name: user_id_check
    column: id
    rules:
      not_null: true
      unique: true

  - name: email_check
    column: email
    rules:
      not_null: true
      unique: true
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"

  - name: created_at_check
    column: created_at
    rules:
      not_null: true
```

### Example 2: Orders Table

```bash
datacheck validate shop.db::orders --config order-validation.yaml
```

**order-validation.yaml:**
```yaml
checks:
  - name: order_id_check
    column: order_id
    rules:
      not_null: true
      unique: true

  - name: customer_id_check
    column: customer_id
    rules:
      not_null: true

  - name: total_check
    column: total_amount
    rules:
      not_null: true
      min: 0

  - name: status_check
    column: status
    rules:
      allowed_values: ["pending", "paid", "shipped", "delivered", "cancelled"]
```

---

## DuckDB Database (Linux/macOS)

DuckDB is optimized for analytical workloads.

**Install:**
```bash
pip install datacheck-cli[duckdb]
```

**Validate:**
```bash
datacheck validate analytics.duckdb::events --config event-validation.yaml
```

**event-validation.yaml:**
```yaml
checks:
  - name: event_id_check
    column: event_id
    rules:
      not_null: true
      unique: true

  - name: timestamp_check
    column: timestamp
    rules:
      not_null: true

  - name: user_id_check
    column: user_id
    rules:
      not_null: true

  - name: event_type_check
    column: event_type
    rules:
      allowed_values: ["click", "view", "purchase", "signup"]
```

---

## Validating Multiple Tables

Create validation configs for each table:

```
validation/
├── users.yaml
├── orders.yaml
├── products.yaml
└── events.yaml
```

Validate all tables:
```bash
datacheck validate app.db::users --config validation/users.yaml
datacheck validate app.db::orders --config validation/orders.yaml
datacheck validate app.db::products --config validation/products.yaml
datacheck validate app.db::events --config validation/events.yaml
```

Or use a script:
```bash
#!/bin/bash
for table in users orders products events; do
    echo "Validating $table..."
    datacheck validate app.db::$table --config validation/$table.yaml
    if [ $? -ne 0 ]; then
        echo "❌ Validation failed for $table"
        exit 1
    fi
done
echo "✅ All tables validated successfully"
```

---

## CI/CD Database Validation

Validate database dumps before deployment:

```yaml
# .github/workflows/validate-db.yml
name: Validate Database

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install DataCheck
        run: pip install datacheck-cli

      - name: Validate users table
        run: datacheck validate backup.db::users --config validation/users.yaml

      - name: Validate orders table
        run: datacheck validate backup.db::orders --config validation/orders.yaml
```

---

## Export Database to CSV (for validation)

If you need to validate data from other databases (PostgreSQL, MySQL, etc.), export to CSV first:

```bash
# PostgreSQL
psql -d mydb -c "COPY users TO '/tmp/users.csv' CSV HEADER"
datacheck validate /tmp/users.csv --config user-validation.yaml

# MySQL
mysql -e "SELECT * FROM users" mydb > /tmp/users.csv
datacheck validate /tmp/users.csv --config user-validation.yaml
```

Or convert to Parquet for better performance:
```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://localhost/mydb')
df = pd.read_sql('SELECT * FROM users', engine)
df.to_parquet('users.parquet')
```

Then validate:
```bash
datacheck validate users.parquet --config user-validation.yaml
```
