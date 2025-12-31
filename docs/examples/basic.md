# Basic Examples

Simple examples to get you started with DataCheck.

See the [Quick Start](../getting-started/quick-start.md) guide for step-by-step tutorials.

---

## Example 1: CSV Validation

```bash
datacheck validate employees.csv --config validation.yaml
```

## Example 2: Parquet Validation

```bash
datacheck validate products.parquet --config product_rules.yaml
```

## Example 3: Database Validation

```bash
datacheck validate orders.db --table orders --config order_validation.yaml
```

For more examples, see the [`examples/`](https://github.com/yash-chauhan-dev/datacheck/tree/main/examples) directory in the repository.
