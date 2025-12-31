---
name: Bug Report
about: Report a bug or unexpected behavior
title: '[BUG] '
labels: 'type: bug'
assignees: ''
---

## Bug Description

A clear and concise description of what the bug is.

## Steps to Reproduce

1. Go to '...'
2. Run command '...'
3. Use config file '...'
4. See error

## Expected Behavior

A clear and concise description of what you expected to happen.

## Actual Behavior

What actually happened instead.

## Error Messages

```
Paste any error messages or stack traces here
```

## Environment

**DataCheck Version:**
```bash
datacheck version
# Output:
```

**Python Version:**
```bash
python --version
# Output:
```

**Operating System:**
- [ ] Windows
- [ ] macOS
- [ ] Linux (specify distribution: _____________)

**Installation Method:**
- [ ] pip install datacheck
- [ ] poetry install
- [ ] From source

## Data Format

What type of data were you validating?
- [ ] CSV
- [ ] Parquet
- [ ] SQLite database
- [ ] Other: _____________

## Configuration File

```yaml
# Paste your validation_config.yaml here (remove sensitive data)
```

## Sample Data

If possible, provide a minimal sample of the data that causes the issue (remove sensitive information):

```csv
# Sample data here
```

## Additional Context

Add any other context about the problem here. Screenshots are helpful!

## Possible Solution

(Optional) If you have an idea of what might be causing this or how to fix it, please share!

---

**Checklist:**
- [ ] I have searched existing issues to ensure this bug hasn't been reported
- [ ] I have tested with the latest version of DataCheck
- [ ] I have included all required information above
