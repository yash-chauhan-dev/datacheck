# Advanced DataCheck Example

This example demonstrates advanced validation features including unique constraints, regex patterns, and allowed values.

## Files

- `customer_data.csv` - Valid customer data
- `customer_data_with_errors.csv` - Customer data with intentional errors
- `validation_config.yaml` - Advanced validation rules

## Validation Rules

This example demonstrates:

### Complex Regex Patterns
- **Customer ID**: Format `C###` (C followed by 3 digits)
- **Name**: Only letters allowed
- **Email**: Valid email format
- **Phone**: International format with country code

### Uniqueness Constraints
- **Customer ID**: Must be unique across all records
- **Email**: Must be unique across all records

### Allowed Values
- **Country**: Only specific countries supported
- **Subscription Tier**: Must be one of: basic, premium, enterprise

### Range Validation
- **Monthly Spend**: Between 0 and 10,000

## Running the Examples

### Validate valid data (all checks pass):
```bash
datacheck validate customer_data.csv --config validation_config.yaml
```

### Validate data with errors (shows failures):
```bash
datacheck validate customer_data_with_errors.csv --config validation_config.yaml
```

### Get JSON output for integration:
```bash
datacheck validate customer_data.csv --config validation_config.yaml --format json
```

## Expected Errors in customer_data_with_errors.csv

1. **Row 2 (Bob)**: Invalid customer_id format ("INVALID" doesn't match `C###`)
2. **Row 3 (Carol)**:
   - Invalid first_name (contains numbers)
   - Invalid email format
3. **Row 4 (David)**:
   - Invalid phone format (missing country code)
   - Invalid country ("InvalidCountry" not in allowed list)
   - Invalid subscription_tier ("invalid_tier" not in allowed list)
4. **Row 5 (Eve)**: Negative monthly_spend (-50.00)

## Use Cases

This configuration is ideal for:
- Customer data validation
- User registration data
- Subscription management systems
- CRM data quality checks
- Data warehouse ETL validation

## Extending the Example

Try adding more rules:
```yaml
- name: signup_date_validation
  column: signup_date
  rules:
    not_null: true
    # Add custom date validation logic
```
