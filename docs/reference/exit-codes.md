# Exit Codes

DataCheck uses standard exit codes for CI/CD integration.

## Exit Code Reference

| Code | Status | Meaning | Action |
|------|--------|---------|--------|
| `0` | Success | All validations passed | Continue pipeline |
| `1` | Failed | Some validations failed | Fail build, investigate data |
| `2` | Error | Configuration error | Fix YAML syntax/rules |
| `3` | Error | Data loading error | Check file path/format |
| `4` | Error | Runtime error | Report bug |

---

## Exit Code 0: Success

**All validations passed.**

```bash
$ datacheck validate data.csv --config rules.yaml
✓ ALL CHECKS PASSED

$ echo $?
0
```

**Use in CI/CD:**
```yaml
- name: Validate data
  run: datacheck validate data.csv --config rules.yaml
  # Job continues if exit code is 0
```

---

## Exit Code 1: Validation Failed

**One or more validation rules failed.**

```bash
$ datacheck validate data.csv --config rules.yaml
✗ VALIDATION FAILED

Check: email_format
├─ Failed: 5/100 rows (5.0%)
└─ Sample failures: [10, 25, 42, 67, 89]

$ echo $?
1
```

**Causes:**
- Data doesn't meet validation rules
- Quality issues in data

**Resolution:**
- Fix data quality issues
- Update validation rules if they're too strict

**Use in CI/CD:**
```yaml
- name: Validate data
  run: |
    datacheck validate data.csv --config rules.yaml
    if [ $? -eq 1 ]; then
      echo "❌ Data quality check failed"
      exit 1
    fi
```

---

## Exit Code 2: Configuration Error

**Invalid validation configuration.**

```bash
$ datacheck validate data.csv --config rules.yaml
❌ Configuration Error: Invalid YAML syntax at line 5

$ echo $?
2
```

**Common Causes:**
- YAML syntax error
- Missing required fields (name, column, rules)
- Unknown validation rule
- Invalid rule value type

**Examples:**

### Invalid YAML
```yaml
checks:
  - name: test
    column: id
    rules:
      not_null true  # ❌ Missing colon
```

### Missing Required Field
```yaml
checks:
  - name: test
    # ❌ Missing 'column'
    rules:
      not_null: true
```

### Unknown Rule
```yaml
checks:
  - name: test
    column: id
    rules:
      unknown_rule: true  # ❌ Not valid
```

**Resolution:**
- Check YAML syntax
- Verify all required fields present
- Use only supported rules: `not_null`, `unique`, `min`, `max`, `regex`, `allowed_values`

---

## Exit Code 3: Data Loading Error

**Failed to load data file.**

```bash
$ datacheck validate missing.csv --config rules.yaml
❌ Error loading data: File not found: missing.csv

$ echo $?
3
```

**Common Causes:**
- File doesn't exist
- Wrong file path
- Insufficient permissions
- Unsupported file format
- Corrupted file

**Examples:**

### File Not Found
```bash
$ datacheck validate data/users.csv --config rules.yaml
❌ Error loading data: File not found: data/users.csv
```

### Wrong Database Format
```bash
$ datacheck validate app.db:users --config rules.yaml
❌ Error loading data: Invalid database format (use :: not :)
```

### Corrupted File
```bash
$ datacheck validate corrupted.parquet --config rules.yaml
❌ Error loading data: Unable to read Parquet file
```

**Resolution:**
- Verify file path is correct
- Check file exists and is readable
- Use correct format: `database.db::table` for databases
- Ensure file isn't corrupted

---

## Exit Code 4: Runtime Error

**Unexpected error during execution.**

```bash
$ datacheck validate data.csv --config rules.yaml
❌ Runtime Error: Unexpected error occurred
```

**Causes:**
- Unexpected exceptions
- System resource issues
- Software bugs

**Resolution:**
- Report issue on GitHub: https://github.com/yash-chauhan-dev/datacheck/issues
- Include error message, data format, and validation config

---

## Using Exit Codes in Scripts

### Bash

```bash
#!/bin/bash

datacheck validate data.csv --config rules.yaml
EXIT_CODE=$?

case $EXIT_CODE in
  0)
    echo "✅ All validations passed"
    ;;
  1)
    echo "❌ Validation failed"
    exit 1
    ;;
  2)
    echo "❌ Configuration error - fix rules.yaml"
    exit 1
    ;;
  3)
    echo "❌ Data loading error - check file path"
    exit 1
    ;;
  *)
    echo "❌ Unknown error"
    exit 1
    ;;
esac
```

### Python

```python
import subprocess
import sys

result = subprocess.run(
    ['datacheck', 'validate', 'data.csv', '--config', 'rules.yaml'],
    capture_output=True
)

if result.returncode == 0:
    print("✅ All validations passed")
elif result.returncode == 1:
    print("❌ Validation failed")
    sys.exit(1)
elif result.returncode == 2:
    print("❌ Configuration error")
    sys.exit(1)
elif result.returncode == 3:
    print("❌ Data loading error")
    sys.exit(1)
else:
    print(f"❌ Unknown error (code {result.returncode})")
    sys.exit(1)
```

### GitHub Actions

```yaml
- name: Validate data
  run: datacheck validate data.csv --config rules.yaml
  continue-on-error: false  # Fail job if exit code != 0

- name: Handle validation failure
  if: failure()
  run: |
    echo "Data validation failed!"
    # Send notification, create issue, etc.
```

### GitLab CI

```yaml
validate:
  script:
    - datacheck validate data.csv --config rules.yaml
  allow_failure: false  # Fail pipeline on non-zero exit
```

---

## Checking Exit Codes

### Bash
```bash
datacheck validate data.csv --config rules.yaml
echo "Exit code: $?"
```

### PowerShell
```powershell
datacheck validate data.csv --config rules.yaml
echo "Exit code: $LASTEXITCODE"
```

### Python
```python
import subprocess

result = subprocess.run(['datacheck', 'validate', 'data.csv'])
print(f"Exit code: {result.returncode}")
```

---

## Best Practices

### 1. Always Check Exit Codes in Scripts

```bash
# ✅ Good
datacheck validate data.csv --config rules.yaml
if [ $? -ne 0 ]; then
    echo "Validation failed"
    exit 1
fi

# ❌ Avoid ignoring exit codes
datacheck validate data.csv --config rules.yaml
# Script continues even if validation fails!
```

### 2. Handle Different Exit Codes Appropriately

```bash
# ✅ Good - Different actions for different errors
case $? in
  1) echo "Fix data quality"; exit 1 ;;
  2) echo "Fix configuration"; exit 1 ;;
  3) echo "Check file path"; exit 1 ;;
esac

# ❌ Avoid treating all errors the same
if [ $? -ne 0 ]; then
    echo "Something failed"
fi
```

### 3. Use in CI/CD Pipelines

```yaml
# ✅ Good - Explicit failure handling
- name: Validate
  run: |
    datacheck validate data.csv --config rules.yaml || exit 1
```
