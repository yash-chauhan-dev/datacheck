# Quick Start

Get started with DataCheck in 5 minutes! This guide will walk you through your first data validation.

---

## Step 1: Create Sample Data

Create a CSV file with some sample data:

```bash
cat > employees.csv << EOF
name,age,email,salary,department
Alice Smith,30,alice@example.com,75000,Engineering
Bob Johnson,25,bob@example.com,65000,Marketing
Carol Williams,35,carol@example.com,85000,Engineering
David Brown,28,david@example.com,70000,Sales
Eve Davis,32,eve@example.com,80000,Engineering
EOF
```

---

## Step 2: Create Validation Rules

Create a YAML file with validation rules:

```bash
cat > validation.yaml << EOF
checks:
  - name: age_validation
    column: age
    rules:
      not_null: true
      min: 18
      max: 120

  - name: email_format
    column: email
    rules:
      not_null: true
      regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\\\.[a-zA-Z]{2,}$"

  - name: salary_range
    column: salary
    rules:
      not_null: true
      min: 0
      max: 1000000

  - name: department_values
    column: department
    rules:
      allowed_values: ["Engineering", "Marketing", "Sales", "HR"]
EOF
```

---

## Step 3: Run Validation

Execute the validation command:

```bash
datacheck validate employees.csv --config validation.yaml
```

### Expected Output

If all validations pass, you'll see:

```
╭──────────────────────────────╮
│ DataCheck Validation Results │
╰──────────────────────────────╯

✓ ALL CHECKS PASSED

 Metric       Value
 Total Rules      8
 Passed           8
 Failed           0
 Errors           0

✓ age_validation
✓ email_format
✓ salary_range
✓ department_values
```

---

## Step 4: Introduce an Error

Let's see what happens when validation fails. Modify the CSV:

```bash
cat > employees.csv << EOF
name,age,email,salary,department
Alice Smith,30,alice@example.com,75000,Engineering
Bob Johnson,150,invalid-email,65000,Marketing
Carol Williams,35,carol@example.com,85000,InvalidDept
EOF
```

Run validation again:

```bash
datacheck validate employees.csv --config validation.yaml
```

### Expected Output with Failures

```
╭──────────────────────────────╮
│ DataCheck Validation Results │
╰──────────────────────────────╯

✗ VALIDATION FAILED

 Metric       Value
 Total Rules      8
 Passed           5
 Failed           3
 Errors           0

✓ salary_range
✗ age_validation
  → max: Failed for 1 rows (33.33%)
     Sample failing rows: [1]

✗ email_format
  → regex: Failed for 1 rows (33.33%)
     Sample failing rows: [1]

✗ department_values
  → allowed_values: Failed for 1 rows (33.33%)
     Sample failing rows: [2]
```

---

## Step 5: JSON Output

For automation and CI/CD, use JSON output:

```bash
datacheck validate employees.csv \
  --config validation.yaml \
  --format json \
  --json-output results.json
```

View the JSON output:

```bash
cat results.json
```

Example JSON:

```json
{
  "summary": {
    "total_checks": 4,
    "passed_checks": 1,
    "failed_checks": 3,
    "error_checks": 0,
    "all_passed": false
  },
  "checks": [
    {
      "name": "age_validation",
      "column": "age",
      "passed": false,
      "rules": [
        {
          "rule": "max",
          "passed": false,
          "message": "Failed for 1 rows (33.33%)",
          "failing_rows": [1]
        }
      ]
    }
  ]
}
```

---

## Common Use Cases

### Auto-discover Configuration

DataCheck automatically looks for config files:

```bash
# Rename your config
mv validation.yaml .datacheck.yaml

# Run without --config flag
datacheck validate employees.csv
```

### Validate Multiple Files

```bash
# Using shell globbing
for file in data/*.csv; do
  datacheck validate "$file" --config validation.yaml || exit 1
done
```

### Use in Shell Scripts

```bash
#!/bin/bash
set -e  # Exit on error

echo "Validating data..."
datacheck validate data.csv --config rules.yaml

if [ $? -eq 0 ]; then
  echo "✓ Validation passed! Loading to warehouse..."
  python load_to_warehouse.py
else
  echo "✗ Validation failed! Aborting..."
  exit 1
fi
```

---

## Exit Codes

DataCheck uses exit codes for automation:

| Code | Meaning | Description |
|------|---------|-------------|
| `0` | Success | All validations passed |
| `1` | Failed | Some validations failed |
| `2` | Config Error | Configuration file error |
| `3` | Data Error | Data loading error |
| `4` | Runtime Error | Unexpected error |

---

## Next Steps

- Learn about all [Validation Rules](../user-guide/validation-rules.md)
- Explore [Real-World Examples](../examples/real-world.md)
- Integrate with [CI/CD Pipelines](../integration/cicd.md)
- Read the complete [User Guide](../user-guide/overview.md)

---

## Quick Reference

```bash
# Basic validation
datacheck validate data.csv --config rules.yaml

# JSON output
datacheck validate data.csv --config rules.yaml --format json

# Auto-discover config
datacheck validate data.csv

# Check version
datacheck --version

# Get help
datacheck --help
datacheck validate --help
```
