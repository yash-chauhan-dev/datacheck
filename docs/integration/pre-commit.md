# Pre-commit Hooks

Validate data files before committing to version control.

---

## Setup

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

echo "Running data validation..."

for file in $(git diff --cached --name-only | grep '\\.csv$'); do
  if [ -f "validation/${file%.csv}.yaml" ]; then
    echo "Validating $file..."
    datacheck validate "$file" --config "validation/${file%.csv}.yaml"
    
    if [ $? -ne 0 ]; then
      echo "❌ Validation failed for $file"
      exit 1
    fi
  fi
done

echo "✅ All data files validated"
```

Make it executable:

```bash
chmod +x .git/hooks/pre-commit
```

---

## Using pre-commit Framework

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: datacheck
        name: DataCheck Validation
        entry: datacheck validate
        language: system
        files: '\\.csv$'
        pass_filenames: true
```

---

## Best Practices

1. Only validate changed files
2. Keep validation fast (< 10 seconds)
3. Allow bypass with `--no-verify` for emergencies
4. Document which files require validation

---

See [Configuration](../user-guide/configuration.md) for validation rules.
