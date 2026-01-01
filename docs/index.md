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

## Real-World Use Cases

### 🏭 Airflow Data Pipelines

**Problem:** You discover data issues after 2 hours of expensive transformation.

**Solution:** Validate in 30 seconds before transformation starts.

```python
from airflow import DAG
from airflow.operators.bash import BashOperator

# Fail fast: validate before expensive operations
validate = BashOperator(
    task_id='validate',
    bash_command='datacheck validate /data/raw.csv --config /rules/validation.yaml'
)

transform = BashOperator(
    task_id='transform',
    bash_command='python expensive_transform.py'  # 2 hours
)

validate >> transform  # Only transform if data is valid
```

**Impact:** Save 8 hours/month in debugging time. Catch issues in 30 seconds instead of 2 hours.

---

### 🤖 ML Training Pipelines

**Problem:** GPU training fails after 2 hours because of bad data.

**Solution:** Validate training data before starting GPU jobs.

```yaml
# training-data-validation.yaml
checks:
  - name: feature_completeness
    column: features
    rules:
      not_null: true

  - name: label_range
    column: label
    rules:
      min: 0
      max: 1

  - name: data_freshness
    column: timestamp
    rules:
      not_null: true
```

```python
def train_model():
    # Validate first (30 seconds)
    result = subprocess.run(['datacheck', 'validate', 'training_data.parquet'])
    if result.returncode != 0:
        print("❌ Training data validation failed!")
        return

    # Only train if data is valid (2 hours on GPU)
    model.fit(training_data)
```

**Impact:** Save $50-100/month in wasted GPU costs. Prevent 2 hours of wasted compute per bad data incident.

---

### 🤝 Data Contracts Between Teams

**Problem:** Producer team changes data schema, breaks consumer team's pipelines in production.

**Solution:** Validation configs become the contract. Both teams test against it.

```yaml
# contracts/user_events.yaml - THE source of truth
checks:
  - name: user_id_contract
    column: user_id
    rules:
      not_null: true
      unique: true
      min: 1000

  - name: event_type_contract
    column: event_type
    rules:
      not_null: true
      allowed_values: ["click", "view", "purchase", "signup"]

  - name: timestamp_contract
    column: timestamp
    rules:
      not_null: true
```

**Producer team CI/CD:**
```yaml
# Validate before deploying
- name: Validate contract
  run: datacheck validate output/user_events.parquet --config contracts/user_events.yaml
```

**Consumer team CI/CD:**
```yaml
# Test with sample data from producer
- name: Validate contract
  run: datacheck validate sample_data/user_events.parquet --config contracts/user_events.yaml
```

**Impact:** Prevent breaking changes. Living documentation that never gets outdated. Clear ownership and expectations.

---

### 🚦 CI/CD Quality Gates

**Problem:** 100+ lines of custom Python validation code that's hard to maintain.

**Solution:** Replace with 10 lines of YAML that anyone can understand.

**Before:**
```python
# validate.py - 100+ lines
import pandas as pd
import sys

df = pd.read_csv('data.csv')
errors = []

# Email validation
if df['email'].isnull().any():
    errors.append('Email has null values')
if not df['email'].str.match(r'^[\w\.-]+@[\w\.-]+\.\w+$').all():
    errors.append('Invalid email format')

# Age validation
if (df['age'] < 18).any() or (df['age'] > 120).any():
    errors.append('Age out of range')

# Status validation
valid_statuses = ['active', 'inactive', 'pending']
if not df['status'].isin(valid_statuses).all():
    errors.append('Invalid status values')

# ... 80 more lines ...

if errors:
    for error in errors:
        print(f"❌ {error}")
    sys.exit(1)
```

**After:**
```yaml
# validation.yaml - 10 lines
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
      allowed_values: ["active", "inactive", "pending"]
```

**GitHub Actions:**
```yaml
- name: Validate data quality
  run: datacheck validate data.csv --config validation.yaml
```

**Impact:**
- **6x faster** to set up (30 min → 5 min)
- **10x less code** (100+ lines → 10 lines)
- **Anyone can contribute** - no Python knowledge required
- **Easier to maintain** - just YAML, not code

---

### 📊 Daily Data Quality Monitoring

**Problem:** Need to monitor production data quality continuously.

**Solution:** Schedule DataCheck to run on production data exports.

```yaml
# .github/workflows/daily-quality-check.yml
name: Daily Data Quality Check

on:
  schedule:
    - cron: '0 0 * * *'  # Every day at midnight

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - name: Download production data export
        run: aws s3 cp s3://prod-data/daily/users.csv users.csv

      - name: Install DataCheck
        run: pip install datacheck-cli

      - name: Validate data quality
        run: datacheck validate users.csv --config validation/prod-users.yaml

      - name: Alert on failure
        if: failure()
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
               -H 'Content-Type: application/json' \
               -d '{"text":"❌ Production data quality check failed!"}'
```

**Impact:** Catch data quality degradation before it affects downstream systems. Early warning system for data issues.
