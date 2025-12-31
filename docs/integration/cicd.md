# CI/CD Integration

Integrate DataCheck into your continuous integration and deployment pipelines.

---

## Supported Platforms

- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI
- Travis CI
- Azure Pipelines

---

## GitHub Actions

See the [GitHub Actions](github-actions.md) guide for detailed examples.

---

## GitLab CI

```yaml
validate_data:
  stage: test
  image: python:3.12
  script:
    - pip install datacheck-cli
    - datacheck validate data.csv --config validation.yaml
```

---

## Jenkins

```groovy
stage('Data Validation') {
  steps {
    sh '''
      pip install datacheck-cli
      datacheck validate data.csv --config validation.yaml
    '''
  }
}
```

---

## Key Concepts

1. **Exit Codes** - DataCheck uses standard exit codes (0=success, 1=failure)
2. **JSON Output** - Use `--format json` for machine-readable results
3. **Fail Fast** - Stop pipeline on validation failure
4. **Artifacts** - Save validation results for audit trails

---

See [GitHub Actions](github-actions.md) for comprehensive examples.
