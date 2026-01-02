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

## Why Teams Choose DataCheck

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin: 2rem 0;">

<div style="padding: 1.5rem; background: #f9fafb; border: 2px solid #e5e7eb; border-radius: 12px;">
  <div style="font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem; color: #1f2937;">10x</div>
  <div style="font-size: 1.1rem; color: #374151;">Less code than custom validation</div>
  <div style="margin-top: 1rem; color: #6b7280; font-size: 0.9rem;">Replace 100+ lines of Python with 10 lines of YAML</div>
</div>

<div style="padding: 1.5rem; background: #f9fafb; border: 2px solid #e5e7eb; border-radius: 12px;">
  <div style="font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem; color: #1f2937;">6x</div>
  <div style="font-size: 1.1rem; color: #374151;">Faster to set up</div>
  <div style="margin-top: 1rem; color: #6b7280; font-size: 0.9rem;">From 30 minutes to 5 minutes</div>
</div>

<div style="padding: 1.5rem; background: #f9fafb; border: 2px solid #e5e7eb; border-radius: 12px;">
  <div style="font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem; color: #1f2937;">8 hrs</div>
  <div style="font-size: 1.1rem; color: #374151;">Saved per month</div>
  <div style="margin-top: 1rem; color: #6b7280; font-size: 0.9rem;">Catch issues in 30 seconds vs 2 hours</div>
</div>

<div style="padding: 1.5rem; background: #f9fafb; border: 2px solid #e5e7eb; border-radius: 12px;">
  <div style="font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem; color: #1f2937;">$100</div>
  <div style="font-size: 1.1rem; color: #374151;">Saved per month</div>
  <div style="margin-top: 1rem; color: #6b7280; font-size: 0.9rem;">Prevent wasted GPU training costs</div>
</div>

</div>

## The Problem DataCheck Solves

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin: 2rem 0;">

<div>

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

</div>

<div>

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

</div>

</div>

## Real-World Impact

Teams use DataCheck to prevent costly data quality issues in production pipelines.

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem; margin: 3rem 0;">

<div style="background: #ffffff; padding: 2.5rem; border-radius: 16px; border: 2px solid #e5e7eb; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">
  <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
    <div style="font-size: 3rem;">🏭</div>
    <h3 style="margin: 0; color: #1f2937; font-size: 1.5rem;">Airflow Pipelines</h3>
  </div>

  <p style="font-size: 1.05rem; color: #4b5563; margin-bottom: 1.5rem; line-height: 1.6;">Stop wasting hours on bad data. Validate before expensive transformations and catch issues instantly.</p>

  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1.5rem 0;">
    <div style="background: #f9fafb; padding: 1.25rem; border-radius: 10px; border: 1px solid #e5e7eb;">
      <div style="color: #6b7280; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Before</div>
      <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0; color: #1f2937;">2 hours</div>
      <div style="color: #6b7280; font-size: 0.9rem;">to find bad data</div>
    </div>
    <div style="background: #f9fafb; padding: 1.25rem; border-radius: 10px; border: 1px solid #e5e7eb;">
      <div style="color: #6b7280; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">After</div>
      <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0; color: #1f2937;">30 sec</div>
      <div style="color: #6b7280; font-size: 0.9rem;">fail-fast validation</div>
    </div>
  </div>

  <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #e5e7eb;">
    <div style="color: #4b5563; font-size: 0.95rem;">💡 Save <strong>8 hours/month</strong> in debugging time</div>
  </div>

  <a href="/use-cases/#airflow-data-pipelines" style="display: inline-block; margin-top: 1.5rem; padding: 0.75rem 1.5rem; background: #1f2937; color: white; border-radius: 8px; text-decoration: none; font-weight: 600;">See How →</a>
</div>

<div style="background: #ffffff; padding: 2.5rem; border-radius: 16px; border: 2px solid #e5e7eb; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">
  <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
    <div style="font-size: 3rem;">🤖</div>
    <h3 style="margin: 0; color: #1f2937; font-size: 1.5rem;">ML Training</h3>
  </div>

  <p style="font-size: 1.05rem; color: #4b5563; margin-bottom: 1.5rem; line-height: 1.6;">Don't waste expensive GPU time on bad training data. Validate before you train.</p>

  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1.5rem 0;">
    <div style="background: #f9fafb; padding: 1.25rem; border-radius: 10px; border: 1px solid #e5e7eb;">
      <div style="color: #6b7280; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Wasted</div>
      <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0; color: #1f2937;">$150</div>
      <div style="color: #6b7280; font-size: 0.9rem;">per month on bad runs</div>
    </div>
    <div style="background: #f9fafb; padding: 1.25rem; border-radius: 10px; border: 1px solid #e5e7eb;">
      <div style="color: #6b7280; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">With DataCheck</div>
      <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0; color: #1f2937;">$0</div>
      <div style="color: #6b7280; font-size: 0.9rem;">validate first</div>
    </div>
  </div>

  <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #e5e7eb;">
    <div style="color: #4b5563; font-size: 0.95rem;">💡 Prevent <strong>2 hours</strong> of wasted GPU time per incident</div>
  </div>

  <a href="/use-cases/#ml-training-pipelines" style="display: inline-block; margin-top: 1.5rem; padding: 0.75rem 1.5rem; background: #1f2937; color: white; border-radius: 8px; text-decoration: none; font-weight: 600;">See How →</a>
</div>

<div style="background: #ffffff; padding: 2.5rem; border-radius: 16px; border: 2px solid #e5e7eb; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">
  <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
    <div style="font-size: 3rem;">🤝</div>
    <h3 style="margin: 0; color: #1f2937; font-size: 1.5rem;">Data Contracts</h3>
  </div>

  <p style="font-size: 1.05rem; color: #4b5563; margin-bottom: 1.5rem; line-height: 1.6;">Turn validation configs into living contracts between teams. Prevent breaking changes before production.</p>

  <div style="background: #f9fafb; padding: 1.25rem; border-radius: 10px; border: 1px solid #e5e7eb; margin: 1.5rem 0;">
    <div style="color: #4b5563; font-size: 0.95rem; line-height: 1.6;">
      Both producer and consumer teams validate against the same contract. Breaking changes caught in CI/CD, not production.
    </div>
  </div>

  <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #e5e7eb;">
    <div style="color: #4b5563; font-size: 0.95rem;">💡 Prevent production incidents • Clear ownership • Living docs</div>
  </div>

  <a href="/use-cases/#data-contracts-between-teams" style="display: inline-block; margin-top: 1.5rem; padding: 0.75rem 1.5rem; background: #1f2937; color: white; border-radius: 8px; text-decoration: none; font-weight: 600;">See How →</a>
</div>

</div>

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
