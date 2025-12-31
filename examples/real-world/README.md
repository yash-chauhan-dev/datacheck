# Real-World DataCheck Examples

This directory contains production-ready examples for common data validation scenarios.

## Examples

### 1. E-Commerce Sales Data (`sales_data.csv`)

**Use Case**: Validate sales transactions for analytics and reporting

**Validation Rules**:
- Order ID format: `ORD-YYYY-###`
- Customer and Product ID formats
- Quantity and price ranges
- Valid order statuses
- Accepted payment methods

**Run Example**:
```bash
datacheck validate sales_data.csv --config sales_validation.yaml
```

**CI/CD Integration**:
```yaml
# .github/workflows/data-quality.yml
- name: Validate Sales Data
  run: |
    datacheck validate data/sales.csv --config validation/sales.yaml --format json
    if [ $? -ne 0 ]; then
      echo "Sales data validation failed!"
      exit 1
    fi
```

---

### 2. User Account Data (`user_data.csv`)

**Use Case**: Validate user registration and account data for SaaS applications

**Validation Rules**:
- Unique user IDs and usernames
- Email format and uniqueness
- Age requirements (13+)
- Country codes (ISO format)
- Account type restrictions

**Run Example**:
```bash
datacheck validate user_data.csv --config user_validation.yaml
```

**Automated Testing**:
```bash
# Run validation as part of your data pipeline
#!/bin/bash
INPUT_FILE="data/new_users.csv"
CONFIG="validation/user_validation.yaml"

datacheck validate "$INPUT_FILE" --config "$CONFIG" --format json --json-output results.json

# Check exit code
if [ $? -eq 0 ]; then
  echo "✓ User data validation passed"
  # Proceed with data import
  python import_users.py
else
  echo "✗ User data validation failed"
  cat results.json
  exit 1
fi
```

---

## Common Use Cases

### Data Warehouse ETL
Validate data before loading into your data warehouse:
```bash
# Validate staging data
datacheck validate staging/customers.csv --config validation/customers.yaml

# Exit codes:
# 0 = Pass, load data
# 1 = Failed rules, investigate
# 2 = Config error
# 3 = File error
```

### API Data Validation
Validate exported API data:
```bash
# Export API data
curl -o export.csv "https://api.example.com/export"

# Validate exported data
datacheck validate export.csv --config api_validation.yaml --format json

# Parse results
python process_validation_results.py
```

### Scheduled Data Quality Checks
Run periodic validations:
```bash
# Cron job: Daily at 2 AM
0 2 * * * /usr/local/bin/datacheck validate /data/daily_export.csv \
  --config /configs/daily_checks.yaml \
  --format json \
  --json-output /logs/validation_$(date +\%Y\%m\%d).json
```

### Pre-commit Hooks
Validate data files before committing:
```bash
# .git/hooks/pre-commit
#!/bin/bash
for file in $(git diff --cached --name-only | grep '\.csv$'); do
  echo "Validating $file..."
  datacheck validate "$file" --config validation/data.yaml
  if [ $? -ne 0 ]; then
    echo "Validation failed for $file"
    exit 1
  fi
done
```

---

## Integration Patterns

### Python Integration
```python
import subprocess
import json

def validate_data(file_path, config_path):
    """Validate data and return results."""
    result = subprocess.run(
        [
            "datacheck", "validate",
            file_path,
            "--config", config_path,
            "--format", "json"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return {"status": "passed", "data": json.loads(result.stdout)}
    elif result.returncode == 1:
        return {"status": "failed", "data": json.loads(result.stdout)}
    else:
        return {"status": "error", "message": result.stderr}

# Usage
results = validate_data("data.csv", "config.yaml")
if results["status"] == "passed":
    print("✓ Data validation passed")
else:
    print(f"✗ Validation {results['status']}")
```

### Shell Script Integration
```bash
#!/bin/bash
set -e

validate_and_process() {
  local file=$1
  local config=$2

  echo "Validating $file..."
  if datacheck validate "$file" --config "$config"; then
    echo "✓ Validation passed - proceeding with processing"
    python process_data.py "$file"
  else
    echo "✗ Validation failed - check data quality"
    exit 1
  fi
}

validate_and_process "data/import.csv" "validation/config.yaml"
```

---

## Best Practices

1. **Version Control**: Keep validation configs in version control
2. **Document Rules**: Add comments explaining why each rule exists
3. **Start Simple**: Begin with basic rules, add complexity gradually
4. **Test Configs**: Test validation configs with known-good and known-bad data
5. **Monitor Results**: Track validation failure rates over time
6. **Automate**: Integrate into CI/CD pipelines and data workflows
7. **Alert on Failures**: Set up notifications for validation failures

---

## Exit Codes Reference

- `0`: All validation rules passed ✓
- `1`: Some validation rules failed (data quality issues)
- `2`: Configuration error (fix config file)
- `3`: Data loading error (check file path/format)
- `4`: Unexpected error (check logs)

Use exit codes in scripts:
```bash
datacheck validate data.csv --config config.yaml
case $? in
  0) echo "Success" ;;
  1) echo "Validation failed" ;;
  2) echo "Config error" ;;
  3) echo "File error" ;;
  4) echo "Unexpected error" ;;
esac
```
