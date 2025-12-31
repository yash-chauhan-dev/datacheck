# Database Validation

Validate SQLite and DuckDB database tables.

---

## SQLite Validation

```bash
datacheck validate customers.db --table customers --config validation.yaml
```

---

## DuckDB Validation

```bash
datacheck validate warehouse.duckdb --table orders --config validation.yaml
```

(DuckDB available on Linux/macOS only)

---

## Complete Example

```yaml
# validation.yaml
checks:
  - name: customer_id_check
    column: customer_id
    rules:
      not_null: true
      unique: true

  - name: email_validation
    column: email
    rules:
      not_null: true
      unique: true
      regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
```

---

For more examples, see the repository: [examples/database-example](https://github.com/yash-chauhan-dev/datacheck/tree/main/examples/database-example)
