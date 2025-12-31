# Python API

Use DataCheck programmatically in your Python scripts.

---

## Basic Usage

```python
from datacheck.loader import LoaderFactory
from datacheck.engine import ValidationEngine

# Load data
df = LoaderFactory.load("customers.csv")

# Run validation
engine = ValidationEngine(config_path="validation.yaml")
summary = engine.validate(df=df)

# Check results
if summary.all_passed:
    print("✅ All validations passed!")
else:
    print("❌ Some validations failed")
    for check in summary.checks:
        if not check.passed:
            print(f"Failed: {check.name}")
```

---

## Loading Different Formats

```python
# CSV
df = LoaderFactory.load("data.csv")

# Parquet
df = LoaderFactory.load("data.parquet")

# SQLite
df = LoaderFactory.load("data.db", table_name="customers")

# DuckDB
df = LoaderFactory.load("data.duckdb", table_name="orders")
```

---

## Programmatic Rule Creation

```python
from datacheck.config import ValidationConfig, Check, Rules

# Create rules programmatically
config = ValidationConfig(
    checks=[
        Check(
            name="email_validation",
            column="email",
            rules=Rules(
                not_null=True,
                regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            )
        )
    ]
)

# Validate
engine = ValidationEngine(config=config)
summary = engine.validate(df=df)
```

---

## Accessing Results

```python
# Summary
print(f"Total checks: {summary.total_checks}")
print(f"Passed: {summary.passed_checks}")
print(f"Failed: {summary.failed_checks}")

# Individual check results
for check in summary.checks:
    print(f"\n{check.name}: {'✅' if check.passed else '❌'}")
    for rule in check.rules:
        if not rule.passed:
            print(f"  - {rule.rule}: {rule.message}")
            print(f"    Failing rows: {rule.failing_rows}")
```

---

## JSON Export

```python
import json

# Export to JSON
result_dict = summary.to_dict()
with open("results.json", "w") as f:
    json.dump(result_dict, f, indent=2)
```

---

See the [examples/database-example/validate_orders.py](https://github.com/yash-chauhan-dev/datacheck/blob/main/examples/database-example/validate_orders.py) for a complete example.
