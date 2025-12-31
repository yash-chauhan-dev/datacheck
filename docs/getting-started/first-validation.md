# Your First Validation

This tutorial walks you through creating and running your first DataCheck validation from scratch.

---

## What You'll Build

By the end of this tutorial, you'll have:

- ✅ A sample CSV file with customer data
- ✅ Validation rules to ensure data quality
- ✅ A working validation pipeline
- ✅ Understanding of how to handle failures

---

## Scenario

You're a data engineer at an e-commerce company. You receive daily customer export files that need validation before loading into the data warehouse.

### Requirements

- Customer emails must be valid and unique
- Ages must be between 18 and 120
- Phone numbers must follow US format
- Account status must be one of: active, inactive, suspended

---

## Step-by-Step Guide

### 1. Create the Data File

Create `customers.csv`:

```csv
customer_id,name,email,age,phone,status,signup_date
1001,Alice Johnson,alice@example.com,28,+1-555-0123,active,2024-01-15
1002,Bob Smith,bob@example.com,35,+1-555-0124,active,2024-01-16
1003,Carol Davis,carol@example.com,42,+1-555-0125,inactive,2024-01-17
1004,David Wilson,david@example.com,31,+1-555-0126,active,2024-01-18
1005,Eve Brown,eve@example.com,29,+1-555-0127,suspended,2024-01-19
```

### 2. Define Validation Rules

Create `customer_validation.yaml`:

```yaml
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

  - name: age_validation
    column: age
    rules:
      not_null: true
      min: 18
      max: 120

  - name: phone_validation
    column: phone
    rules:
      not_null: true
      regex: "^\\+1-[0-9]{3}-[0-9]{4}$"

  - name: status_validation
    column: status
    rules:
      not_null: true
      allowed_values: ["active", "inactive", "suspended"]
```

### 3. Run the Validation

```bash
datacheck validate customers.csv --config customer_validation.yaml
```

**Expected Result** (all passing):

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

### 4. Test with Bad Data

Now let's introduce errors to see how DataCheck catches them. Update `customers.csv`:

```csv
customer_id,name,email,age,phone,status,signup_date
1001,Alice Johnson,alice@example.com,28,+1-555-0123,active,2024-01-15
1001,Bob Smith,invalid-email,150,555-0124,deleted,2024-01-16
,Carol Davis,carol@example.com,17,+1-555-0125,inactive,2024-01-17
```

Run validation again:

```bash
datacheck validate customers.csv --config customer_validation.yaml
```

**Expected Result** (with failures):

```
╭──────────────────────────────╮
│ DataCheck Validation Results │
╰──────────────────────────────╯

✗ VALIDATION FAILED

 Metric       Value
 Total Rules     11
 Passed           5
 Failed           6
 Errors           0

✗ customer_id_check
  → unique: Failed for 2 rows (66.67%)
     Sample failing rows: [0, 1]
  → not_null: Failed for 1 rows (33.33%)
     Sample failing rows: [2]

✗ email_validation
  → regex: Failed for 1 rows (33.33%)
     Sample failing rows: [1]

✗ age_validation
  → max: Failed for 1 rows (33.33%)
     Sample failing rows: [1]
  → min: Failed for 1 rows (33.33%)
     Sample failing rows: [2]

✗ phone_validation
  → regex: Failed for 1 rows (33.33%)
     Sample failing rows: [1]

✗ status_validation
  → allowed_values: Failed for 1 rows (33.33%)
     Sample failing rows: [1]
```

### 5. Export Results to JSON

For automated processing:

```bash
datacheck validate customers.csv \
  --config customer_validation.yaml \
  --format json \
  --json-output validation_results.json
```

Inspect the results:

```bash
cat validation_results.json | python -m json.tool
```

---

## Integration with Your Workflow

### Daily Data Pipeline

```bash
#!/bin/bash
# daily_load.sh

DATA_FILE="exports/customers_$(date +%Y%m%d).csv"
VALIDATION_CONFIG="config/customer_validation.yaml"

echo "Starting daily customer data load..."

# Download file
echo "Downloading data..."
aws s3 cp s3://bucket/exports/customers.csv "$DATA_FILE"

# Validate
echo "Validating data quality..."
datacheck validate "$DATA_FILE" --config "$VALIDATION_CONFIG"

if [ $? -eq 0 ]; then
  echo "✓ Validation passed! Loading to warehouse..."
  python load_to_snowflake.py "$DATA_FILE"
  
  # Archive successful load
  mv "$DATA_FILE" "archive/"
else
  echo "✗ Validation failed! Sending alert..."
  python send_alert.py "Data validation failed for $DATA_FILE"
  exit 1
fi
```

### Pre-commit Hook

Validate data files before committing:

```bash
#!/bin/bash
# .git/hooks/pre-commit

for file in $(git diff --cached --name-only | grep '\.csv$'); do
  if [ -f "config/${file%.csv}_validation.yaml" ]; then
    echo "Validating $file..."
    datacheck validate "$file" --config "config/${file%.csv}_validation.yaml"
    
    if [ $? -ne 0 ]; then
      echo "✗ Validation failed for $file"
      exit 1
    fi
  fi
done

echo "✓ All data files validated"
```

---

## Key Takeaways

1. **Simple YAML** - Validation rules are easy to read and write
2. **Clear Feedback** - Terminal output shows exactly what failed
3. **Exit Codes** - Perfect for automation and CI/CD
4. **JSON Output** - Machine-readable for programmatic use
5. **Fast** - Validates millions of rows quickly

---

## Next Steps

Now that you've completed your first validation:

- Explore [Validation Rules](../user-guide/validation-rules.md) to learn all available rules
- Check out [Real-World Examples](../examples/real-world.md) for more complex scenarios
- Learn how to [Integrate with CI/CD](../integration/cicd.md)
- Read about [Output Formats](../user-guide/output-formats.md)

---

## Troubleshooting

### Common Issues

**File not found**:
```bash
# Use absolute path
datacheck validate /full/path/to/data.csv --config /full/path/to/config.yaml
```

**Config syntax error**:
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

**Encoding issues**:
```bash
# DataCheck auto-detects encoding, but you can specify:
# Edit the CSV with proper encoding tools if needed
iconv -f ISO-8859-1 -t UTF-8 data.csv > data_utf8.csv
```

---

Need help? [Open an issue](https://github.com/yash-chauhan-dev/datacheck/issues) on GitHub!
