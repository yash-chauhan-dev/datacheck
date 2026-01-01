# Real-World Use Cases

See how teams are using DataCheck to improve data quality and save time.

---

## 🏭 Airflow Data Pipelines

### The Problem

Your Airflow pipeline runs for 2 hours transforming data, only to fail at the end because of bad input data. You've wasted compute resources and delayed your data consumers.

**Common scenario:**
```
08:00 AM - Pipeline starts
08:00 AM - Extract raw data (5 min)
08:05 AM - Transform data (2 hours)
10:05 AM - Load fails - null values in required field!
10:05 AM - Debug and fix (1 hour)
11:05 AM - Re-run entire pipeline (2 hours)
01:05 PM - Finally complete (5 hours total)
```

### The Solution

Add DataCheck validation **before** expensive transformations.

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG('data_pipeline', start_date=datetime(2025, 1, 1)) as dag:

    # Extract raw data
    extract = BashOperator(
        task_id='extract',
        bash_command='python scripts/extract_data.py'
    )

    # Validate BEFORE transformation (30 seconds)
    validate = BashOperator(
        task_id='validate',
        bash_command='datacheck validate /data/raw.csv --config /config/validation.yaml'
    )

    # Only run expensive transformation if data is valid
    transform = BashOperator(
        task_id='transform',
        bash_command='python scripts/transform_data.py'  # 2 hours
    )

    # Load transformed data
    load = BashOperator(
        task_id='load',
        bash_command='python scripts/load_data.py'
    )

    # Pipeline flow: fail fast if data is bad
    extract >> validate >> transform >> load
```

**Validation config** (`/config/validation.yaml`):
```yaml
checks:
  - name: required_fields
    column: user_id
    rules:
      not_null: true
      unique: true

  - name: email_format
    column: email
    rules:
      not_null: true
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"

  - name: data_freshness
    column: created_at
    rules:
      not_null: true
```

### The Impact

**Before DataCheck:**
- ❌ Issues discovered after 2-hour transformation
- ❌ 5 hours total time to fix and re-run
- ❌ Wasted compute resources
- ❌ Delayed data delivery

**After DataCheck:**
- ✅ Issues caught in 30 seconds
- ✅ Fix data at source
- ✅ Re-run only validation (30 seconds)
- ✅ Transformation only runs on valid data

**ROI:** Save 8 hours/month in debugging and re-running pipelines.

---

## 🤖 ML Training Pipelines

### The Problem

You start training a machine learning model on GPU instances. After 2 hours and $50 in compute costs, training fails because of data quality issues.

**Pain points:**
- Missing values in critical features
- Labels outside expected range
- Data drift not caught before training
- Expensive GPU time wasted

### The Solution

Validate training data **before** starting expensive GPU jobs.

```python
import subprocess
import sys

def validate_training_data():
    """Validate training data before expensive GPU training"""
    result = subprocess.run([
        'datacheck',
        'validate',
        'data/training_data.parquet',
        '--config', 'validation/ml_training.yaml',
        '--output', 'json'
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ Training data validation failed!")
        print(result.stdout)
        return False

    print("✅ Training data validated successfully")
    return True

def train_model():
    """Train ML model with data validation"""

    # Step 1: Validate data (30 seconds)
    if not validate_training_data():
        print("Fix data quality issues before training")
        sys.exit(1)

    # Step 2: Only train if data is valid (2 hours on GPU)
    print("Starting model training on GPU...")
    # model.fit(training_data)
    # ... training code ...

if __name__ == "__main__":
    train_model()
```

**Training data validation** (`validation/ml_training.yaml`):
```yaml
checks:
  # Feature completeness
  - name: features_not_null
    column: features
    rules:
      not_null: true

  # Label validation
  - name: label_range
    column: label
    rules:
      not_null: true
      min: 0
      max: 1

  # Data freshness
  - name: timestamp_check
    column: timestamp
    rules:
      not_null: true

  # Feature ID uniqueness
  - name: sample_id_unique
    column: sample_id
    rules:
      not_null: true
      unique: true
```

### The Impact

**Before DataCheck:**
- ❌ Start training → discover bad data 2 hours later
- ❌ $25/hour × 2 hours = $50 wasted per failure
- ❌ 3-4 failures per month = $150-200/month wasted
- ❌ Delayed model deployment

**After DataCheck:**
- ✅ Validate in 30 seconds
- ✅ Fix data before training starts
- ✅ No wasted GPU time
- ✅ Faster model iteration

**ROI:** Save $50-100/month in GPU costs. Prevent 2 hours of wasted compute per incident.

---

## 🤝 Data Contracts Between Teams

### The Problem

Your data engineering team produces data for downstream consumers. A schema change breaks production pipelines, causing:
- Production incidents
- Angry downstream teams
- Emergency fixes
- Lost trust

**Classic scenario:**
```
Data Producer Team changes schema:
- Removes 'user_type' column
- Adds new 'account_tier' column
- Doesn't notify consumers

Consumer Team's pipeline:
- Breaks in production
- Missing 'user_type' column error
- 2 AM incident
- Rollback required
```

### The Solution

Turn validation configs into **data contracts** - the single source of truth that both teams test against.

**The Contract** (`contracts/user_events.yaml`):
```yaml
# This is THE contract between producer and consumer teams
# Both teams MUST pass validation against this file

checks:
  # User identification
  - name: user_id_contract
    column: user_id
    rules:
      not_null: true
      unique: true
      min: 1000

  # Event type enum
  - name: event_type_contract
    column: event_type
    rules:
      not_null: true
      allowed_values: ["click", "view", "purchase", "signup", "logout"]

  # Timestamp requirement
  - name: timestamp_contract
    column: timestamp
    rules:
      not_null: true

  # User type (REQUIRED field)
  - name: user_type_contract
    column: user_type
    rules:
      not_null: true
      allowed_values: ["free", "premium", "enterprise"]

  # Session tracking
  - name: session_id_contract
    column: session_id
    rules:
      not_null: true
```

**Producer Team CI/CD** (`.github/workflows/producer-ci.yml`):
```yaml
name: Producer CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install DataCheck
        run: pip install datacheck-cli

      - name: Generate sample output
        run: python scripts/generate_events.py

      # Validate against contract BEFORE merging
      - name: Validate data contract
        run: |
          datacheck validate output/user_events.parquet \
            --config contracts/user_events.yaml

          if [ $? -ne 0 ]; then
            echo "❌ Breaking contract! Cannot merge."
            exit 1
          fi
```

**Consumer Team CI/CD** (`.github/workflows/consumer-ci.yml`):
```yaml
name: Consumer CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install DataCheck
        run: pip install datacheck-cli

      # Test with sample data from producer
      - name: Download sample data
        run: aws s3 cp s3://shared/user_events_sample.parquet data/

      # Validate consumer still works with contract
      - name: Validate contract compatibility
        run: |
          datacheck validate data/user_events_sample.parquet \
            --config contracts/user_events.yaml
```

### The Impact

**Before Data Contracts:**
- ❌ Producer changes schema → breaks consumer in production
- ❌ No early warning
- ❌ Production incidents
- ❌ Manual coordination required

**After Data Contracts:**
- ✅ Producer CI fails if breaking contract
- ✅ Consumer CI fails if expecting different schema
- ✅ Issues caught in PR review
- ✅ Contract is living documentation

**ROI:**
- Prevent production incidents
- Clear ownership and expectations
- Self-documenting data contracts
- Trust between teams

---

## 🚦 CI/CD Quality Gates

### The Problem

You have 100+ lines of custom Python code for data validation. It's:
- Hard to maintain
- Requires Python knowledge to modify
- Difficult for non-engineers to contribute
- Tightly coupled to your codebase

**Example custom validation** (`validate.py` - 100+ lines):
```python
import pandas as pd
import sys
import re

def validate_data(file_path):
    """Custom validation logic"""
    df = pd.read_csv(file_path)
    errors = []

    # Email validation
    if df['email'].isnull().any():
        errors.append('Email column has null values')

    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    invalid_emails = df[~df['email'].str.match(email_pattern, na=False)]
    if len(invalid_emails) > 0:
        errors.append(f'Invalid email format: {len(invalid_emails)} rows')

    # Age validation
    if (df['age'] < 18).any():
        errors.append('Age below minimum (18)')
    if (df['age'] > 120).any():
        errors.append('Age above maximum (120)')
    if df['age'].isnull().any():
        errors.append('Age has null values')

    # Status validation
    valid_statuses = ['active', 'inactive', 'pending']
    invalid_status = df[~df['status'].isin(valid_statuses)]
    if len(invalid_status) > 0:
        errors.append(f'Invalid status values: {len(invalid_status)} rows')

    # Price validation
    if df['price'].isnull().any():
        errors.append('Price has null values')
    if (df['price'] < 0).any():
        errors.append('Negative prices found')
    if (df['price'] > 1000000).any():
        errors.append('Price exceeds maximum')

    # ... 60 more lines ...

    if errors:
        print("❌ Validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("✅ All validations passed")

if __name__ == "__main__":
    validate_data('data.csv')
```

### The Solution

Replace with simple, declarative YAML that anyone can understand and modify.

**New validation** (`validation.yaml` - 25 lines):
```yaml
checks:
  # Email validation
  - name: email_validation
    column: email
    rules:
      not_null: true
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"

  # Age validation
  - name: age_validation
    column: age
    rules:
      not_null: true
      min: 18
      max: 120

  # Status validation
  - name: status_validation
    column: status
    rules:
      not_null: true
      allowed_values: ["active", "inactive", "pending"]

  # Price validation
  - name: price_validation
    column: price
    rules:
      not_null: true
      min: 0
      max: 1000000
```

**GitHub Actions** (`.github/workflows/data-quality.yml`):
```yaml
name: Data Quality Check

on:
  pull_request:
    paths:
      - 'data/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install DataCheck
        run: pip install datacheck-cli

      - name: Validate data quality
        run: datacheck validate data/users.csv --config validation.yaml
```

### The Impact

**Before DataCheck:**
- ❌ 100+ lines of Python code
- ❌ Requires Python expertise to modify
- ❌ Hard to maintain
- ❌ Tightly coupled to codebase

**After DataCheck:**
- ✅ 25 lines of simple YAML
- ✅ Anyone can understand and modify
- ✅ Easy to maintain
- ✅ Decoupled from codebase

**ROI:**
- **6x faster** to set up (30 min → 5 min)
- **75% less code** (100+ lines → 25 lines)
- **Lower barrier** - product managers can contribute
- **Faster iterations** - no code reviews for rule changes

---

## 📊 Daily Data Quality Monitoring

### The Problem

You need to monitor production data quality continuously, but:
- Manual checks are time-consuming
- Issues discovered too late
- No early warning system
- Reactive instead of proactive

### The Solution

Schedule DataCheck to run on production data exports and alert on failures.

**GitHub Actions** (`.github/workflows/daily-monitoring.yml`):
```yaml
name: Daily Data Quality Monitoring

on:
  schedule:
    # Run every day at 1 AM UTC
    - cron: '0 1 * * *'
  workflow_dispatch:  # Allow manual trigger

jobs:
  monitor-production:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install DataCheck
        run: pip install datacheck-cli

      - name: Download production data export
        run: |
          # Download yesterday's data export
          aws s3 cp s3://prod-exports/users/latest.csv users.csv

      - name: Validate production data quality
        id: validation
        run: |
          datacheck validate users.csv \
            --config validation/production-users.yaml \
            --output json > validation-results.json

          echo "exit_code=$?" >> $GITHUB_OUTPUT

      - name: Parse validation results
        if: always()
        run: |
          FAILED=$(jq '.summary.failed' validation-results.json)
          TOTAL=$(jq '.summary.total_checks' validation-results.json)

          echo "failed_checks=$FAILED" >> $GITHUB_ENV
          echo "total_checks=$TOTAL" >> $GITHUB_ENV

      - name: Send Slack alert on failure
        if: steps.validation.outputs.exit_code != '0'
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
               -H 'Content-Type: application/json' \
               -d "{
                 \"text\": \"❌ Production data quality alert!\",
                 \"blocks\": [
                   {
                     \"type\": \"section\",
                     \"text\": {
                       \"type\": \"mrkdwn\",
                       \"text\": \"*Production Data Quality Alert*\\n${{ env.failed_checks }} out of ${{ env.total_checks }} checks failed.\"
                     }
                   },
                   {
                     \"type\": \"section\",
                     \"text\": {
                       \"type\": \"mrkdwn\",
                       \"text\": \"<https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}|View Details>\"
                     }
                   }
                 ]
               }"

      - name: Create GitHub issue on failure
        if: steps.validation.outputs.exit_code != '0'
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '⚠️ Production Data Quality Alert',
              body: `Production data validation failed.\n\n**Failed Checks:** ${{ env.failed_checks }}/${{ env.total_checks }}\n\n[View Run](https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }})`,
              labels: ['data-quality', 'production', 'alert']
            });

      - name: Upload validation results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: validation-results
          path: validation-results.json
```

**Production validation config** (`validation/production-users.yaml`):
```yaml
checks:
  - name: user_id_integrity
    column: user_id
    rules:
      not_null: true
      unique: true

  - name: email_quality
    column: email
    rules:
      not_null: true
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"

  - name: account_status
    column: status
    rules:
      not_null: true
      allowed_values: ["active", "inactive", "suspended"]

  - name: created_date
    column: created_at
    rules:
      not_null: true
```

### The Impact

**Before Monitoring:**
- ❌ Reactive - discover issues when users complain
- ❌ Manual spot checks (time-consuming)
- ❌ No trending or history
- ❌ Late detection

**After Monitoring:**
- ✅ Proactive - catch issues before users see them
- ✅ Automated daily checks
- ✅ Slack alerts for immediate action
- ✅ GitHub issues for tracking
- ✅ Historical trend data

**ROI:**
- Early warning system for data quality degradation
- Automated instead of manual checks
- Faster incident response
- Historical validation results for trend analysis

---

## Ready to Get Started?

Choose the use case that fits your needs:

- **[Airflow Pipelines](/examples/cicd)** - See full CI/CD integration examples
- **[ML Training](/guide/data-formats)** - Learn about Parquet validation for ML data
- **[Data Contracts](/guide/configuration)** - Set up validation configs as contracts
- **[Quality Gates](/guide/getting-started)** - Get started in 5 minutes
- **[Monitoring](/reference/exit-codes)** - Understand exit codes for automation
