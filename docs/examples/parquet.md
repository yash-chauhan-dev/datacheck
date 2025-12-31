# Parquet Validation

Validate Parquet files efficiently with DataCheck.

---

## Basic Usage

```bash
datacheck validate products.parquet --config validation.yaml
```

---

## Complete Example

```yaml
# validation.yaml
checks:
  - name: product_id_validation
    column: product_id
    rules:
      not_null: true
      unique: true
      regex: "^SKU[0-9]{3}$"

  - name: price_validation
    column: price
    rules:
      not_null: true
      min: 0.01
      max: 99999.99
```

---

## Parquet Features

- ✅ Efficient columnar format
- ✅ Fast reading with PyArrow
- ✅ Handles compressed files
- ✅ Large dataset support

---

For more examples, see the repository: [examples/parquet-example](https://github.com/yash-chauhan-dev/datacheck/tree/main/examples/parquet-example)
