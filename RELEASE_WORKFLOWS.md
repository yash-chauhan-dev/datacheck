# Release Workflows Guide

DataCheck supports **two automated release approaches**. Choose the one that fits your workflow best.

---

## 🚀 Approach 1: Auto-Release on PR Merge (Recommended)

**Best for**: Teams who want fully automated releases when features are merged.

### How It Works

1. Developer creates a feature branch
2. Developer bumps version in `pyproject.toml` (using `poetry version`)
3. Developer updates `CHANGELOG.md`
4. PR is opened → CI validates version was bumped
5. PR is merged to `main` → **Automatic release triggered**
   - ⏳ Waits for CI workflow to pass
   - ✅ Validates version changed and increased
   - ✅ Runs full test suite (Python 3.10, 3.11, 3.12)
   - 📦 Builds package
   - 🏷️ Creates git tag automatically
   - 📤 Publishes to PyPI
   - 🎉 Creates GitHub release with changelog

### Setup

**No setup required!** The workflow is already configured:
- `.github/workflows/auto-release.yml` - Main release workflow
- `.github/workflows/pr-version-check.yml` - PR validation

### Usage

#### Step 1: Create Feature Branch

```bash
git checkout -b feature/my-awesome-feature
# Make your changes...
```

#### Step 2: Bump Version

```bash
# For bug fixes (0.1.0 → 0.1.1)
poetry version patch

# For new features (0.1.0 → 0.2.0)
poetry version minor

# For breaking changes (0.1.0 → 1.0.0)
poetry version major
```

#### Step 3: Update CHANGELOG.md

Add a new section at the top:

```markdown
## [0.2.0] - 2025-01-15

### Added
- New awesome feature that does X
- Support for Y format

### Fixed
- Bug in Z validation

[0.2.0]: https://github.com/yash-chauhan-dev/datacheck/releases/tag/v0.2.0
```

#### Step 4: Commit and Push

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "feat: Add awesome new feature

- Implement feature X
- Add support for Y
- Bump version to 0.2.0"

git push origin feature/my-awesome-feature
```

#### Step 5: Create Pull Request

- Open PR on GitHub
- **PR check will automatically validate**:
  - ✅ Version was bumped
  - ✅ Version increased (not decreased)
  - ✅ Follows semantic versioning
  - ⚠️ Warns if CHANGELOG.md not updated

#### Step 6: Merge PR

**When PR is merged to `main`:**
1. CI workflow runs automatically
2. Auto-release workflow triggers (waits for CI to pass)
3. CI must pass ✅ (if CI fails, release is blocked)
4. Checks version changed
5. Runs full test suite (double-check after CI)
6. Creates git tag `v0.2.0`
7. Publishes to PyPI
8. Creates GitHub release

**Total time:** ~10-15 minutes ⏱️ (includes CI wait)

### What If I Don't Want to Release?

If your PR doesn't need a release (docs, tests, refactoring):
- **Don't bump the version**
- PR check will warn but won't fail
- Merge normally - no release triggered

---

## 🏷️ Approach 2: Manual Tag-Based Release

**Best for**: When you want explicit control over release timing.

### How It Works

1. Merge features to `main` without bumping version
2. When ready to release, manually bump version
3. Push git tag → Release triggered

### Setup

**Already configured!** The tag-based workflow is at:
- `.github/workflows/release.yml`

### Usage

#### Step 1: Prepare Release

```bash
# Make sure you're on main
git checkout main
git pull origin main

# Bump version
poetry version minor  # or patch/major

# Update CHANGELOG.md
# (Add release notes for this version)
```

#### Step 2: Commit and Push

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "chore: Release v0.2.0"
git push origin main
```

#### Step 3: Create and Push Tag

```bash
# Create annotated tag
git tag -a v0.2.0 -m "Release v0.2.0"

# Push tag to trigger release
git push origin v0.2.0
```

**When tag is pushed:**
- Release workflow triggers
- Tests run
- Package published to PyPI
- GitHub release created

---

## 📊 Comparison

| Feature | Auto-Release (PR Merge) | Manual Tag-Based |
|---------|------------------------|------------------|
| **Release Trigger** | Merge to main | Push git tag |
| **Version Validation** | ✅ Automatic in PR | ❌ Manual check |
| **Control** | Less (auto on merge) | More (explicit tag) |
| **Speed** | Faster (one step) | Slower (two steps) |
| **Safety** | High (PR checks) | Medium (manual) |
| **Best For** | Continuous delivery | Scheduled releases |

---

## 🔧 Configuration

Both workflows support the same configuration options.

### PyPI Publishing

**Option A: API Token (Simpler)**

1. Generate token at https://pypi.org/manage/account/token/
2. Add to GitHub secrets as `PYPI_API_TOKEN`

Both workflows use:
```yaml
password: ${{ secrets.PYPI_API_TOKEN }}
```

**Option B: Trusted Publishing (More Secure)**

1. Publish first release manually (one-time)
2. Configure at https://pypi.org/manage/project/datacheck-cli/settings/publishing/
3. Remove `password:` line from workflows

Both workflows already support trusted publishing.

---

## 🛡️ Safety Features

Both workflows include:

### Pre-Release Validation
- ✅ **CI must pass first**: Auto-release waits for main CI workflow to succeed
- ✅ Full test suite on Python 3.10, 3.11, 3.12
- ✅ Linting with ruff
- ✅ Type checking with mypy
- ✅ Version format validation
- ✅ Version increase validation

### Fail-Safe Mechanisms
- **CI dependency**: Release blocked if CI workflow fails
- **Duplicate tag check**: Won't create existing tags
- **Test failure = no release**: Package only published if all tests pass
- **Version validation**: Won't release if version decreased
- **Artifact preservation**: Build artifacts stored for 90 days

### Recommended: Branch Protection Rules
For additional safety, configure branch protection on `main`:
1. Go to: Settings → Branches → Add rule for `main`
2. Enable:
   - ✅ Require pull request reviews
   - ✅ Require status checks to pass (select "CI" and "PR Version Check")
   - ✅ Require branches to be up to date
3. This ensures PRs can't merge unless CI passes and version is valid

---

## 📝 Best Practices

### Semantic Versioning

Follow [semver](https://semver.org/):

- **Patch** (0.1.0 → 0.1.1): Bug fixes, no new features
- **Minor** (0.1.0 → 0.2.0): New features, backward compatible
- **Major** (0.1.0 → 1.0.0): Breaking changes

### CHANGELOG.md Format

Use [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [0.2.0] - 2025-01-15

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security fixes

[0.2.0]: https://github.com/yash-chauhan-dev/datacheck/releases/tag/v0.2.0
```

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: Add new validation rule
fix: Resolve issue with CSV loader
docs: Update README examples
chore: Bump version to 0.2.0
```

---

## 🔍 Monitoring Releases

### GitHub Actions
- View workflow runs: https://github.com/yash-chauhan-dev/datacheck/actions

### PyPI
- Package page: https://pypi.org/project/datacheck-cli/
- Download stats: https://pepy.tech/project/datacheck-cli

### GitHub Releases
- Releases page: https://github.com/yash-chauhan-dev/datacheck/releases

---

## 🐛 Troubleshooting

### "Tag already exists"
**Problem**: Trying to create a tag that exists.
**Solution**: Check existing tags with `git tag -l` and use a new version number.

### "Version didn't increase"
**Problem**: New version is not higher than previous.
**Solution**: Use `poetry version patch/minor/major` to properly bump version.

### "CI workflow failed, release blocked"
**Problem**: Auto-release is waiting but CI workflow failed.
**Solution**:
- Check CI workflow logs: Actions tab → CI workflow
- Fix the failing tests/linting/type errors
- Push a fix commit to `main`
- CI will re-run and auto-release will proceed if it passes

### "Tests failed"
**Problem**: Test suite failed, release blocked.
**Solution**: Fix tests before merging/tagging.

### "PyPI upload failed"
**Problem**: Authentication error or network issue.
**Solution**:
- Check `PYPI_API_TOKEN` secret is set correctly
- Or configure Trusted Publishing

### "Version not bumped" warning in PR
**Problem**: PR check warns version wasn't bumped.
**Solution**:
- If you want to release: Bump version with `poetry version`
- If no release needed: Ignore warning and merge normally

---

## 🎯 Which Approach Should You Use?

### Use Auto-Release (PR Merge) If:
- ✅ You want continuous delivery
- ✅ You release frequently (every feature)
- ✅ Your team follows strict PR review
- ✅ You want maximum automation

### Use Manual Tag-Based If:
- ✅ You want to batch multiple features into one release
- ✅ You release on a schedule (weekly, monthly)
- ✅ You want explicit control over release timing
- ✅ You need time to prepare release notes

### Can You Use Both?
**Yes!** Both workflows can coexist:
- Use auto-release for patch releases
- Use manual tags for major/minor releases

Or disable one by deleting/renaming the workflow file.

---

## 📚 Related Documentation

- **PYPI_RELEASE_GUIDE.md**: Manual release process
- **AUTOMATED_RELEASE.md**: Original automated release guide (tag-based)
- **RELEASE_CHECKLIST.md**: Interactive release checklist
- **CHANGELOG.md**: Release history

---

## 🚦 Quick Start Cheatsheet

### Auto-Release (PR Merge)
```bash
# 1. Create branch
git checkout -b feature/my-feature

# 2. Make changes + bump version
poetry version patch

# 3. Update CHANGELOG.md

# 4. Commit and push
git add .
git commit -m "feat: My feature"
git push origin feature/my-feature

# 5. Create PR, get approved, merge
# → Release happens automatically!
```

### Manual Tag-Based
```bash
# 1. Make sure you're on main
git checkout main
git pull

# 2. Bump version
poetry version patch

# 3. Update CHANGELOG.md

# 4. Commit
git add .
git commit -m "chore: Release v0.1.1"
git push

# 5. Tag and push
git tag -a v0.1.1 -m "Release v0.1.1"
git push origin v0.1.1

# → Release triggered!
```

---

**Need help?** Open an issue: https://github.com/yash-chauhan-dev/datacheck/issues
