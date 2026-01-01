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
    src: /datacheck/hero.svg
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

<div style="padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white;">
  <div style="font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem;">10x</div>
  <div style="font-size: 1.1rem; opacity: 0.95;">Less code than custom validation</div>
  <div style="margin-top: 1rem; opacity: 0.8; font-size: 0.9rem;">Replace 100+ lines of Python with 10 lines of YAML</div>
</div>

<div style="padding: 1.5rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 12px; color: white;">
  <div style="font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem;">6x</div>
  <div style="font-size: 1.1rem; opacity: 0.95;">Faster to set up</div>
  <div style="margin-top: 1rem; opacity: 0.8; font-size: 0.9rem;">From 30 minutes to 5 minutes</div>
</div>

<div style="padding: 1.5rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 12px; color: white;">
  <div style="font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem;">8 hrs</div>
  <div style="font-size: 1.1rem; opacity: 0.95;">Saved per month</div>
  <div style="margin-top: 1rem; opacity: 0.8; font-size: 0.9rem;">Catch issues in 30 seconds vs 2 hours</div>
</div>

<div style="padding: 1.5rem; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); border-radius: 12px; color: white;">
  <div style="font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem;">$100</div>
  <div style="font-size: 1.1rem; opacity: 0.95;">Saved per month</div>
  <div style="margin-top: 1rem; opacity: 0.8; font-size: 0.9rem;">Prevent wasted GPU training costs</div>
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

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2.5rem; border-radius: 16px; color: white; box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);">
  <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
    <div style="font-size: 3rem;">🏭</div>
    <h3 style="margin: 0; color: white; font-size: 1.5rem;">Airflow Pipelines</h3>
  </div>

  <p style="font-size: 1.05rem; opacity: 0.95; margin-bottom: 1.5rem; line-height: 1.6;">Stop wasting hours on bad data. Validate before expensive transformations and catch issues instantly.</p>

  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1.5rem 0;">
    <div style="background: rgba(255,255,255,0.15); padding: 1.25rem; border-radius: 10px; backdrop-filter: blur(10px);">
      <div style="opacity: 0.85; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Before</div>
      <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">2 hours</div>
      <div style="opacity: 0.85; font-size: 0.9rem;">to find bad data</div>
    </div>
    <div style="background: rgba(255,255,255,0.15); padding: 1.25rem; border-radius: 10px; backdrop-filter: blur(10px);">
      <div style="opacity: 0.85; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">After</div>
      <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">30 sec</div>
      <div style="opacity: 0.85; font-size: 0.9rem;">fail-fast validation</div>
    </div>
  </div>

  <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.2);">
    <div style="opacity: 0.9; font-size: 0.95rem;">💡 Save <strong>8 hours/month</strong> in debugging time</div>
  </div>

  <a href="/datacheck/use-cases/#airflow-data-pipelines" style="display: inline-block; margin-top: 1.5rem; padding: 0.75rem 1.5rem; background: white; color: #667eea; border-radius: 8px; text-decoration: none; font-weight: 600; transition: transform 0.2s;">See How →</a>
</div>

<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2.5rem; border-radius: 16px; color: white; box-shadow: 0 10px 40px rgba(240, 147, 251, 0.3);">
  <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
    <div style="font-size: 3rem;">🤖</div>
    <h3 style="margin: 0; color: white; font-size: 1.5rem;">ML Training</h3>
  </div>

  <p style="font-size: 1.05rem; opacity: 0.95; margin-bottom: 1.5rem; line-height: 1.6;">Don't waste expensive GPU time on bad training data. Validate before you train.</p>

  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1.5rem 0;">
    <div style="background: rgba(255,255,255,0.15); padding: 1.25rem; border-radius: 10px; backdrop-filter: blur(10px);">
      <div style="opacity: 0.85; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Wasted</div>
      <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">$150</div>
      <div style="opacity: 0.85; font-size: 0.9rem;">per month on bad runs</div>
    </div>
    <div style="background: rgba(255,255,255,0.15); padding: 1.25rem; border-radius: 10px; backdrop-filter: blur(10px);">
      <div style="opacity: 0.85; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">With DataCheck</div>
      <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">$0</div>
      <div style="opacity: 0.85; font-size: 0.9rem;">validate first</div>
    </div>
  </div>

  <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.2);">
    <div style="opacity: 0.9; font-size: 0.95rem;">💡 Prevent <strong>2 hours</strong> of wasted GPU time per incident</div>
  </div>

  <a href="/datacheck/use-cases/#ml-training-pipelines" style="display: inline-block; margin-top: 1.5rem; padding: 0.75rem 1.5rem; background: white; color: #f5576c; border-radius: 8px; text-decoration: none; font-weight: 600; transition: transform 0.2s;">See How →</a>
</div>

<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 2.5rem; border-radius: 16px; color: white; box-shadow: 0 10px 40px rgba(79, 172, 254, 0.3);">
  <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
    <div style="font-size: 3rem;">🤝</div>
    <h3 style="margin: 0; color: white; font-size: 1.5rem;">Data Contracts</h3>
  </div>

  <p style="font-size: 1.05rem; opacity: 0.95; margin-bottom: 1.5rem; line-height: 1.6;">Turn validation configs into living contracts between teams. Prevent breaking changes before production.</p>

  <div style="background: rgba(255,255,255,0.15); padding: 1.25rem; border-radius: 10px; backdrop-filter: blur(10px); margin: 1.5rem 0;">
    <div style="opacity: 0.9; font-size: 0.95rem; line-height: 1.6;">
      Both producer and consumer teams validate against the same contract. Breaking changes caught in CI/CD, not production.
    </div>
  </div>

  <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.2);">
    <div style="opacity: 0.9; font-size: 0.95rem;">💡 Prevent production incidents • Clear ownership • Living docs</div>
  </div>

  <a href="/datacheck/use-cases/#data-contracts-between-teams" style="display: inline-block; margin-top: 1.5rem; padding: 0.75rem 1.5rem; background: white; color: #00f2fe; border-radius: 8px; text-decoration: none; font-weight: 600; transition: transform 0.2s;">See How →</a>
</div>

</div>

## Validate Any Data Format

DataCheck works with all your data sources - from simple CSV files to analytical databases.

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; margin: 3rem 0;">

<div style="background: linear-gradient(to bottom right, #ffffff, #f8fafc); padding: 2rem; border-radius: 12px; border: 2px solid #e2e8f0; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
  <div style="font-size: 3rem; margin-bottom: 1rem;">📄</div>
  <h3 style="color: #1e293b; margin-bottom: 0.75rem; font-size: 1.3rem;">CSV Files</h3>
  <p style="color: #64748b; margin-bottom: 1rem; line-height: 1.6;">Perfect for spreadsheets and exports. Automatic UTF-8 encoding detection, handles BOM, works with any delimiter.</p>
  <div style="background: #f1f5f9; padding: 0.75rem; border-radius: 6px; font-family: monospace; font-size: 0.85rem; color: #475569;">
    datacheck validate users.csv
  </div>
</div>

<div style="background: linear-gradient(to bottom right, #ffffff, #fef3c7); padding: 2rem; border-radius: 12px; border: 2px solid #fbbf24; box-shadow: 0 4px 20px rgba(251,191,36,0.1);">
  <div style="font-size: 3rem; margin-bottom: 1rem;">📦</div>
  <h3 style="color: #78350f; margin-bottom: 0.75rem; font-size: 1.3rem;">Parquet Files</h3>
  <p style="color: #92400e; margin-bottom: 1rem; line-height: 1.6;">High performance for big data. Columnar format, compressed, type-safe. Perfect for ML pipelines and analytics.</p>
  <div style="background: #fef3c7; padding: 0.75rem; border-radius: 6px; font-family: monospace; font-size: 0.85rem; color: #78350f;">
    datacheck validate data.parquet
  </div>
</div>

<div style="background: linear-gradient(to bottom right, #ffffff, #dbeafe); padding: 2rem; border-radius: 12px; border: 2px solid #3b82f6; box-shadow: 0 4px 20px rgba(59,130,246,0.1);">
  <div style="font-size: 3rem; margin-bottom: 1rem;">💾</div>
  <h3 style="color: #1e3a8a; margin-bottom: 0.75rem; font-size: 1.3rem;">SQLite Database</h3>
  <p style="color: #1e40af; margin-bottom: 1rem; line-height: 1.6;">Validate tables directly from SQLite databases. No export needed, works with production databases.</p>
  <div style="background: #dbeafe; padding: 0.75rem; border-radius: 6px; font-family: monospace; font-size: 0.85rem; color: #1e3a8a;">
    datacheck validate app.db::users
  </div>
</div>

<div style="background: linear-gradient(to bottom right, #ffffff, #fce7f3); padding: 2rem; border-radius: 12px; border: 2px solid #ec4899; box-shadow: 0 4px 20px rgba(236,72,153,0.1);">
  <div style="font-size: 3rem; margin-bottom: 1rem;">🦆</div>
  <h3 style="color: #831843; margin-bottom: 0.75rem; font-size: 1.3rem;">DuckDB Database</h3>
  <p style="color: #9f1239; margin-bottom: 1rem; line-height: 1.6;">Analytical database for large datasets. Fast queries, handles 100GB+ files. Linux/macOS only.</p>
  <div style="background: #fce7f3; padding: 0.75rem; border-radius: 6px; font-family: monospace; font-size: 0.85rem; color: #831843;">
    datacheck validate data.duckdb::events
  </div>
</div>

</div>
