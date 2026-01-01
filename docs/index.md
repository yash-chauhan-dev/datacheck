---
layout: home

hero:
  name: DataCheck
  text: Data Quality Validation Made Simple
  tagline: Lightweight CLI tool for validating data quality in your pipelines
  actions:
    - theme: brand
      text: Get Started
      link: /guide/getting-started
    - theme: alt
      text: View Examples
      link: /examples/quick-start
  image:
    src: /hero.svg
    alt: DataCheck

features:
  - icon: ⚡
    title: Fast & Lightweight
    details: Validate millions of rows in seconds. No heavy frameworks, just pure speed.

  - icon: 📝
    title: Simple YAML Configuration
    details: Write validation rules in clean, readable YAML. No code required.

  - icon: 🎯
    title: Built for CI/CD
    details: Proper exit codes, JSON output, and seamless integration with any CI/CD platform.

  - icon: 📊
    title: Multiple Formats
    details: CSV, Parquet, SQLite, and DuckDB support out of the box.

  - icon: 🔍
    title: Detailed Reports
    details: Beautiful terminal output with precise failure information and row indices.

  - icon: 🚀
    title: Zero Setup
    details: Install with pip and start validating. No configuration files, no complex setup.
---

## Quick Example

```bash
# Install
pip install datacheck-cli

# Create a validation config
cat > rules.yaml << EOF
checks:
  - name: email_validation
    column: email
    rules:
      not_null: true
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"

  - name: age_check
    column: age
    rules:
      min: 18
      max: 120
EOF

# Validate your data
datacheck validate users.csv --config rules.yaml
```

## Why DataCheck?

**Before DataCheck:**
```python
# 100+ lines of custom validation code
import pandas as pd

df = pd.read_csv('data.csv')
errors = []

if df['email'].isnull().any():
    errors.append('Email has null values')

if not df['email'].str.match(r'^[\w\.-]+@[\w\.-]+\.\w+$').all():
    errors.append('Invalid email format')

# ... 90 more lines ...
```

**With DataCheck:**
```yaml
# 10 lines of YAML
checks:
  - name: email_validation
    column: email
    rules:
      not_null: true
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"
```

**Result:** 10x less code, 6x faster setup, anyone can contribute.

## Use Cases

### Airflow Pipelines
Validate data before expensive transformations. Catch bad data in 30 seconds instead of discovering it after 2 hours of processing.

### ML Training
Validate training data before starting expensive GPU jobs. Save $50-100/month in wasted compute costs.

### Data Contracts
Turn validation configs into living documentation between teams. Prevent breaking changes before they reach production.

### CI/CD Quality Gates
Add data validation as a required check in your PR workflow. Fail fast when data quality drops.

## Next Steps

<div style="display: flex; gap: 1rem; margin-top: 2rem;">
  <a href="/guide/getting-started" style="flex: 1; padding: 1rem; border: 1px solid #3eaf7c; border-radius: 8px; text-decoration: none; text-align: center;">
    <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;">📖 Read the Guide</div>
    <div>Learn the basics in 5 minutes</div>
  </a>
  <a href="/examples/quick-start" style="flex: 1; padding: 1rem; border: 1px solid #3eaf7c; border-radius: 8px; text-decoration: none; text-align: center;">
    <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;">🚀 See Examples</div>
    <div>Real-world validation scenarios</div>
  </a>
</div>
