# Exit Codes

DataCheck uses standard exit codes for automation and CI/CD integration.

---

## Exit Code Reference

| Code | Name | Description | Action |
|------|------|-------------|--------|
| `0` | Success | All validations passed | Continue pipeline |
| `1` | Validation Failed | Some rules failed | Stop pipeline |
| `2` | Config Error | Configuration file error | Fix config |
| `3` | Data Error | Data loading error | Check data source |
| `4` | Runtime Error | Unexpected error | Debug/report bug |

---

## Exit Code 0: Success

**When**: All validation rules pass

**Example**:
```bash
$ datacheck validate data.csv --config rules.yaml
# All checks passed
$ echo $?
0
```

**In Scripts**:
```bash
if datacheck validate data.csv --config rules.yaml; then
  echo "✅ Validation passed!"
  python load_to_warehouse.py
fi
```

---

## Exit Code 1: Validation Failed

**When**: One or more validation rules fail

**Example**:
```bash
$ datacheck validate data.csv --config rules.yaml
# Some checks failed
$ echo $?
1
```

**In Scripts**:
```bash
datacheck validate data.csv --config rules.yaml

if [ $? -eq 1 ]; then
  echo "❌ Validation failed!"
  python send_alert.py
  exit 1
fi
```

---

## Exit Code 2: Config Error

**When**: Configuration file has errors

**Common Causes**:
- Invalid YAML syntax
- Missing required fields
- Unknown rule types
- File not found

**Example**:
```bash
$ datacheck validate data.csv --config invalid.yaml
Error: Failed to load configuration
$ echo $?
2
```

**In Scripts**:
```bash
datacheck validate data.csv --config rules.yaml

case $? in
  0)
    echo "✅ Passed"
    ;;
  1)
    echo "❌ Failed validation"
    ;;
  2)
    echo "⚙️  Config error - check YAML syntax"
    ;;
esac
```

---

## Exit Code 3: Data Error

**When**: Data file cannot be loaded

**Common Causes**:
- File not found
- Invalid file format
- Encoding issues
- Permission denied

**Example**:
```bash
$ datacheck validate missing.csv --config rules.yaml
Error: Failed to load data
$ echo $?
3
```

---

## Exit Code 4: Runtime Error

**When**: Unexpected error during execution

**Common Causes**:
- Out of memory
- Disk space issues
- Network problems (if loading from URL)
- Bug in DataCheck

**Example**:
```bash
$ datacheck validate data.csv --config rules.yaml
Error: Unexpected runtime error
$ echo $?
4
```

**Action**: Report bug with error message

---

## Usage in CI/CD

### GitHub Actions

```yaml
- name: Validate Data
  run: |
    datacheck validate data.csv --config rules.yaml
    
- name: Handle Failure
  if: failure()
  run: |
    echo "Validation failed - check logs"
    exit 1
```

### GitLab CI

```yaml
validate:
  script:
    - datacheck validate data.csv --config rules.yaml
  allow_failure: false  # Fail pipeline if validation fails
```

### Jenkins

```groovy
stage('Data Validation') {
  steps {
    sh 'datacheck validate data.csv --config rules.yaml'
  }
  post {
    failure {
      mail to: 'team@example.com',
           subject: "Data Validation Failed",
           body: "Check the build logs"
    }
  }
}
```

---

## Best Practices

1. **Always check exit codes** in automation scripts
2. **Handle each code differently** for better error messages
3. **Log failures** for debugging
4. **Alert on failures** in production pipelines
5. **Don't ignore errors** - investigate all failures

---

## Examples

### Bash Script

```bash
#!/bin/bash
set -e  # Exit on any error

echo "Running data validation..."
datacheck validate data.csv --config rules.yaml

EXIT_CODE=$?

case $EXIT_CODE in
  0)
    echo "✅ Validation passed - continuing pipeline"
    ./load_data.sh
    ;;
  1)
    echo "❌ Validation failed - stopping pipeline"
    ./send_alert.sh "Data validation failed"
    exit 1
    ;;
  2)
    echo "⚙️  Configuration error - check rules.yaml"
    exit 2
    ;;
  3)
    echo "📁 Data loading error - check data.csv"
    exit 3
    ;;
  4)
    echo "💥 Runtime error - investigate logs"
    exit 4
    ;;
esac
```

### Python Script

```python
import subprocess
import sys

result = subprocess.run(
    ["datacheck", "validate", "data.csv", "--config", "rules.yaml"],
    capture_output=True
)

if result.returncode == 0:
    print("✅ Validation passed")
    # Continue with data processing
    
elif result.returncode == 1:
    print("❌ Validation failed")
    print(result.stdout.decode())
    sys.exit(1)
    
elif result.returncode == 2:
    print("⚙️  Configuration error")
    sys.exit(2)
    
elif result.returncode == 3:
    print("📁 Data loading error")
    sys.exit(3)
    
else:
    print("💥 Runtime error")
    sys.exit(4)
```

---

## Next Steps

- See [CI/CD Integration](../integration/cicd.md) for more examples
- Learn about [Output Formats](output-formats.md)
- Check [GitHub Actions](../integration/github-actions.md) guide
