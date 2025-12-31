# Basic DataCheck Example

This example demonstrates basic data validation using DataCheck.

## Files

- `sample_data.csv` - Sample employee data
- `validation_config.yaml` - Basic validation rules

## Validation Rules

The configuration validates:
- **Age**: Not null, between 18 and 120
- **Name**: Not null, minimum 2 characters
- **Email**: Not null, valid email format
- **Salary**: Not null, non-negative

## Running the Example

### Validate with terminal output:
```bash
datacheck validate sample_data.csv --config validation_config.yaml
```

### Validate with JSON output:
```bash
datacheck validate sample_data.csv --config validation_config.yaml --format json
```

### Save JSON results to file:
```bash
datacheck validate sample_data.csv --config validation_config.yaml --format json --json-output results.json
```

## Expected Output

All validation checks should **PASS** for this example data.

```
╭──────────────────────────────╮
│ DataCheck Validation Results │
╰──────────────────────────────╯

✓ ALL CHECKS PASSED

 Metric       Value
 Total Rules      7
 Passed           7
 Failed           0
 Errors           0
```

## Try It Yourself

Modify the data or configuration to see validation failures:

1. **Change age to invalid value** (e.g., 150):
   ```csv
   Alice Johnson,150,alice@example.com,75000
   ```

2. **Add invalid email**:
   ```csv
   Bob Smith,25,invalid-email,65000
   ```

3. **Add negative salary**:
   ```csv
   Carol White,35,carol@example.com,-1000
   ```

Run validation again to see how DataCheck reports failures!
