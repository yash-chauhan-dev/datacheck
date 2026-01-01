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

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; color: white; margin: 2rem 0;">
  <h3 style="margin-top: 0; color: white;">🏭 Airflow Data Pipelines</h3>
  <p style="font-size: 1.1rem; opacity: 0.95;">Validate data before expensive transformations</p>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
      <div style="opacity: 0.8; font-size: 0.9rem;">Before</div>
      <div style="font-size: 1.3rem; font-weight: bold;">2 hours</div>
      <div style="opacity: 0.8; font-size: 0.85rem;">to discover bad data</div>
    </div>
    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
      <div style="opacity: 0.8; font-size: 0.9rem;">After</div>
      <div style="font-size: 1.3rem; font-weight: bold;">30 seconds</div>
      <div style="opacity: 0.8; font-size: 0.85rem;">fail-fast validation</div>
    </div>
  </div>
  <a href="/datacheck/use-cases/#airflow-data-pipelines" style="display: inline-block; margin-top: 1rem; padding: 0.5rem 1rem; background: white; color: #667eea; border-radius: 6px; text-decoration: none; font-weight: 500;">Learn More →</a>
</div>

<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; border-radius: 12px; color: white; margin: 2rem 0;">
  <h3 style="margin-top: 0; color: white;">🤖 ML Training Pipelines</h3>
  <p style="font-size: 1.1rem; opacity: 0.95;">Validate training data before expensive GPU jobs</p>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
      <div style="opacity: 0.8; font-size: 0.9rem;">Wasted GPU costs</div>
      <div style="font-size: 1.3rem; font-weight: bold;">$150/month</div>
      <div style="opacity: 0.8; font-size: 0.85rem;">on bad training runs</div>
    </div>
    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
      <div style="opacity: 0.8; font-size: 0.9rem;">With DataCheck</div>
      <div style="font-size: 1.3rem; font-weight: bold;">$0</div>
      <div style="opacity: 0.8; font-size: 0.85rem;">validate before training</div>
    </div>
  </div>
  <a href="/datacheck/use-cases/#ml-training-pipelines" style="display: inline-block; margin-top: 1rem; padding: 0.5rem 1rem; background: white; color: #f5576c; border-radius: 6px; text-decoration: none; font-weight: 500;">Learn More →</a>
</div>

<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 2rem; border-radius: 12px; color: white; margin: 2rem 0;">
  <h3 style="margin-top: 0; color: white;">🤝 Data Contracts</h3>
  <p style="font-size: 1.1rem; opacity: 0.95;">Turn validation configs into living contracts between teams</p>
  <div style="margin-top: 1rem; background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
    <div style="opacity: 0.9;">Prevent breaking changes before they reach production. Both producer and consumer teams validate against the same contract.</div>
  </div>
  <a href="/datacheck/use-cases/#data-contracts-between-teams" style="display: inline-block; margin-top: 1rem; padding: 0.5rem 1rem; background: white; color: #00f2fe; border-radius: 6px; text-decoration: none; font-weight: 500;">Learn More →</a>
</div>

## What You Can Validate

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin: 2rem 0;">

<div style="text-align: center; padding: 1.5rem; border: 2px solid #e5e7eb; border-radius: 12px;">
  <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📄</div>
  <div style="font-weight: 600; margin-bottom: 0.5rem;">CSV Files</div>
  <div style="color: #6b7280; font-size: 0.9rem;">UTF-8, automatic encoding detection</div>
</div>

<div style="text-align: center; padding: 1.5rem; border: 2px solid #e5e7eb; border-radius: 12px;">
  <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📦</div>
  <div style="font-weight: 600; margin-bottom: 0.5rem;">Parquet</div>
  <div style="color: #6b7280; font-size: 0.9rem;">Efficient columnar format</div>
</div>

<div style="text-align: center; padding: 1.5rem; border: 2px solid #e5e7eb; border-radius: 12px;">
  <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">💾</div>
  <div style="font-weight: 600; margin-bottom: 0.5rem;">SQLite</div>
  <div style="color: #6b7280; font-size: 0.9rem;">Direct table validation</div>
</div>

<div style="text-align: center; padding: 1.5rem; border: 2px solid #e5e7eb; border-radius: 12px;">
  <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🦆</div>
  <div style="font-weight: 600; margin-bottom: 0.5rem;">DuckDB</div>
  <div style="color: #6b7280; font-size: 0.9rem;">Analytics database (Linux/macOS)</div>
</div>

</div>

## Available Validation Rules

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin: 2rem 0;">

<div style="padding: 1rem; background: #f9fafb; border-left: 4px solid #3b82f6; border-radius: 4px;">
  <div style="font-weight: 600; color: #3b82f6; margin-bottom: 0.5rem;">not_null</div>
  <div style="font-size: 0.9rem; color: #6b7280;">Ensure no missing values</div>
</div>

<div style="padding: 1rem; background: #f9fafb; border-left: 4px solid #10b981; border-radius: 4px;">
  <div style="font-weight: 600; color: #10b981; margin-bottom: 0.5rem;">unique</div>
  <div style="font-size: 0.9rem; color: #6b7280;">Detect duplicate values</div>
</div>

<div style="padding: 1rem; background: #f9fafb; border-left: 4px solid #f59e0b; border-radius: 4px;">
  <div style="font-weight: 600; color: #f59e0b; margin-bottom: 0.5rem;">min / max</div>
  <div style="font-size: 0.9rem; color: #6b7280;">Numeric range validation</div>
</div>

<div style="padding: 1rem; background: #f9fafb; border-left: 4px solid #8b5cf6; border-radius: 4px;">
  <div style="font-weight: 600; color: #8b5cf6; margin-bottom: 0.5rem;">regex</div>
  <div style="font-size: 0.9rem; color: #6b7280;">Pattern matching for strings</div>
</div>

<div style="padding: 1rem; background: #f9fafb; border-left: 4px solid #ec4899; border-radius: 4px;">
  <div style="font-weight: 600; color: #ec4899; margin-bottom: 0.5rem;">allowed_values</div>
  <div style="font-size: 0.9rem; color: #6b7280;">Whitelist validation</div>
</div>

</div>

## Trusted by Data Teams

<div style="text-align: center; padding: 3rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; color: white; margin: 3rem 0;">
  <div style="font-size: 1.3rem; margin-bottom: 1rem; opacity: 0.95;">Join teams improving their data quality</div>
  <div style="font-size: 2.5rem; font-weight: bold; margin-bottom: 2rem;">Start validating in 2 minutes</div>
  <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
    <a href="/datacheck/guide/getting-started" style="display: inline-block; padding: 1rem 2rem; background: white; color: #667eea; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1.1rem;">Get Started →</a>
    <a href="/datacheck/use-cases/" style="display: inline-block; padding: 1rem 2rem; background: rgba(255,255,255,0.2); color: white; border: 2px solid white; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1.1rem;">See Use Cases →</a>
  </div>
</div>
