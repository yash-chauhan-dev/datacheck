# DataCheck

<div align="center">

**Lightweight data quality validation CLI tool for data engineers**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/datacheck-cli.svg)](https://pypi.org/project/datacheck-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/yash-chauhan-dev/datacheck/workflows/CI/badge.svg)](https://github.com/yash-chauhan-dev/datacheck/actions)

[Get Started](getting-started/installation.md){ .md-button .md-button--primary }
[View on GitHub](https://github.com/yash-chauhan-dev/datacheck){ .md-button }

</div>

---

## What is DataCheck?

DataCheck is a **simple, fast, and CLI-first** data validation tool designed for data engineers who need to:

- :white_check_mark: **Validate data quality** without heavy frameworks
- :x: **Fail CI/CD pipelines** when data doesn't meet expectations
- :zap: **Get instant feedback** on data issues with beautiful terminal output
- :page_facing_up: **Write validation rules** in simple, declarative YAML

**Think of it as "pytest for data" - lightweight, focused, and developer-friendly.**

---

## Key Features

### :rocket: Multiple Data Formats

DataCheck supports all your data sources out of the box:

- **CSV** with automatic encoding detection
- **Parquet** for efficient columnar data
- **SQLite** and **DuckDB** for database tables

### :wrench: Comprehensive Validation Rules

Built-in validation rules for common data quality checks:

- `not_null` - Ensure no missing values
- `unique` - Detect duplicates
- `min` / `max` - Numeric range validation
- `regex` - Pattern matching for strings
- `allowed_values` - Whitelist validation

### :art: Beautiful Terminal Output

Colorful, rich terminal output powered by [Rich](https://rich.readthedocs.io/):

- Clear pass/fail indicators
- Detailed failure reports with row indices
- Summary statistics and metrics
- JSON output for automation

### :rocket: CI/CD Ready

Perfect for data pipelines and automation:

- Proper exit codes (0=pass, 1=fail)
- JSON output for programmatic use
- Fast validation using Pandas
- Works in GitHub Actions, GitLab CI, Jenkins, etc.

### :clipboard: Simple Configuration

Write validation rules in clean, readable YAML:

```yaml
checks:
  - name: email_validation
    column: email
    rules:
      not_null: true
      regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

  - name: age_validation
    column: age
    rules:
      min: 18
      max: 120
```

---

## Quick Example

```bash
# Install
pip install datacheck-cli

# Create validation rules
cat > validation.yaml << EOF
checks:
  - name: product_id_check
    column: product_id
    rules:
      not_null: true
      unique: true

  - name: price_validation
    column: price
    rules:
      min: 0
      max: 10000
EOF

# Run validation
datacheck validate products.csv --config validation.yaml
```

**Output**:
```
╭──────────────────────────────╮
│ DataCheck Validation Results │
╰──────────────────────────────╯

✓ ALL CHECKS PASSED

 Metric       Value
 Total Rules      4
 Passed           4
 Failed           0
 Errors           0
```

---

## Why DataCheck?

### :zap: Lightweight

- **No complex setup** - just install and use
- **Single binary** - no dependencies to manage
- **Fast** - processes millions of rows efficiently

### :dart: Focused

- **Does one thing well** - data validation
- **No feature bloat** - simple and maintainable
- **Clear API** - easy to understand and use

### :handshake: Developer-Friendly

- **CLI-first** - designed for command-line workflows
- **Git-friendly** - YAML configs version control easily
- **CI/CD native** - proper exit codes and JSON output

---

## Use Cases

### :factory: Data Pipelines

Validate data quality at every stage of your pipeline:

```bash
# In your ETL script
extract_data.sh
transform_data.py
datacheck validate output.csv --config quality-rules.yaml || exit 1
load_to_warehouse.py
```

### :test_tube: Pre-Production Checks

Ensure data meets quality standards before deployment:

```yaml
# .github/workflows/data-quality.yml
- name: Validate Data
  run: datacheck validate exports/*.csv --config validation.yaml
```

### :mag: Data Exploration

Quickly validate assumptions about your data:

```bash
# Check if customer emails are unique
datacheck validate customers.csv --config <(echo "
checks:
  - name: unique_emails
    column: email
    rules:
      unique: true
")
```

---

## Statistics

- :white_check_mark: **180 tests** passing
- :bar_chart: **92% code coverage**
- :safety_vest: **100% type checked** with mypy
- :rocket: **Zero lint errors** with ruff
- :package: **10 Python modules**
- :memo: **701 lines of code**

---

## Community

- :bug: [Report Issues](https://github.com/yash-chauhan-dev/datacheck/issues)
- :bulb: [Feature Requests](https://github.com/yash-chauhan-dev/datacheck/issues/new?template=feature_request.md)
- :books: [Documentation](https://yash-chauhan-dev.github.io/datacheck/)
- :star: [Star on GitHub](https://github.com/yash-chauhan-dev/datacheck)

---

## Next Steps

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __Get Started in 5 Minutes__

    ---

    Install DataCheck and run your first validation

    [:octicons-arrow-right-24: Quick Start](getting-started/quick-start.md)

-   :material-book-open-variant:{ .lg .middle } __Learn the Basics__

    ---

    Understand validation rules and configuration

    [:octicons-arrow-right-24: User Guide](user-guide/overview.md)

-   :material-code-braces:{ .lg .middle } __See Real Examples__

    ---

    Explore real-world validation scenarios

    [:octicons-arrow-right-24: Examples](examples/real-world.md)

-   :material-cog:{ .lg .middle } __Integrate with CI/CD__

    ---

    Add DataCheck to your automation workflows

    [:octicons-arrow-right-24: Integration Guide](integration/cicd.md)

</div>

---

Made with :heart: for data engineers who value simplicity and speed.
