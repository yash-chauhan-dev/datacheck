# Output Formats

DataCheck supports multiple output formats for different use cases.

---

## Terminal Output (Default)

Beautiful, colorful output for human consumption.

### Successful Validation

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

✓ customer_id_validation
✓ email_validation
✓ age_validation
✓ status_validation
```

### Failed Validation

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

✓ customer_id_validation
✗ email_validation
  → regex: Failed for 2 rows (25.00%)
     Sample failing rows: [1, 5]
     
✗ age_validation
  → min: Failed for 1 rows (12.50%)
     Sample failing rows: [3]
     
✓ status_validation
```

---

## JSON Output

Machine-readable format for automation and integration.

### Usage

```bash
datacheck validate data.csv --config rules.yaml --format json
```

### Save to File

```bash
datacheck validate data.csv \
  --config rules.yaml \
  --format json \
  --json-output results.json
```

### JSON Structure

```json
{
  "summary": {
    "total_checks": 4,
    "passed_checks": 2,
    "failed_checks": 2,
    "error_checks": 0,
    "all_passed": false
  },
  "checks": [
    {
      "name": "customer_id_validation",
      "column": "customer_id",
      "passed": true,
      "rules": [
        {
          "rule": "not_null",
          "passed": true,
          "message": "Passed",
          "failing_rows": []
        },
        {
          "rule": "unique",
          "passed": true,
          "message": "Passed",
          "failing_rows": []
        }
      ]
    },
    {
      "name": "email_validation",
      "column": "email",
      "passed": false,
      "rules": [
        {
          "rule": "regex",
          "passed": false,
          "message": "Failed for 2 rows (25.00%)",
          "failing_rows": [1, 5]
        }
      ]
    }
  ]
}
```

---

## Using Output in Scripts

### Bash Example

```bash
#!/bin/bash

# Run validation and save JSON
datacheck validate data.csv \
  --config rules.yaml \
  --format json \
  --json-output results.json

# Parse with jq
FAILED_CHECKS=$(jq '.summary.failed_checks' results.json)

if [ "$FAILED_CHECKS" -gt 0 ]; then
  echo "❌ Validation failed with $FAILED_CHECKS failed checks"
  
  # Get list of failed check names
  jq -r '.checks[] | select(.passed == false) | .name' results.json
  
  exit 1
else
  echo "✅ All validation checks passed"
  exit 0
fi
```

### Python Example

```python
import json
import subprocess
import sys

# Run validation
result = subprocess.run(
    ["datacheck", "validate", "data.csv",
     "--config", "rules.yaml",
     "--format", "json"],
    capture_output=True,
    text=True
)

# Parse JSON
data = json.loads(result.stdout)

if not data["summary"]["all_passed"]:
    print(f"❌ Validation failed!")
    print(f"Failed checks: {data['summary']['failed_checks']}")
    
    # Process failed checks
    for check in data["checks"]:
        if not check["passed"]:
            print(f"\nFailed: {check['name']}")
            for rule in check["rules"]:
                if not rule["passed"]:
                    print(f"  - {rule['rule']}: {rule['message']}")
                    print(f"    Failing rows: {rule['failing_rows']}")
    
    sys.exit(1)
else:
    print("✅ All validation checks passed")
    sys.exit(0)
```

---

## Comparison

| Feature | Terminal | JSON |
|---------|----------|------|
| **Human-readable** | ✅ Excellent | ❌ No |
| **Machine-readable** | ❌ No | ✅ Excellent |
| **Colors** | ✅ Yes | ❌ No |
| **Parsing** | ❌ Difficult | ✅ Easy |
| **CI/CD** | ⚠️ Limited | ✅ Perfect |
| **Debugging** | ✅ Great | ⚠️ Requires tools |

---

## Best Practices

1. **Local development** - Use terminal output for quick feedback
2. **CI/CD pipelines** - Use JSON output for automation
3. **Save results** - Always save JSON output to files for audit trails
4. **Parse carefully** - Handle JSON parsing errors gracefully
5. **Log both** - Consider logging terminal output AND saving JSON

---

## Next Steps

- Learn about [Exit Codes](exit-codes.md) for automation
- See [CI/CD Integration](../integration/cicd.md) examples
- Explore [Python API](../reference/python-api.md)
