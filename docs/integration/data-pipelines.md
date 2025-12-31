# Data Pipeline Integration

Integrate DataCheck into your data pipelines.

---

## Apache Airflow

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

dag = DAG('data_quality', start_date=datetime(2024, 1, 1))

validate = BashOperator(
    task_id='validate',
    bash_command='datacheck validate /data/export.csv --config /config/rules.yaml',
    dag=dag
)

load = BashOperator(
    task_id='load',
    bash_command='python load_to_warehouse.py',
    dag=dag
)

validate >> load  # Load only if validation passes
```

---

## Prefect

```python
from prefect import flow, task

@task
def validate_data(file_path: str, config_path: str):
    import subprocess
    result = subprocess.run(
        ["datacheck", "validate", file_path, "--config", config_path],
        capture_output=True
    )
    if result.returncode != 0:
        raise Exception("Data validation failed")
    return True

@task
def load_to_warehouse(file_path: str):
    # Load data
    pass

@flow
def data_pipeline():
    validate_data("data.csv", "validation.yaml")
    load_to_warehouse("data.csv")
```

---

## dbt

Add as a pre-hook in dbt:

```sql
{{ config(
    pre_hook="!datacheck validate {{ source('raw', 'customers') }} --config validation/customers.yaml"
) }}

SELECT * FROM {{ source('raw', 'customers') }}
```

---

## Luigi

```python
import luigi

class ValidateData(luigi.Task):
    def run(self):
        import subprocess
        result = subprocess.run([
            "datacheck", "validate",
            "data.csv", "--config", "validation.yaml"
        ])
        if result.returncode != 0:
            raise Exception("Validation failed")

class LoadData(luigi.Task):
    def requires(self):
        return ValidateData()
    
    def run(self):
        # Load data
        pass
```

---

See [CI/CD Integration](cicd.md) for more examples.
