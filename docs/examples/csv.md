# CSV Validation Examples

## Basic CSV Validation

**users.csv:**
```csv
id,name,email,age
1,John Doe,john@example.com,25
2,Jane Smith,jane@example.com,30
3,Bob Johnson,bob-invalid,150
```

**validation.yaml:**
```yaml
checks:
  - name: email_validation
    column: email
    rules:
      not_null: true
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"

  - name: age_validation
    column: age
    rules:
      min: 0
      max: 120
```

**Run:**
```bash
datacheck validate users.csv --config validation.yaml
```

---

## Sales Data Validation

**sales.csv:**
```csv
date,product,quantity,revenue,region
2025-01-01,Widget A,100,5000,North
2025-01-02,Widget B,50,2500,South
2025-01-03,Widget C,-10,invalid,East
```

**sales-validation.yaml:**
```yaml
checks:
  - name: quantity_check
    column: quantity
    rules:
      not_null: true
      min: 0

  - name: revenue_check
    column: revenue
    rules:
      not_null: true
      min: 0

  - name: region_check
    column: region
    rules:
      allowed_values: ["North", "South", "East", "West"]
```

**Catches:**
- Negative quantity (-10)
- Invalid revenue (non-numeric)

---

## Customer Data with Multiple Validations

**customers.csv:**
```csv
customer_id,email,phone,zip_code,status
C001,alice@example.com,555-1234,12345,active
C002,bob@example.com,invalid-phone,ABCDE,inactive
```

**customer-validation.yaml:**
```yaml
checks:
  - name: id_check
    column: customer_id
    rules:
      not_null: true
      unique: true

  - name: email_check
    column: email
    rules:
      not_null: true
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"

  - name: phone_check
    column: phone
    rules:
      regex: "^\\d{3}-\\d{4}$"

  - name: zip_check
    column: zip_code
    rules:
      regex: "^\\d{5}$"

  - name: status_check
    column: status
    rules:
      allowed_values: ["active", "inactive", "pending"]
```

---

## Handling Large CSV Files

For files > 100MB, convert to Parquet for better performance:

```bash
# Convert CSV to Parquet
python -c "import pandas as pd; pd.read_csv('large.csv').to_parquet('large.parquet')"

# Validate Parquet file (10x faster)
datacheck validate large.parquet --config rules.yaml
```

---

## Auto-discovery

Place `.datacheck.yaml` in your project:

```
project/
├── .datacheck.yaml
└── data.csv
```

Then simply run:
```bash
datacheck validate data.csv
```

DataCheck automatically finds and uses `.datacheck.yaml`.
