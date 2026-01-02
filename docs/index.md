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
      text: View Use Cases
      link: /use-cases/
  image:
    src: /hero.svg
    alt: DataCheck Data Validation

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

## Quick Start

Get started with DataCheck in under 2 minutes.

::: code-group

```bash [Install]
pip install datacheck-cli
```

```yaml [Create Rules]
# validation.yaml
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
```

```bash [Run Validation]
datacheck validate users.csv --config validation.yaml
```

```text [Output]
╭──────────────────────────────╮
│ DataCheck Validation Results │
╰──────────────────────────────╯

✓ ALL CHECKS PASSED

 Metric       Value
 Total Rules      4
 Passed           4
 Failed           0
```

:::

## Why DataCheck?

- **10x less code** - Replace 100+ lines of Python with 10 lines of YAML
- **6x faster setup** - From 30 minutes to 5 minutes
- **Save 8 hours/month** - Catch issues in 30 seconds instead of 2 hours
- **Save $100+/month** - Prevent wasted GPU training costs

## The Problem DataCheck Solves

### ❌ Without DataCheck

```python
# validate.py - 100+ lines
import pandas as pd
import sys

df = pd.read_csv('data.csv')
errors = []

# Email validation
if df['email'].isnull().any():
    errors.append('Email has null values')

pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
if not df['email'].str.match(pattern).all():
    errors.append('Invalid email')

# Age validation
if (df['age'] < 18).any():
    errors.append('Age < 18')
if (df['age'] > 120).any():
    errors.append('Age > 120')

# Status validation
valid = ['active', 'inactive']
if not df['status'].isin(valid).all():
    errors.append('Invalid status')

# ... 80 more lines ...

if errors:
    for e in errors:
        print(f"❌ {e}")
    sys.exit(1)
```

**Problems:**
- Requires Python expertise
- Hard to maintain
- Tightly coupled to code
- 100+ lines for simple checks

### ✅ With DataCheck

```yaml
# validation.yaml - 15 lines
checks:
  - name: email_validation
    column: email
    rules:
      not_null: true
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"

  - name: age_validation
    column: age
    rules:
      min: 18
      max: 120

  - name: status_validation
    column: status
    rules:
      allowed_values: ["active", "inactive"]
```

```bash
# Run validation
datacheck validate data.csv --config validation.yaml
```

**Benefits:**
- ✅ No coding required
- ✅ Easy to understand and modify
- ✅ Decoupled from codebase
- ✅ 85% less code

## Use Cases

### 🏭 Airflow Pipelines

Stop wasting hours on bad data. Validate before expensive transformations and catch issues in 30 seconds instead of 2 hours.

[Learn more →](/use-cases/#airflow-data-pipelines)

### 🤖 ML Training Pipelines

Don't waste expensive GPU time on bad training data. Validate before you train and save $100+ per month.

[Learn more →](/use-cases/#ml-training-pipelines)

### 🤝 Data Contracts Between Teams

Turn validation configs into living contracts. Both producer and consumer teams validate against the same contract - breaking changes caught in CI/CD, not production.

[Learn more →](/use-cases/#data-contracts-between-teams)

## Supported Data Formats

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin: 2rem 0;">

<div style="display: flex; gap: 1rem; align-items: start; padding: 1.5rem; border: 1px solid #e5e7eb; border-radius: 8px;">
  <img src="/csv-icon.svg" alt="CSV" width="48" height="48" style="flex-shrink: 0;" />
  <div>
    <h3 style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">CSV Files</h3>
    <p style="margin: 0 0 0.75rem 0; color: #6b7280; font-size: 0.9rem;">Automatic encoding detection, any delimiter</p>
    <code style="background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem;">datacheck validate users.csv</code>
  </div>
</div>

<div style="display: flex; gap: 1rem; align-items: start; padding: 1.5rem; border: 1px solid #e5e7eb; border-radius: 8px;">
  <img src="/parquet-icon.svg" alt="Parquet" width="48" height="48" style="flex-shrink: 0;" />
  <div>
    <h3 style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">Parquet Files</h3>
    <p style="margin: 0 0 0.75rem 0; color: #6b7280; font-size: 0.9rem;">High performance columnar format for big data</p>
    <code style="background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem;">datacheck validate data.parquet</code>
  </div>
</div>

<div style="display: flex; gap: 1rem; align-items: start; padding: 1.5rem; border: 1px solid #e5e7eb; border-radius: 8px;">
  <img src="/sqlite-icon.svg" alt="SQLite" width="48" height="48" style="flex-shrink: 0;" />
  <div>
    <h3 style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">SQLite Database</h3>
    <p style="margin: 0 0 0.75rem 0; color: #6b7280; font-size: 0.9rem;">Validate tables directly, no export needed</p>
    <code style="background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem;">datacheck validate app.db::users</code>
  </div>
</div>

<div style="display: flex; gap: 1rem; align-items: start; padding: 1.5rem; border: 1px solid #e5e7eb; border-radius: 8px;">
  <img src="/duckdb-icon.svg" alt="DuckDB" width="48" height="48" style="flex-shrink: 0;" />
  <div>
    <h3 style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">DuckDB Database</h3>
    <p style="margin: 0 0 0.75rem 0; color: #6b7280; font-size: 0.9rem;">Analytics on large datasets (Linux/macOS only)</p>
    <code style="background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem;">datacheck validate data.duckdb::events</code>
  </div>
</div>

</div>
