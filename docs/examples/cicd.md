# CI/CD Integration

Use DataCheck to validate data quality in your CI/CD pipelines.

## GitHub Actions

Add data validation as a required check before merging PRs.

**.github/workflows/data-validation.yml:**
```yaml
name: Data Quality Check

on:
  pull_request:
    paths:
      - 'data/**'
      - 'validation/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install DataCheck
        run: pip install datacheck-cli

      - name: Validate user data
        run: datacheck validate data/users.csv --config validation/users.yaml

      - name: Validate orders
        run: datacheck validate data/orders.csv --config validation/orders.yaml
```

**Result:** PR fails if data doesn't meet quality standards.

---

## GitLab CI

**.gitlab-ci.yml:**
```yaml
data-quality:
  stage: test
  image: python:3.12
  before_script:
    - pip install datacheck-cli
  script:
    - datacheck validate data/users.csv --config validation/users.yaml
    - datacheck validate data/orders.csv --config validation/orders.yaml
  only:
    changes:
      - data/**
      - validation/**
```

---

## Jenkins

**Jenkinsfile:**
```groovy
pipeline {
    agent any

    stages {
        stage('Data Validation') {
            steps {
                sh 'pip install datacheck-cli'
                sh 'datacheck validate data/users.csv --config validation/users.yaml'
                sh 'datacheck validate data/orders.csv --config validation/orders.yaml'
            }
        }
    }

    post {
        failure {
            mail to: 'team@company.com',
                 subject: "Data Quality Check Failed: ${env.JOB_NAME}",
                 body: "Data validation failed. Check ${env.BUILD_URL}"
        }
    }
}
```

---

## Airflow DAG

Validate data before expensive transformations.

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

dag = DAG(
    'data_pipeline',
    start_date=datetime(2025, 1, 1),
    schedule_interval='@daily'
)

# Extract data
extract = BashOperator(
    task_id='extract',
    bash_command='python extract_data.py',
    dag=dag
)

# Validate BEFORE transformation (fail fast!)
validate = BashOperator(
    task_id='validate',
    bash_command='datacheck validate /data/raw.csv --config /config/validation.yaml',
    dag=dag
)

# Only transform if validation passes
transform = BashOperator(
    task_id='transform',
    bash_command='python transform_data.py',
    dag=dag
)

# Load transformed data
load = BashOperator(
    task_id='load',
    bash_command='python load_data.py',
    dag=dag
)

extract >> validate >> transform >> load
```

**Impact:** Catch bad data in 30 seconds instead of after 2-hour transformation.

---

## Pre-commit Hook

Validate data before committing to git.

**.pre-commit-config.yaml:**
```yaml
repos:
  - repo: local
    hooks:
      - id: datacheck
        name: Validate data files
        entry: datacheck validate
        args: ['data/users.csv', '--config', 'validation/users.yaml']
        language: system
        pass_filenames: false
        files: \\.csv$
```

Install:
```bash
pip install pre-commit
pre-commit install
```

Now validation runs automatically before each commit!

---

## Docker Container

Create a Docker image for consistent validation:

**Dockerfile:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN pip install datacheck-cli

COPY validation/ /app/validation/

ENTRYPOINT ["datacheck", "validate"]
```

**Build:**
```bash
docker build -t datacheck-validator .
```

**Use:**
```bash
docker run -v $(pwd)/data:/data datacheck-validator /data/users.csv --config /app/validation/users.yaml
```

---

## Exit Code Handling

DataCheck returns different exit codes for automation:

```bash
#!/bin/bash

datacheck validate data.csv --config rules.yaml
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ All validations passed"
    # Continue pipeline
elif [ $EXIT_CODE -eq 1 ]; then
    echo "Validation failed"
    # Send alert
    curl -X POST https://alerts.company.com/webhook \
         -d '{"message": "Data validation failed"}'
    exit 1
elif [ $EXIT_CODE -eq 2 ]; then
    echo "Configuration error"
    exit 1
elif [ $EXIT_CODE -eq 3 ]; then
    echo "Data loading error"
    exit 1
else
    echo "Unknown error"
    exit 1
fi
```

**Exit Codes:**
- `0` - All validations passed
- `1` - Some validations failed
- `2` - Configuration error
- `3` - Data loading error

---

## Scheduled Validation

Run validation on a schedule to monitor data quality over time.

**GitHub Actions (daily):**
```yaml
name: Daily Data Quality Check

on:
  schedule:
    - cron: '0 0 * * *'  # Every day at midnight

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install DataCheck
        run: pip install datacheck-cli

      - name: Validate production data
        run: datacheck validate data/prod.csv --config validation/prod.yaml

      - name: Send notification
        if: failure()
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
               -H 'Content-Type: application/json' \
               -d '{"text":"Production data validation failed!"}'
```

**GitLab CI (hourly):**
```yaml
monitor-data-quality:
  stage: monitor
  script:
    - datacheck validate data/prod.csv --config validation/prod.yaml
  only:
    - schedules
```
