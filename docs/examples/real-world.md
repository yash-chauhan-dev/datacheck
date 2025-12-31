# Real-World Use Cases

See how DataCheck solves real data quality challenges across different scenarios.

---

## Use Case 1: CI/CD Data Quality Gate

### Scenario

E-commerce company receives daily sales CSV from partners. Data must be validated before loading to warehouse.

### Without DataCheck

Custom validation script (100+ lines of Python):

```python
# validate_sales.py
import pandas as pd
import smtplib

def validate_sales_data(file):
    df = pd.read_csv(file)
    
    errors = []
    
    # Price validation
    if df['price'].min() < 0:
        errors.append("Negative prices found")
    if df['price'].isna().any():
        errors.append("Missing prices")
    if df['price'].max() > 1000000:
        errors.append("Suspiciously high prices")
    
    # Quantity validation
    if df['quantity'].isna().any():
        errors.append("Missing quantities")
    if df['quantity'].min() < 0:
        errors.append("Negative quantities")
    
    # Product ID validation
    if df['product_id'].isna().any():
        errors.append("Missing product IDs")
    if not df['product_id'].str.match(r'^SKU[0-9]{6}$').all():
        errors.append("Invalid product ID format")
    
    # Order ID validation
    if df['order_id'].isna().any():
        errors.append("Missing order IDs")
    if df['order_id'].duplicated().any():
        errors.append("Duplicate order IDs")
    
    # Status validation
    valid_statuses = ['pending', 'shipped', 'delivered', 'cancelled']
    if not df['status'].isin(valid_statuses).all():
        errors.append("Invalid status values")
    
    # ... 20 more custom checks
    
    if errors:
        send_email_alert(errors)
        raise Exception(f"Validation failed: {errors}")
    
    return True

if __name__ == '__main__':
    validate_sales_data('sales.csv')
```

**Problems**:
- 100+ lines of boilerplate code
- Hard to maintain
- Inconsistent across teams
- No standardization
- Requires Python knowledge

### With DataCheck

Simple YAML configuration (10 lines):

```yaml
# sales_validation.yaml
checks:
  - name: price_validation
    column: price
    rules:
      not_null: true
      min: 0
      max: 1000000

  - name: quantity_validation
    column: quantity
    rules:
      not_null: true
      min: 1

  - name: product_id_validation
    column: product_id
    rules:
      not_null: true
      regex: "^SKU[0-9]{6}$"

  - name: order_id_validation
    column: order_id
    rules:
      not_null: true
      unique: true

  - name: status_validation
    column: status
    rules:
      not_null: true
      allowed_values: ["pending", "shipped", "delivered", "cancelled"]
```

**In CI/CD pipeline**:
```bash
# .github/workflows/validate-sales.yml
- name: Validate Sales Data
  run: datacheck validate sales.csv --config sales_validation.yaml || exit 1

- name: Load to Warehouse
  if: success()
  run: python load_to_warehouse.py
```

### Impact

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Setup time | 30 minutes | 5 minutes | **6x faster** |
| Lines of code | 100+ | 10 | **10x less code** |
| Maintenance | Hard | Easy (YAML) | **Much simpler** |
| Team adoption | Requires Python | Anyone can write YAML | **Lower barrier** |
| Consistency | Varies by team | Standardized | **Uniform** |

---

## Use Case 2: Airflow Data Pipeline

### Scenario

Data pipeline ingests from 10+ sources daily. Need to validate before expensive transformations.

### Implementation

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

with DAG(
    'daily_etl',
    schedule='@daily',
    start_date=days_ago(1),
    catchup=False
) as dag:
    
    # Extract data from multiple sources
    extract = BashOperator(
        task_id='extract',
        bash_command='python extract_data.py'
    )
    
    # Validate BEFORE transform (catch issues early)
    validate = BashOperator(
        task_id='validate',
        bash_command='''
            datacheck validate /data/raw/customers.csv --config rules/customers.yaml &&
            datacheck validate /data/raw/orders.csv --config rules/orders.yaml &&
            datacheck validate /data/raw/products.csv --config rules/products.yaml
        '''
    )
    
    # Transform only if validation passes
    transform = BashOperator(
        task_id='transform',
        bash_command='dbt run'
    )
    
    # Load to warehouse
    load = BashOperator(
        task_id='load',
        bash_command='python load_to_warehouse.py'
    )
    
    extract >> validate >> transform >> load
```

### Why This Works

**Fail Fast Principle**:
```
Without DataCheck:
Extract → Transform (2 hours) → Load → ❌ Bad data discovered
                                       ↳ 2 hours wasted

With DataCheck:
Extract → Validate (30 seconds) → ❌ Bad data caught
                                   ↳ 2 hours saved
```

### Impact

| Metric | Before | After |
|--------|--------|-------|
| **Failure detection** | After 2-hour transform | After 30-second validation |
| **Debug time** | 2-3 hours (data in warehouse) | 10 minutes (clear error messages) |
| **Cascade failures** | Breaks downstream pipelines | Stops before breaking anything |
| **Alert clarity** | "Transform failed" | "customers.csv: email column has 5 invalid formats" |

**Real cost savings**:
- **Before**: 1 data issue per week × 2 hours debugging = **8 hours/month**
- **After**: Catches issues in < 1 minute = **~8 hours saved/month**

---

## Use Case 3: ML Training Pipeline

### Scenario

ML model retraining with new data every week. Model training takes 2 hours on GPU.

### Problem

Training models with bad data leads to:
- 2 hours wasted on GPU compute
- Model performance degradation
- Late detection of data quality issues
- Expensive debugging

### Solution

```python
# train.py
import subprocess
import sys

def validate_training_data():
    """Validate before expensive model training"""
    print("🔍 Validating training data...")
    
    result = subprocess.run([
        'datacheck', 'validate',
        'data/train.parquet',
        '--config', 'ml_validation.yaml',
        '--format', 'json',
        '--json-output', 'validation_results.json'
    ])
    
    if result.returncode != 0:
        print("❌ Training data failed validation!")
        print("Check validation_results.json for details")
        sys.exit(1)
    
    print("✅ Training data validated successfully")

def train_model():
    """Train ML model (expensive operation)"""
    validate_training_data()  # Fast check first!
    
    print("🚀 Starting model training (2 hours)...")
    # ... actual training code
    # ... uses expensive GPU resources

if __name__ == '__main__':
    train_model()
```

**Validation rules for ML data**:

```yaml
# ml_validation.yaml
checks:
  # Features must not have nulls
  - name: feature_completeness
    column: feature_1
    rules:
      not_null: true

  - name: feature_2_completeness
    column: feature_2
    rules:
      not_null: true

  # Target variable validation
  - name: label_validation
    column: label
    rules:
      not_null: true
      allowed_values: [0, 1]  # Binary classification

  # Feature range validation (catch data drift)
  - name: feature_range
    column: feature_1
    rules:
      min: 0
      max: 100

  # Ensure sufficient data
  - name: user_id_check
    column: user_id
    rules:
      unique: true  # Detect duplicates
```

### Impact

| Scenario | Without Validation | With DataCheck |
|----------|-------------------|----------------|
| **Good data** | Train 2 hours ✅ | Validate 30s + Train 2 hours ✅ |
| **Bad data** | Train 2 hours ❌ | Validate 30s ❌ (stop here) |
| **Cost savings** | - | **2 hours GPU time saved per failure** |

**Real-world results**:
- Validation time: **30 seconds**
- Training time: **2 hours**
- Failures prevented: **~2 per month**
- GPU hours saved: **~4 hours/month**
- Cost savings: **~$50-100/month** (depending on GPU pricing)

---

## Use Case 4: Data Contract Enforcement

### Scenario

Multiple teams (analytics, ML, product) depend on shared `users` table. Need to enforce data contracts.

### The Problem

**Without contracts**:
- Producer team changes schema → Breaks consumer pipelines
- No visibility into what changed
- Consumers discover issues in production
- Finger-pointing and blame

### The Solution: Data Contracts as Code

```yaml
# data_contracts/users_table.yaml
# This IS the contract between teams

version: "1.0"

# Contract metadata
contract:
  owner: data-engineering-team
  consumers:
    - analytics-team
    - ml-team
    - product-team
  sla: daily

checks:
  # Primary key contract
  - name: user_id_contract
    column: user_id
    rules:
      not_null: true
      unique: true

  # Email contract
  - name: email_contract
    column: email
    rules:
      not_null: true
      regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

  # Signup date contract
  - name: signup_date_contract
    column: signup_date
    rules:
      not_null: true

  # Country code contract
  - name: country_contract
    column: country_code
    rules:
      not_null: true
      allowed_values: ["US", "UK", "CA", "AU", "DE", "FR", "JP", "IN"]

  # Account status contract
  - name: status_contract
    column: account_status
    rules:
      not_null: true
      allowed_values: ["active", "inactive", "suspended", "deleted"]
```

### Producer Team Usage

```bash
# In ETL pipeline (before loading to warehouse)
echo "Validating users data against contract..."
datacheck validate users_export.csv \
  --config data_contracts/users_table.yaml

if [ $? -eq 0 ]; then
  echo "✅ Contract satisfied - loading to warehouse"
  load_to_warehouse users_export.csv users_table
else
  echo "❌ Contract violated - blocking load"
  notify_team "Users data contract violation"
  exit 1
fi
```

### Consumer Team Usage

```bash
# Consumers can verify data meets their expectations
echo "Verifying users table meets our contract..."
export_from_warehouse users_table > warehouse_users.csv

datacheck validate warehouse_users.csv \
  --config data_contracts/users_table.yaml

if [ $? -ne 0 ]; then
  echo "⚠️ Data doesn't meet contract - pausing pipeline"
  exit 1
fi
```

### Workflow

```
Producer Team                     Consumer Teams
     │                                 │
     │ 1. Generate users data          │
     ├─────────────────────────────────┤
     │                                 │
     │ 2. Validate against contract    │
     │    datacheck validate           │
     │         ↓                        │
     │    ✅ Pass                       │
     │         ↓                        │
     │ 3. Load to warehouse             │
     ├─────────────────────────────────┤
     │                                 │
     │                            4. Read from warehouse
     │                                 │
     │                            5. Validate against contract
     │                                 datacheck validate
     │                                      ↓
     │                                 ✅ Pass
     │                                      ↓
     │                            6. Use in pipeline
```

### Impact

| Aspect | Before (No Contract) | After (DataCheck Contracts) |
|--------|---------------------|----------------------------|
| **Schema changes** | Break consumers silently | Caught immediately |
| **Discovery** | Production failures | Pre-production validation |
| **Documentation** | Wiki (outdated) | Living code (always current) |
| **Ownership** | Unclear | Clear (in contract file) |
| **Trust** | Low | High |
| **Debugging time** | Hours | Minutes |

**Real-world benefits**:
- ✅ **Living documentation** - Contract IS the documentation
- ✅ **Prevents breaking changes** - Can't deploy if contract violated
- ✅ **Clear ownership** - Who owns the data
- ✅ **Self-service** - Consumers can validate anytime
- ✅ **Version controlled** - Changes tracked in git
- ✅ **Automated enforcement** - No manual checks needed

---

## Additional Use Cases

### Use Case 5: Partner Data Validation

Validate data from external partners before accepting:

```yaml
# partner_data_contract.yaml
checks:
  - name: file_format_validation
    column: order_date
    rules:
      regex: "^\\d{4}-\\d{2}-\\d{2}$"  # ISO format required

  - name: required_fields
    column: partner_order_id
    rules:
      not_null: true
      unique: true
```

```bash
# In partner data ingestion pipeline
if datacheck validate partner_export.csv --config partner_data_contract.yaml; then
  echo "✅ Partner data accepted"
  process_partner_data.py
else
  echo "❌ Partner data rejected - sending back to partner"
  notify_partner "Data quality issues found"
fi
```

### Use Case 6: Regulatory Compliance

Ensure data meets compliance requirements (GDPR, HIPAA, SOX):

```yaml
# gdpr_compliance.yaml
checks:
  # Must have consent
  - name: consent_required
    column: marketing_consent
    rules:
      not_null: true
      allowed_values: ["granted", "denied"]

  # Age verification (GDPR: 16+ in EU)
  - name: age_compliance
    column: age
    rules:
      min: 16

  # Email must be valid for GDPR requests
  - name: email_required
    column: email
    rules:
      not_null: true
      regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
```

---

## Key Patterns Across Use Cases

### 1. Fail Fast
Validate early in the pipeline to avoid expensive failures.

### 2. Contracts as Code
Use validation configs as living documentation and contracts.

### 3. Standardization
One tool for all validation needs across the organization.

### 4. Self-Service
Anyone can create and run validations without custom code.

### 5. Automation
Integrate into CI/CD, Airflow, cron jobs, pre-commit hooks.

---

## Next Steps

- See [Configuration Guide](../user-guide/configuration.md) to write your own rules
- Check [Integration Guide](../integration/cicd.md) for CI/CD setup
- Explore [GitHub Actions](../integration/github-actions.md) examples
- Read about [Data Pipelines](../integration/data-pipelines.md) integration
