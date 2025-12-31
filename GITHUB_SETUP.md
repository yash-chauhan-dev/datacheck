# GitHub Repository Setup Guide

This guide will help you configure your DataCheck repository for open-source collaboration.

## Table of Contents

- [Repository Settings](#repository-settings)
- [Branch Protection Rules](#branch-protection-rules)
- [GitHub Actions Permissions](#github-actions-permissions)
- [Collaboration Settings](#collaboration-settings)
- [Security Settings](#security-settings)
- [Optional Integrations](#optional-integrations)

---

## Repository Settings

Navigate to **Settings** in your GitHub repository.

### General Settings

#### About Section (Top of main page)
1. Click **⚙️ (gear icon)** next to "About"
2. Configure:
   - **Description**: `Lightweight data quality validation CLI tool for CSV, Parquet, and database files`
   - **Website**: `https://github.com/yash-chauhan-dev/datacheck` (or your docs site)
   - **Topics** (add these tags):
     - `data-quality`
     - `data-validation`
     - `cli-tool`
     - `python`
     - `pandas`
     - `data-engineering`
     - `testing`
     - `csv`
     - `parquet`
     - `sqlite`
   - ✅ Check "Include in the home page"

#### Features

Enable these features in **Settings → General**:

- ✅ **Wikis** (optional - for additional documentation)
- ✅ **Issues** (required for bug reports and feature requests)
- ✅ **Sponsorships** (optional - if you want GitHub Sponsors)
- ✅ **Preserve this repository** (archives repo in Arctic Code Vault)
- ✅ **Discussions** (recommended - for Q&A and community)

#### Pull Requests

Configure in **Settings → General → Pull Requests**:

- ✅ **Allow merge commits**
- ✅ **Allow squash merging** (recommended as default)
- ✅ **Allow rebase merging**
- ✅ **Always suggest updating pull request branches**
- ✅ **Allow auto-merge**
- ✅ **Automatically delete head branches** (keeps repo clean)

#### Default Branch

- Set to `main` (should already be configured)

---

## Branch Protection Rules

Protect your main branch from accidental changes.

### Setting Up Branch Protection

1. Go to **Settings → Branches**
2. Click **Add rule** under "Branch protection rules"
3. Branch name pattern: `main`

### Recommended Rules for `main` Branch

#### Protect Matching Branches

✅ **Require a pull request before merging**
   - Required approvals: `1` (you can increase later)
   - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ Require review from Code Owners (if you add CODEOWNERS file)

✅ **Require status checks to pass before merging**
   - ✅ Require branches to be up to date before merging
   - **Required status checks** (add these):
     - `test (ubuntu-latest, 3.10)`
     - `test (ubuntu-latest, 3.11)`
     - `test (ubuntu-latest, 3.12)`
     - `test (macos-latest, 3.10)`
     - `test (macos-latest, 3.11)`
     - `test (macos-latest, 3.12)`
     - `test (windows-latest, 3.10)`
     - `test (windows-latest, 3.11)`
     - `test (windows-latest, 3.12)`
     - `build`

✅ **Require conversation resolution before merging**

✅ **Require signed commits** (optional, recommended for security)

✅ **Require linear history** (optional, keeps history clean)

✅ **Include administrators** (enforces rules on repo admins too)

❌ **Allow force pushes** (keep disabled for safety)

❌ **Allow deletions** (keep disabled for safety)

### Click **Create** to save the rule

---

## GitHub Actions Permissions

Configure workflow permissions to ensure CI can run properly.

### Steps

1. Go to **Settings → Actions → General**

2. **Actions permissions:**
   - ✅ Select "Allow all actions and reusable workflows"

3. **Workflow permissions:**
   - ✅ Select "Read and write permissions"
   - ✅ Check "Allow GitHub Actions to create and approve pull requests"

4. **Fork pull request workflows:**
   - ✅ Select "Require approval for first-time contributors"

5. Click **Save**

---

## Collaboration Settings

### Issue Templates

Issue templates are already in `.github/ISSUE_TEMPLATE/` (will be created in next step).

### Labels

GitHub auto-creates basic labels. Add these custom labels:

Go to **Issues → Labels → New label**:

| Name | Color | Description |
|------|-------|-------------|
| `good first issue` | `7057ff` | Good for newcomers |
| `help wanted` | `008672` | Extra attention is needed |
| `priority: high` | `d73a4a` | High priority |
| `priority: low` | `0e8a16` | Low priority |
| `type: feature` | `a2eeef` | New feature request |
| `type: bug` | `d73a4a` | Something isn't working |
| `type: docs` | `0075ca` | Documentation improvements |
| `type: enhancement` | `84b6eb` | Improvement to existing feature |
| `status: needs-review` | `fbca04` | Awaiting review |
| `status: blocked` | `b60205` | Blocked by other issues |

### Collaborators

Initially, you're the only collaborator. Add team members in **Settings → Collaborators**.

Permission levels:
- **Read**: Can view and clone
- **Triage**: Can manage issues/PRs
- **Write**: Can push to non-protected branches
- **Maintain**: Can manage repo without access to sensitive actions
- **Admin**: Full access

---

## Security Settings

### Security Advisories

1. Go to **Security → Advisories**
2. Review and enable **Private vulnerability reporting**
3. This allows security researchers to privately report vulnerabilities

### Dependabot

Enable automated dependency updates:

1. Go to **Settings → Security → Code security and analysis**

2. Enable these features:
   - ✅ **Dependency graph** (shows dependencies)
   - ✅ **Dependabot alerts** (security vulnerability alerts)
   - ✅ **Dependabot security updates** (auto-creates PRs for security fixes)
   - ✅ **Dependabot version updates** (optional - auto-updates dependencies)

3. For Dependabot version updates, create `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    reviewers:
      - "yash-chauhan-dev"
    labels:
      - "dependencies"
```

### Secret Scanning

- ✅ Enable **Secret scanning** (detects accidentally committed secrets)
- ✅ Enable **Push protection** (prevents pushing secrets)

---

## Optional Integrations

### Codecov (Code Coverage)

1. Sign up at https://codecov.io with your GitHub account
2. Add your repository
3. Get the upload token
4. Add as repository secret:
   - Go to **Settings → Secrets and variables → Actions**
   - Click **New repository secret**
   - Name: `CODECOV_TOKEN`
   - Value: (paste your token)

Your CI already uploads coverage to Codecov!

### Discussions

Enable for community Q&A:

1. Go to **Settings → General → Features**
2. ✅ Enable **Discussions**
3. Configure categories:
   - 💡 Ideas (for feature suggestions)
   - 🙏 Q&A (for questions)
   - 📣 Announcements (for updates)
   - 🐛 General (for general discussion)

### GitHub Pages (Optional Documentation Site)

If you want to host docs:

1. Create a `docs/` directory with documentation
2. Go to **Settings → Pages**
3. Source: `Deploy from a branch`
4. Branch: `main`, Folder: `/docs`
5. Click **Save**

### Sponsors (Optional)

If you want to accept sponsorships:

1. Create `.github/FUNDING.yml`:

```yaml
# Supported platforms
github: [yash-chauhan-dev]
# Other platforms (optional)
# patreon: username
# ko_fi: username
# custom: ["https://www.buymeacoffee.com/username"]
```

2. Go to **Settings → General → Features**
3. ✅ Enable **Sponsorships**

---

## Repository Badges

Add these badges to your README for better visibility:

```markdown
[![CI](https://github.com/yash-chauhan-dev/datacheck/workflows/CI/badge.svg)](https://github.com/yash-chauhan-dev/datacheck/actions)
[![codecov](https://codecov.io/gh/yash-chauhan-dev/datacheck/branch/main/graph/badge.svg)](https://codecov.io/gh/yash-chauhan-dev/datacheck)
[![PyPI version](https://badge.fury.io/py/datacheck.svg)](https://badge.fury.io/py/datacheck)
[![Python Versions](https://img.shields.io/pypi/pyversions/datacheck.svg)](https://pypi.org/project/datacheck/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
```

---

## Social Preview

Set a nice preview image for social media shares:

1. Go to **Settings → General**
2. Scroll to **Social preview**
3. Click **Edit**
4. Upload an image (1280x640px recommended)
   - Create a simple banner with "DataCheck" logo/text
   - Include tagline: "Lightweight data quality validation"

---

## Checklist

Use this checklist to ensure you've configured everything:

### Essential Settings
- [ ] Repository description and topics added
- [ ] Issues enabled
- [ ] Pull request settings configured
- [ ] Main branch protection rules added
- [ ] GitHub Actions permissions set
- [ ] Dependabot enabled
- [ ] Secret scanning enabled

### Recommended Settings
- [ ] Discussions enabled
- [ ] Auto-delete head branches enabled
- [ ] Require conversation resolution enabled
- [ ] Custom labels created
- [ ] Social preview image uploaded

### Optional Settings
- [ ] Codecov integration configured
- [ ] GitHub Sponsors configured
- [ ] GitHub Pages configured
- [ ] Wiki enabled

---

## Quick Start Commands

After configuring GitHub settings, verify everything works:

```bash
# Clone your repo
git clone https://github.com/yash-chauhan-dev/datacheck.git
cd datacheck

# Install dependencies
poetry install

# Run tests
poetry run pytest

# Create a feature branch
git checkout -b feature/my-feature

# Make changes, commit, and push
git add .
git commit -m "feat: add new feature"
git push origin feature/my-feature

# Create pull request on GitHub
# The branch protection rules will require CI to pass before merging
```

---

## Maintenance

### Regular Tasks

**Monthly:**
- Review and merge Dependabot PRs
- Check GitHub Insights for activity
- Review and triage open issues

**Quarterly:**
- Update documentation
- Review and update branch protection rules
- Audit collaborator access

**Yearly:**
- Update LICENSE copyright year
- Review and update SECURITY.md
- Celebrate your open-source project! 🎉

---

## Getting Help

If you need help with any of these settings:

1. **GitHub Docs**: https://docs.github.com
2. **GitHub Community**: https://github.community
3. **Open an issue** in your repo for specific questions

---

## Next Steps

After completing this setup:

1. ✅ Configure all settings in this guide
2. ✅ Create remaining open-source files (CODE_OF_CONDUCT, SECURITY, etc.)
3. ✅ Test the PR workflow by creating a test pull request
4. ✅ Announce your project on social media, Reddit, etc.
5. ✅ Add "good first issue" labels to beginner-friendly issues

**Your repository is now ready for open-source collaboration!** 🚀
