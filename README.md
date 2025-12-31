# DataCheck

> Lightweight data quality validation CLI tool for data engineers

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue.svg)](https://yash-chauhan-dev.github.io/datacheck/)

📚 **[Read the Full Documentation](https://yash-chauhan-dev.github.io/datacheck/)** 📚

## What is DataCheck?

DataCheck is a **simple, fast, and CLI-first** data validation tool for engineers who need to:
- ✅ Validate data quality without heavy frameworks
- ✅ Fail CI/CD pipelines when data doesn't meet expectations
- ✅ Get instant, beautiful feedback on data issues
- ✅ Write validation rules in simple YAML

**Think of it as "pytest for data" - lightweight, focused, and developer-friendly.**

---

## Quick Start

### Installation

```bash
# From PyPI (when published)
pip install datacheck-cli

# From source
git clone https://github.com/yash-chauhan-dev/datacheck.git
cd datacheck
pip install -e .
```

### Your First Validation

**1. Create sample data** (`employees.csv`):
```csv
name,age,email,salary
Alice,30,alice@example.com,75000
Bob,25,bob@example.com,65000
Carol,35,carol@example.com,85000
```

**2. Create validation rules** (`validation.yaml`):
```yaml
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
      regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

  - name: salary_range
    column: salary
    rules:
      not_null: true
      min: 0
```

**3. Run validation**:
```bash
datacheck validate employees.csv --config validation.yaml
```

**4. See beautiful results**:
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

---

## Features

### 🚀 **Multiple Data Formats**
- **CSV** (with automatic encoding detection)
- **Parquet** (efficient columnar format)
- **DuckDB/SQLite** (SQL databases)

### 📝 **Simple YAML Configuration**
- Easy to write and version control
- Clear, declarative syntax
- Reusable validation configs

### 🎨 **Beautiful Terminal Output**
- Rich, colorful output using [Rich](https://rich.readthedocs.io/)
- Clear pass/fail indicators
- Detailed failure reports with row indices
- JSON output for programmatic use

### ⚡ **CI/CD Ready**
- Proper exit codes (0=pass, 1=fail, 2+=errors)
- JSON output for automation
- Fast validation using Pandas

### 🔧 **Comprehensive Validation Rules**
- `not_null` - No missing values
- `min` / `max` - Numeric range validation
- `unique` - Detect duplicates
- `regex` - Pattern matching
- `allowed_values` - Enum/whitelist validation

### 📊 **Detailed Reporting**
- Pass/fail statistics
- Sample failure indices
- Failure rates and percentages
- Export results to JSON

---

## Usage

### Basic Command

```bash
datacheck validate <file> --config <config.yaml>
```

### Common Options

```bash
# Auto-discover config file (.datacheck.yaml)
datacheck validate data.csv

# JSON output
datacheck validate data.csv --config rules.yaml --format json

# Save JSON results
datacheck validate data.csv --config rules.yaml --format json --json-output results.json

# Show version
datacheck version
```

### Exit Codes

DataCheck uses exit codes for automation and CI/CD:

| Code | Meaning | Description |
|------|---------|-------------|
| `0` | Success | All validation rules passed |
| `1` | Failed | Some validation rules failed |
| `2` | Config Error | Configuration file error |
| `3` | Data Error | Data loading error |
| `4` | Runtime Error | Unexpected error |

**Use in scripts**:
```bash
datacheck validate data.csv --config rules.yaml
if [ $? -eq 0 ]; then
  echo "✓ Data validation passed"
  python load_to_warehouse.py
else
  echo "✗ Data validation failed"
  exit 1
fi
```

---

## Validation Rules Reference

### Data Presence

#### `not_null`
Ensures no missing/null values in column.

```yaml
- name: required_field
  column: user_id
  rules:
    not_null: true
```

#### `unique`
Ensures all values are unique (no duplicates).

```yaml
- name: unique_emails
  column: email
  rules:
    unique: true
```

### Numeric Validation

#### `min` / `max`
Validates numeric ranges (inclusive).

```yaml
- name: age_range
  column: age
  rules:
    min: 18
    max: 120
```

### String Validation

#### `regex`
Pattern matching using regular expressions.

```yaml
- name: email_format
  column: email
  rules:
    regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
```

**Common patterns**:
```yaml
# Email
regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

# Phone (US)
regex: "^\\+1-[0-9]{3}-[0-9]{3}-[0-9]{4}$"

# UUID
regex: "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"

# ISO Date
regex: "^\\d{4}-\\d{2}-\\d{2}$"
```

### Value Constraints

#### `allowed_values`
Restricts values to a specific list.

```yaml
- name: status_validation
  column: status
  rules:
    allowed_values: ["pending", "approved", "rejected"]
```

### Combining Rules

Multiple rules on one column:

```yaml
- name: comprehensive_validation
  column: user_age
  rules:
    not_null: true    # Required
    unique: false      # Duplicates OK
    min: 13           # COPPA compliance
    max: 120          # Reasonable maximum
```

---

## Configuration Guide

### Basic Structure

```yaml
checks:
  - name: <check_name>
    column: <column_name>
    rules:
      <rule_type>: <rule_value>
```

### Auto-Discovery

DataCheck automatically searches for config files:
- `.datacheck.yaml`
- `.datacheck.yml`
- `datacheck.yaml`
- `datacheck.yml`

```bash
# Will auto-discover config
datacheck validate data.csv
```

### Multiple Checks

Validate multiple columns:

```yaml
checks:
  - name: user_id_validation
    column: user_id
    rules:
      not_null: true
      unique: true

  - name: email_validation
    column: email
    rules:
      not_null: true
      unique: true
      regex: ".+@.+\\..+"

  - name: age_validation
    column: age
    rules:
      min: 0
      max: 150
```

### Comments and Documentation

```yaml
checks:
  # User identification validation
  - name: user_id_check
    column: user_id
    rules:
      not_null: true      # Required field
      unique: true         # No duplicate users

  # GDPR compliance - must be 16+ in EU
  - name: age_compliance
    column: age
    rules:
      min: 16             # GDPR minimum age
      max: 120            # Reasonable upper bound
```

---

## Examples

DataCheck includes comprehensive examples in the [`examples/`](examples/) directory:

### Basic Example
```bash
cd examples/basic
datacheck validate sample_data.csv --config validation_config.yaml
```

### Advanced Example (with errors)
```bash
cd examples/advanced
datacheck validate customer_data_with_errors.csv --config validation_config.yaml
```

### Real-World Examples
```bash
cd examples/real-world
# E-commerce sales validation
datacheck validate sales_data.csv --config sales_validation.yaml

# User account validation
datacheck validate user_data.csv --config user_validation.yaml
```

**See [examples/README.md](examples/README.md) for detailed documentation.**

---

## Integration Patterns

### Python Integration

```python
import subprocess
import json

def validate_data(file_path, config_path):
    """Run DataCheck validation and return results."""
    result = subprocess.run(
        ["datacheck", "validate", file_path,
         "--config", config_path, "--format", "json"],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        return {"status": "passed", "data": json.loads(result.stdout)}
    elif result.returncode == 1:
        return {"status": "failed", "data": json.loads(result.stdout)}
    else:
        return {"status": "error", "message": result.stderr}

# Usage
results = validate_data("data.csv", "rules.yaml")
if results["status"] == "passed":
    print("✓ Validation passed")
    # Proceed with data processing
```

### CI/CD Integration

**GitHub Actions**:
```yaml
name: Data Quality Check

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'

      - name: Install DataCheck
        run: pip install datacheck-cli

      - name: Validate Data
        run: |
          datacheck validate data/export.csv \
            --config validation/rules.yaml \
            --format json \
            --json-output results.json

      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v2
        with:
          name: validation-results
          path: results.json
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running data validation..."

for file in $(git diff --cached --name-only | grep '\.csv$'); do
  datacheck validate "$file" --config validation/data.yaml
  if [ $? -ne 0 ]; then
    echo "✗ Validation failed for $file"
    exit 1
  fi
done

echo "✓ All data files validated successfully"
```

### Data Pipeline Integration

```python
# Apache Airflow DAG
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

dag = DAG('data_quality_check', start_date=datetime(2024, 1, 1))

validate_task = BashOperator(
    task_id='validate_data',
    bash_command='datacheck validate /data/export.csv --config /configs/rules.yaml',
    dag=dag
)

load_task = PythonOperator(
    task_id='load_to_warehouse',
    python_callable=load_data,
    dag=dag
)

validate_task >> load_task  # Load only if validation passes
```

---

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/yash-chauhan-dev/datacheck.git
cd datacheck

# Install with development dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=datacheck --cov-report=html

# Run specific test categories
poetry run pytest -m unit          # Unit tests only
poetry run pytest -m integration   # Integration tests only
poetry run pytest -m "not slow"    # Exclude slow tests
```

### Code Quality

```bash
# Type checking
poetry run mypy datacheck/

# Linting
poetry run ruff check datacheck/ tests/

# Format code
poetry run ruff format datacheck/ tests/
```

### Project Statistics

- **180 tests** passing (92.14% coverage)
- **Type-safe** with mypy
- **Linted** with ruff
- **Documented** with comprehensive examples

---

## Architecture

DataCheck is built with a modular architecture:

```
datacheck/
├── cli.py          # CLI interface (Typer)
├── config.py       # YAML configuration parsing
├── engine.py       # Validation orchestration
├── loader.py       # Data loading (CSV, Parquet, SQL)
├── rules.py        # Validation rule implementations
├── results.py      # Result aggregation and reporting
├── output.py       # Terminal and JSON output formatting
└── exceptions.py   # Custom exceptions
```

**Design Principles**:
- **Separation of Concerns**: Each module has a single responsibility
- **Extensibility**: Easy to add new rules and loaders
- **Type Safety**: Fully typed with mypy
- **Testability**: 92% test coverage
- **CLI-First**: Optimized for command-line usage

---

## Roadmap

### v0.2.0 (Next Release)
- [ ] Database connection strings
- [ ] Custom rule definitions in Python
- [ ] HTML report generation
- [ ] Performance benchmarking mode

### v0.3.0
- [ ] Data profiling and statistics
- [ ] Column correlation analysis
- [ ] Anomaly detection
- [ ] Schema validation

### Future
- [ ] Web UI for results
- [ ] Real-time data stream validation
- [ ] Machine learning-based validation
- [ ] Integration with dbt

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Coding standards
- Pull request process
- Adding new features

---

## FAQ

**Q: How is DataCheck different from Great Expectations?**
A: DataCheck is lightweight and CLI-first, designed for engineers who want fast validation without extensive setup. Great Expectations is more comprehensive but requires more configuration.

**Q: Can I use DataCheck in production?**
A: Yes! DataCheck is designed for production use in CI/CD pipelines and data workflows. See the [examples/real-world](examples/real-world/) directory.

**Q: Does DataCheck support custom validation rules?**
A: Currently, DataCheck supports a core set of rules. Custom rules via Python plugins are planned for v0.2.0.

**Q: How fast is DataCheck?**
A: DataCheck is built on Pandas and processes data efficiently. For example, validating 1M rows with 10 rules takes ~2-3 seconds on standard hardware.

**Q: Can DataCheck handle large files?**
A: Yes, DataCheck uses Pandas which efficiently handles millions of rows. For very large files (GB+), consider using Parquet format for better performance.

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Acknowledgments

Built with:
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Pandas](https://pandas.pydata.org/) - Data processing
- [Rich](https://rich.readthedocs.io/) - Terminal output
- [DuckDB](https://duckdb.org/) - SQL support
- [PyArrow](https://arrow.apache.org/docs/python/) - Parquet support

---

## Support

- **Documentation**: [https://yash-chauhan-dev.github.io/datacheck/](https://yash-chauhan-dev.github.io/datacheck/)
- **Examples**: [examples/README.md](examples/README.md)
- **Issues**: [GitHub Issues](https://github.com/yash-chauhan-dev/datacheck/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yash-chauhan-dev/datacheck/discussions)

---

**Made with ❤️ for data engineers who value simplicity and speed.**
