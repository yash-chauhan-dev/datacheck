# CLI Reference

## Commands

### validate

Validate data file against configured quality rules.

```bash
datacheck validate <file> [options]
```

**Arguments:**
- `<file>` - Path to data file (CSV, Parquet, or database)

**Options:**
- `--config PATH` - Path to validation config file (YAML)
- `--output FORMAT` - Output format: `terminal` (default) or `json`

**Examples:**
```bash
# Basic validation
datacheck validate users.csv --config rules.yaml

# JSON output
datacheck validate users.csv --config rules.yaml --output json

# Auto-discovery (.datacheck.yaml)
datacheck validate users.csv

# Database table
datacheck validate app.db::users --config rules.yaml

# Parquet file
datacheck validate data.parquet --config rules.yaml
```

---

### version

Display version information.

```bash
datacheck version
```

**Output:**
```
DataCheck 0.1.1
```

---

## File Formats

### CSV Files
```bash
datacheck validate data.csv --config rules.yaml
```

### Parquet Files
```bash
datacheck validate data.parquet --config rules.yaml
```

### SQLite Database
```bash
# Format: database.db::table_name
datacheck validate app.db::users --config rules.yaml
```

### DuckDB Database (Linux/macOS)
```bash
# Requires: pip install datacheck-cli[duckdb]
datacheck validate analytics.duckdb::events --config rules.yaml
```

---

## Output Formats

### Terminal Output (Default)

Beautiful, colored output for humans.

```bash
datacheck validate data.csv --config rules.yaml
```

**Output:**
```
╭──────────────────────────────╮
│ DataCheck Validation Results │
╰──────────────────────────────╯

✗ VALIDATION FAILED

Check: email_format
├─ Column: email
├─ Rule: regex
├─ Failed: 2/100 rows (2.0%)
└─ Sample failures: [15, 42]

Summary:
  Total Rules: 5
  Passed: 3
  Failed: 2
```

### JSON Output

Machine-readable output for automation.

```bash
datacheck validate data.csv --config rules.yaml --output json
```

**Output:**
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
      "rule": "regex",
      "status": "failed",
      "failures": {
        "count": 2,
        "percentage": 2.0,
        "sample_rows": [15, 42]
      }
    }
  ]
}
```

---

## Exit Codes

DataCheck uses standard exit codes for CI/CD integration:

| Code | Meaning | Action |
|------|---------|--------|
| `0` | All validations passed | Continue pipeline |
| `1` | Some validations failed | Fail build |
| `2` | Configuration error | Fix config file |
| `3` | Data loading error | Check file path/format |
| `4` | Runtime error | Report bug |

**Usage in scripts:**
```bash
datacheck validate data.csv --config rules.yaml
if [ $? -eq 0 ]; then
    echo "✅ Validation passed"
else
    echo "❌ Validation failed"
    exit 1
fi
```

---

## Config Auto-discovery

Place `.datacheck.yaml` in your working directory:

```
project/
├── .datacheck.yaml
└── data.csv
```

Then run without `--config`:
```bash
datacheck validate data.csv
```

DataCheck automatically finds and uses `.datacheck.yaml`.

---

## Environment Variables

Currently DataCheck doesn't use environment variables. All configuration is via command-line arguments and YAML files.

---

## Shell Completion

Coming in future release.

---

## Common Usage Patterns

### Local Development
```bash
# Quick validation during development
datacheck validate test-data.csv --config dev-rules.yaml
```

### CI/CD Pipeline
```bash
# Strict validation in production
datacheck validate prod-data.csv --config prod-rules.yaml

# JSON output for processing
datacheck validate data.csv --config rules.yaml --output json > results.json
```

### Data Pipeline
```bash
# Validate at each stage
datacheck validate raw/data.csv --config validation/raw.yaml
datacheck validate cleaned/data.csv --config validation/clean.yaml
datacheck validate final/data.parquet --config validation/final.yaml
```

### Multiple Files
```bash
# Validate multiple files
for file in data/*.csv; do
    datacheck validate "$file" --config rules/$(basename "$file" .csv).yaml
done
```
