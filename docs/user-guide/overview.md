# User Guide Overview

Welcome to the DataCheck User Guide! This section covers everything you need to know to use DataCheck effectively.

---

## What's in This Guide

### [Validation Rules](validation-rules.md)
Complete reference of all available validation rules with examples.

### [Configuration](configuration.md)
Learn how to write validation configuration files in YAML.

### [Output Formats](output-formats.md)
Understand terminal and JSON output formats.

### [Exit Codes](exit-codes.md)
Learn how DataCheck uses exit codes for automation.

---

## Key Concepts

### Data Validation

DataCheck validates data by applying **rules** to **columns** in your dataset. Each rule checks a specific condition.

```yaml
checks:
  - name: age_check      # Descriptive name for this check
    column: age          # Column to validate
    rules:               # Rules to apply
      not_null: true
      min: 18
      max: 120
```

### Validation Checks

A **check** is a named collection of rules applied to a single column. You can have multiple checks per file.

### Rules

**Rules** are the actual validation logic:

- `not_null`: No missing values
- `unique`: No duplicates
- `min`/`max`: Numeric ranges
- `regex`: Pattern matching
- `allowed_values`: Whitelist

### Results

DataCheck provides detailed results:

- **Pass/Fail status** for each rule
- **Failure counts** and percentages
- **Sample row indices** that failed
- **Summary statistics**

---

## Basic Workflow

1. **Prepare your data** (CSV, Parquet, SQLite, DuckDB)
2. **Write validation rules** in YAML
3. **Run validation** with `datacheck validate`
4. **Review results** in terminal or JSON
5. **Fix issues** or update rules
6. **Integrate** into your data pipeline

---

## Quick Reference

```bash
# Basic validation
datacheck validate data.csv --config rules.yaml

# Auto-discover config
datacheck validate data.csv  # Looks for .datacheck.yaml

# JSON output
datacheck validate data.csv --config rules.yaml --format json

# Save JSON to file
datacheck validate data.csv --config rules.yaml \
  --format json --json-output results.json

# Validate Parquet
datacheck validate data.parquet --config rules.yaml

# Validate database table
datacheck validate data.db --table customers --config rules.yaml
```

---

## Next Steps

- Learn about [Validation Rules](validation-rules.md)
- Understand [Configuration](configuration.md)
- Explore [Output Formats](output-formats.md)
