# Quick Start Examples

## Example 1: User Registration Data

Validate new user signups before processing.

**Data** (`users.csv`):
```csv
user_id,email,age,country
1001,alice@example.com,28,US
1002,bob@example.com,35,UK
1003,invalid-email,17,CA
```

**Rules** (`user-validation.yaml`):
```yaml
checks:
  - name: user_id_check
    column: user_id
    rules:
      not_null: true
      unique: true
      min: 1000

  - name: email_format
    column: email
    rules:
      not_null: true
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"

  - name: age_requirement
    column: age
    rules:
      min: 18
```

**Run:**
```bash
datacheck validate users.csv --config user-validation.yaml
```

**Result:** Catches row 3 with invalid email and underage user.

---

## Example 2: E-commerce Orders

Validate order data before processing payments.

**Data** (`orders.csv`):
```csv
order_id,product_id,quantity,price,status
ORD001,PROD123,2,49.99,pending
ORD002,PROD456,0,199.99,confirmed
ORD003,PROD789,5,-10.00,pending
```

**Rules** (`order-validation.yaml`):
```yaml
checks:
  - name: order_id_check
    column: order_id
    rules:
      not_null: true
      unique: true

  - name: quantity_check
    column: quantity
    rules:
      min: 1

  - name: price_check
    column: price
    rules:
      min: 0

  - name: status_check
    column: status
    rules:
      allowed_values: ["pending", "confirmed", "shipped", "delivered"]
```

**Run:**
```bash
datacheck validate orders.csv --config order-validation.yaml
```

**Result:** Catches zero quantity and negative price.

---

## Example 3: Financial Transactions

Validate transaction data for anomalies.

**Data** (`transactions.parquet`)**

**Rules** (`transaction-validation.yaml`):
```yaml
checks:
  - name: transaction_id
    column: txn_id
    rules:
      not_null: true
      unique: true

  - name: amount_range
    column: amount
    rules:
      not_null: true
      min: 0.01
      max: 1000000

  - name: account_format
    column: account_number
    rules:
      not_null: true
      regex: "^\\d{10,12}$"

  - name: transaction_type
    column: type
    rules:
      allowed_values: ["deposit", "withdrawal", "transfer"]
```

**Run:**
```bash
datacheck validate transactions.parquet --config transaction-validation.yaml
```

---

## Example 4: Data Pipeline Validation

Validate at each stage of your pipeline.

```bash
# Stage 1: Raw data
datacheck validate raw/users.csv --config validation/raw-users.yaml

# Stage 2: Cleaned data
datacheck validate cleaned/users.csv --config validation/clean-users.yaml

# Stage 3: Transformed data
datacheck validate transformed/users.parquet --config validation/final-users.yaml
```

**Benefits:**
- Catch issues early
- Know exactly where data quality breaks
- Independent validation at each stage

---

## Example 5: JSON Output for Automation

Get machine-readable output for processing.

```bash
datacheck validate data.csv --config rules.yaml --output json > results.json
```

**Output** (`results.json`):
```json
{
  "summary": {
    "total_checks": 5,
    "passed": 3,
    "failed": 2,
    "errors": 0
  },
  "checks": [
    {
      "name": "email_format",
      "column": "email",
      "status": "failed",
      "failures": {
        "count": 1,
        "percentage": 33.3,
        "sample_rows": [2]
      }
    }
  ]
}
```

Use in scripts:
```python
import json
import subprocess

result = subprocess.run(
    ['datacheck', 'validate', 'data.csv', '--output', 'json'],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)
if data['summary']['failed'] > 0:
    print(f"{data['summary']['failed']} checks failed")
    # Send alert, update dashboard, etc.
```

---

## Next Steps

- [Use in CI/CD pipelines](/examples/cicd)
- [Database validation](/examples/database)
- [See CLI reference](/reference/cli)
