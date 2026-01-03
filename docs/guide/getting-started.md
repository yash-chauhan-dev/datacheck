# Getting Started

DataCheck validates your data against rules you define in YAML. It's that simple.

## Installation

```bash
pip install datacheck-cli
```

## Your First Validation

Create a CSV file `users.csv`:
```csv
name,email,age
John,john@example.com,25
Jane,jane@example.com,30
Bob,invalid-email,150
```

Create validation rules `rules.yaml`:
```yaml
checks:
  - name: email_format
    column: email
    rules:
      not_null: true
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"

  - name: age_range
    column: age
    rules:
      min: 18
      max: 120
```

Run validation:
```bash
datacheck validate users.csv --config rules.yaml
```

Output:
```
╭──────────────────────────────╮
│ DataCheck Validation Results │
╰──────────────────────────────╯

VALIDATION FAILED

Check: email_format
├─ Column: email
├─ Rule: regex
├─ Failed: 1/3 rows (33.3%)
└─ Sample failures: [2]

Check: age_range
├─ Column: age
├─ Rule: max
├─ Failed: 1/3 rows (33.3%)
└─ Sample failures: [2]

Summary:
  Total Rules: 4
  Passed: 2
  Failed: 2
```

## What Just Happened?

1. DataCheck loaded your CSV file
2. Checked each validation rule against your data
3. Found 2 issues:
   - Row 2: Invalid email format
   - Row 2: Age exceeds maximum (150 > 120)
4. Exited with code `1` (validation failed)

## Exit Codes

- `0`: All validations passed
- `1`: Some validations failed
- `2`: Configuration error
- `3`: Data loading error

Use these in your CI/CD pipelines to fail builds on bad data.

## Next Steps

- [Learn about validation rules](/guide/validation-rules)
- [See more examples](/examples/quick-start)
- [Use in CI/CD](/examples/cicd)
