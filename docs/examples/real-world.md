# Real-World Scenarios

Explore real-world data validation scenarios across different industries and use cases.

---

## E-Commerce: Order Validation

Validate daily order exports before loading to data warehouse.

### Scenario

- 50K orders per day
- Must validate before warehouse load
- Invalid data breaks downstream analytics

### Data Sample

```csv
order_id,customer_id,product_sku,quantity,price,status,order_date
ORD2024010001,CUST00123,SKU456789,2,29.99,pending,2024-01-15
ORD2024010002,CUST00124,SKU456790,1,49.99,shipped,2024-01-15
```

### Validation Rules

```yaml
checks:
  - name: order_id_format
    column: order_id
    rules:
      not_null: true
      unique: true
      regex: "^ORD[0-9]{10}$"

  - name: customer_id_valid
    column: customer_id
    rules:
      not_null: true
      regex: "^CUST[0-9]{5}$"

  - name: product_sku_format
    column: product_sku
    rules:
      not_null: true
      regex: "^SKU[0-9]{6}$"

  - name: quantity_validation
    column: quantity
    rules:
      not_null: true
      min: 1
      max: 1000

  - name: price_validation
    column: price
    rules:
      not_null: true
      min: 0.01
      max: 99999.99

  - name: status_validation
    column: status
    rules:
      not_null: true
      allowed_values: ["pending", "processing", "shipped", "delivered", "cancelled", "refunded"]
```

### Pipeline Integration

```bash
#!/bin/bash
# daily_order_load.sh

DATE=$(date +%Y%m%d)
EXPORT_FILE="orders_${DATE}.csv"

# Download from S3
aws s3 cp s3://exports/orders/${DATE}/ ./${EXPORT_FILE}

# Validate
datacheck validate ${EXPORT_FILE} --config order_validation.yaml

if [ $? -eq 0 ]; then
  python load_to_snowflake.py ${EXPORT_FILE}
  aws s3 cp ${EXPORT_FILE} s3://archive/orders/${DATE}/
else
  python alert_team.py "Order validation failed for ${DATE}"
  exit 1
fi
```

---

## Healthcare: Patient Data Validation

Ensure patient data meets HIPAA and quality standards.

### Scenario

- Patient records from multiple clinics
- Must validate before EHR import
- HIPAA compliance required

### Validation Rules

```yaml
checks:
  - name: patient_id_unique
    column: patient_id
    rules:
      not_null: true
      unique: true
      regex: "^P[0-9]{8}$"

  - name: date_of_birth_valid
    column: date_of_birth
    rules:
      not_null: true
      regex: "^\\d{4}-\\d{2}-\\d{2}$"

  - name: ssn_format
    column: ssn_encrypted
    rules:
      not_null: true
      unique: true

  - name: email_hipaa_compliant
    column: email
    rules:
      not_null: true
      regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

  - name: consent_status
    column: consent_status
    rules:
      not_null: true
      allowed_values: ["granted", "denied", "pending", "revoked"]
```

---

## Financial: Transaction Validation

Validate financial transactions before processing.

### Scenario

- Real-time transaction feed
- Fraud detection requirements
- Regulatory compliance (SOX, PCI-DSS)

### Validation Rules

```yaml
checks:
  - name: transaction_id_unique
    column: transaction_id
    rules:
      not_null: true
      unique: true
      regex: "^TXN[0-9]{12}$"

  - name: amount_validation
    column: amount
    rules:
      not_null: true
      min: 0.01
      max: 999999.99

  - name: currency_code
    column: currency
    rules:
      not_null: true
      allowed_values: ["USD", "EUR", "GBP", "JPY", "CAD", "AUD"]

  - name: account_number_format
    column: account_number
    rules:
      not_null: true
      regex: "^[0-9]{10,12}$"

  - name: transaction_type
    column: type
    rules:
      not_null: true
      allowed_values: ["debit", "credit", "transfer", "withdrawal", "deposit"]

  - name: status_validation
    column: status
    rules:
      not_null: true
      allowed_values: ["pending", "authorized", "settled", "failed", "reversed"]
```

---

## Marketing: Campaign Data Validation

Validate marketing campaign data before analytics.

### Validation Rules

```yaml
checks:
  - name: campaign_id
    column: campaign_id
    rules:
      not_null: true
      regex: "^CAMP[0-9]{6}$"

  - name: email_validation
    column: subscriber_email
    rules:
      not_null: true
      regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

  - name: click_rate_validation
    column: click_rate
    rules:
      min: 0
      max: 1

  - name: engagement_score
    column: engagement_score
    rules:
      not_null: true
      min: 0
      max: 100

  - name: campaign_status
    column: status
    rules:
      allowed_values: ["draft", "scheduled", "running", "completed", "paused", "archived"]
```

---

## IoT: Sensor Data Validation

Validate IoT sensor readings before storage.

### Scenario

- Temperature sensors across facilities
- Data ingested every 5 minutes
- Invalid readings cause equipment damage

### Validation Rules

```yaml
checks:
  - name: sensor_id_format
    column: sensor_id
    rules:
      not_null: true
      regex: "^SENSOR[0-9]{4}$"

  - name: temperature_range
    column: temperature_celsius
    rules:
      not_null: true
      min: -50
      max: 150

  - name: humidity_range
    column: humidity_percent
    rules:
      not_null: true
      min: 0
      max: 100

  - name: pressure_validation
    column: pressure_kpa
    rules:
      not_null: true
      min: 50
      max: 200

  - name: sensor_status
    column: status
    rules:
      not_null: true
      allowed_values: ["active", "maintenance", "error", "offline"]
```

---

## Best Practices from Real-World Use

1. **Start with critical fields** - Focus on IDs, amounts, status first
2. **Add rules incrementally** - Don't try to validate everything at once
3. **Monitor failure rates** - Track which rules fail most often
4. **Version config files** - Keep validation rules in git
5. **Test with real data** - Use production samples for testing
6. **Document business rules** - Add comments explaining why rules exist
7. **Set up alerts** - Notify team when validation fails
8. **Regular reviews** - Update rules as business requirements change

---

## Common Patterns

### Unique Identifiers
Always validate IDs are non-null, unique, and properly formatted.

### Status Fields
Use `allowed_values` to enforce valid states.

### Amounts/Quantities
Set realistic min/max bounds to catch data entry errors.

### Format Validation
Use regex for emails, phone numbers, SKUs, etc.

### Required Fields
Start with `not_null` on all critical fields.

---

## Next Steps

- See all [Validation Rules](../user-guide/validation-rules.md)
- Learn [Configuration](../user-guide/configuration.md) best practices
- Set up [CI/CD Integration](../integration/cicd.md)
