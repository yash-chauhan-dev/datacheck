# Configuration

Learn how to write and organize validation configuration files.

---

## Basic Structure

DataCheck uses YAML files for configuration:

```yaml
checks:
  - name: check_name
    column: column_name
    rules:
      rule_type: rule_value
```

---

## Configuration File

### Minimal Example

```yaml
checks:
  - name: email_check
    column: email
    rules:
      not_null: true
```

### Complete Example

```yaml
checks:
  - name: customer_id_validation
    column: customer_id
    rules:
      not_null: true
      unique: true

  - name: email_validation
    column: email
    rules:
      not_null: true
      unique: true
      regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

  - name: age_validation
    column: age
    rules:
      not_null: true
      min: 18
      max: 120

  - name: status_validation
    column: status
    rules:
      not_null: true
      allowed_values: ["active", "inactive", "suspended"]
```

---

## Auto-Discovery

DataCheck automatically searches for config files in this order:

1. `.datacheck.yaml`
2. `.datacheck.yml`
3. `datacheck.yaml`
4. `datacheck.yml`

**Usage**:
```bash
# With auto-discovery
datacheck validate data.csv

# Explicit config
datacheck validate data.csv --config custom_rules.yaml
```

---

## Configuration Keys

### `name` (required)

Descriptive name for the validation check.

```yaml
- name: email_format_validation
```

**Best practices**:
- Use snake_case or kebab-case
- Be descriptive
- Unique per configuration

### `column` (required)

Column name to validate.

```yaml
column: email
```

**Notes**:
- Must match exact column name in data
- Case-sensitive
- Whitespace preserved

### `rules` (required)

Dictionary of validation rules to apply.

```yaml
rules:
  not_null: true
  min: 0
  max: 100
```

---

## Comments and Documentation

Add comments to document your validation logic:

```yaml
checks:
  # User identification must be unique and present
  - name: user_id_validation
    column: user_id
    rules:
      not_null: true    # Required field
      unique: true       # No duplicate users

  # GDPR compliance - minimum age 16 in EU
  - name: age_gdpr_compliance
    column: age
    rules:
      min: 16           # GDPR requirement
      max: 120          # Sanity check
```

---

## Organizing Large Configurations

### By Entity

```yaml
# User validation rules
checks:
  - name: user_id_check
    column: user_id
    rules:
      not_null: true
      unique: true

  - name: user_email_check
    column: email
    rules:
      not_null: true
      unique: true

# Order validation rules
  - name: order_id_check
    column: order_id
    rules:
      not_null: true
      unique: true
```

### By Priority

```yaml
# Critical validations - must pass
checks:
  - name: id_validation
    column: id
    rules:
      not_null: true
      unique: true

# Important validations
  - name: email_validation
    column: email
    rules:
      not_null: true

# Optional validations
  - name: phone_validation
    column: phone
    rules:
      regex: "^\\+1-[0-9]{3}-[0-9]{4}$"
```

---

## Environment-Specific Configs

Different rules for different environments:

```yaml
# validation_dev.yaml (lenient for development)
checks:
  - name: email_check
    column: email
    rules:
      not_null: true

# validation_prod.yaml (strict for production)
checks:
  - name: email_check
    column: email
    rules:
      not_null: true
      unique: true
      regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
```

---

## Best Practices

1. **Version control** - Keep configs in git
2. **Use comments** - Document why rules exist
3. **Test thoroughly** - Validate with sample data first
4. **Start simple** - Add rules incrementally
5. **Descriptive names** - Make checks easy to understand
6. **Group related checks** - Organize logically

---

## Common Patterns

### Required Fields Only
```yaml
checks:
  - name: required_fields
    column: customer_id
    rules:
      not_null: true
```

### Unique Identifiers
```yaml
checks:
  - name: unique_identifier
    column: order_id
    rules:
      not_null: true
      unique: true
```

### Format Validation
```yaml
checks:
  - name: format_check
    column: email
    rules:
      not_null: true
      regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
```

### Range Validation
```yaml
checks:
  - name: range_check
    column: price
    rules:
      not_null: true
      min: 0
      max: 999999.99
```

### Enum Validation
```yaml
checks:
  - name: enum_check
    column: status
    rules:
      not_null: true
      allowed_values: ["pending", "approved", "rejected"]
```

---

## Next Steps

- See [Validation Rules](validation-rules.md) for all available rules
- Check [Examples](../examples/real-world.md) for real-world configs
- Learn about [Output Formats](output-formats.md)
