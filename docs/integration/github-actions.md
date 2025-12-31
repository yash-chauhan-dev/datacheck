# GitHub Actions Integration

Integrate DataCheck into your GitHub Actions workflows for automated data quality validation.

---

## Basic Workflow

Add data validation to your CI/CD pipeline:

```yaml
name: Data Quality Check

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  validate-data:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install DataCheck
        run: pip install datacheck-cli

      - name: Validate Data
        run: |
          datacheck validate data/customers.csv \
            --config validation/customers.yaml \
            --format json \
            --json-output results.json

      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: validation-results
          path: results.json
```

---

## Validate on Schedule

Run validation checks on a schedule:

```yaml
name: Daily Data Validation

on:
  schedule:
    - cron: '0 8 * * *'  # Every day at 8 AM UTC

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

      - name: Download latest data
        run: |
          # Download from S3, database, API, etc.
          aws s3 cp s3://bucket/data/export.csv ./data.csv

      - name: Validate
        run: datacheck validate data.csv --config validation.yaml

      - name: Notify on Failure
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "❌ Daily data validation failed!",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "Data validation failed. Check the <${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|workflow logs>."
                  }
                }
              ]
            }
```

---

## Validate Multiple Files

Validate all CSV files in a directory:

```yaml
- name: Validate All CSV Files
  run: |
    for file in data/*.csv; do
      echo "Validating $file..."
      datacheck validate "$file" --config "config/$(basename $file .csv).yaml"
      
      if [ $? -ne 0 ]; then
        echo "❌ Validation failed for $file"
        exit 1
      fi
    done
```

---

## Matrix Strategy

Test across different data sources:

```yaml
jobs:
  validate:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        dataset:
          - name: customers
            file: data/customers.csv
            config: config/customers.yaml
          - name: orders
            file: data/orders.csv
            config: config/orders.yaml
          - name: products
            file: data/products.csv
            config: config/products.yaml
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install DataCheck
        run: pip install datacheck-cli
      
      - name: Validate ${{ matrix.dataset.name }}
        run: |
          datacheck validate ${{ matrix.dataset.file }} \
            --config ${{ matrix.dataset.config }}
```

---

## Comment on PR

Post validation results as PR comment:

```yaml
- name: Validate Data
  id: validate
  run: |
    datacheck validate data.csv \
      --config validation.yaml \
      --format json \
      --json-output results.json
  continue-on-error: true

- name: Comment PR
  uses: actions/github-script@v7
  with:
    script: |
      const fs = require('fs');
      const results = JSON.parse(fs.readFileSync('results.json', 'utf8'));
      
      const comment = `## Data Validation Results
      
      **Status**: ${results.summary.all_passed ? '✅ Passed' : '❌ Failed'}
      
      | Metric | Value |
      |--------|-------|
      | Total Checks | ${results.summary.total_checks} |
      | Passed | ${results.summary.passed_checks} |
      | Failed | ${results.summary.failed_checks} |
      | Errors | ${results.summary.error_checks} |
      
      ${results.summary.all_passed ? '' : '⚠️ Check the workflow logs for details on failed validations.'}
      `;
      
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: comment
      });
```

---

## Block Merge on Failure

Require validation to pass before merging:

```yaml
name: Required Data Validation

on:
  pull_request:
    branches: [ main ]

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

      - name: Validate (Required)
        run: datacheck validate data.csv --config validation.yaml
        # This step will fail the workflow if validation fails
```

Then in repository settings:
1. Go to Settings → Branches
2. Add branch protection rule for `main`
3. Require status checks to pass: Select "Required Data Validation"

---

## Secrets and Variables

Store sensitive information securely:

```yaml
- name: Download from Database
  env:
    DB_HOST: ${{ secrets.DB_HOST }}
    DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
  run: |
    python export_from_db.py
    datacheck validate export.csv --config validation.yaml
```

---

## Caching for Speed

Cache dependencies for faster runs:

```yaml
- name: Cache pip packages
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

- name: Install DataCheck
  run: pip install datacheck-cli
```

---

## Complete Example

Production-ready workflow with all best practices:

```yaml
name: Data Quality Pipeline

on:
  push:
    branches: [ main ]
    paths:
      - 'data/**'
      - 'validation/**'
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  validate:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write  # For PR comments
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install datacheck-cli
          pip install boto3  # If downloading from S3

      - name: Download latest data
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          aws s3 sync s3://my-bucket/data/ ./data/

      - name: Validate data
        id: validate
        run: |
          datacheck validate data/export.csv \
            --config validation/rules.yaml \
            --format json \
            --json-output results.json
        continue-on-error: true

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: validation-results-${{ github.run_number }}
          path: results.json
          retention-days: 30

      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const results = JSON.parse(fs.readFileSync('results.json'));
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Validation Results\n\n${results.summary.all_passed ? '✅ All checks passed' : '❌ Some checks failed'}\n\n**Details**: ${results.summary.passed_checks}/${results.summary.total_checks} passed`
            });

      - name: Fail if validation failed
        if: steps.validate.outcome == 'failure'
        run: exit 1

      - name: Notify Slack on failure
        if: failure() && github.ref == 'refs/heads/main'
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {"text": "❌ Data validation failed on main branch"}
```

---

## Best Practices

1. **Always upload results** - Use `if: always()` to save results even on failure
2. **Use continue-on-error** - Allow workflow to complete for reporting
3. **Cache dependencies** - Speed up workflow with caching
4. **Notify on failures** - Alert team via Slack, email, etc.
5. **Use matrix strategy** - Validate multiple datasets in parallel
6. **Protect main branch** - Require validation to pass before merge
7. **Schedule regular checks** - Don't just validate on code changes

---

## Next Steps

- See [CI/CD Integration](cicd.md) for more platforms
- Learn about [Exit Codes](../user-guide/exit-codes.md)
- Check [Output Formats](../user-guide/output-formats.md) for JSON parsing
