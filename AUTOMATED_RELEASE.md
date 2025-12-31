# Automated Release Pipeline

DataCheck now has an automated release pipeline! Just push a tag and everything happens automatically.

## 🚀 How It Works

When you push a version tag (e.g., `v0.1.0`), the pipeline automatically:

1. ✅ **Runs all tests** on Python 3.10, 3.11, 3.12
2. ✅ **Runs linting** (ruff) and type checking (mypy)
3. ✅ **Builds the package** (wheel and source distribution)
4. ✅ **Publishes to PyPI** automatically
5. ✅ **Creates a GitHub Release** with changelog and artifacts
6. ✅ **Generates release summary** with install instructions

**Zero manual work needed!** 🎉

---

## 📋 Setup (One-Time)

### Option 1: PyPI API Token (Simpler)

1. **Generate PyPI API Token:**
   - Go to: https://pypi.org/manage/account/token/
   - Click "Add API token"
   - Token name: `datacheck-github-actions`
   - Scope: "Entire account" (first release) or "Project: datacheck" (after first release)
   - Copy the token (starts with `pypi-`)

2. **Add to GitHub Secrets:**
   - Go to: https://github.com/yash-chauhan-dev/datacheck/settings/secrets/actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Paste your PyPI token
   - Click "Add secret"

3. **Done!** The workflow will use this token to publish.

### Option 2: Trusted Publishing (More Secure, Recommended)

Trusted Publishing eliminates the need for API tokens!

1. **First Manual Release:**
   - You need to publish v0.1.0 manually first (one time only)
   - Follow `PYPI_RELEASE_GUIDE.md` for the first release

2. **Configure Trusted Publishing on PyPI:**
   - Go to: https://pypi.org/manage/project/datacheck-cli/settings/publishing/
   - Add a new publisher:
     - **Owner**: `yash-chauhan-dev`
     - **Repository name**: `datacheck`
     - **Workflow name**: `release.yml`
     - **Environment name**: `pypi`
   - Click "Add"

3. **Update the workflow:**
   - In `.github/workflows/release.yml`, remove the `password:` line
   - The workflow will automatically use trusted publishing

4. **Done!** Much more secure, no tokens to manage.

---

## 🎯 How to Release

### Simple 3-Step Process:

```bash
# 1. Update version in pyproject.toml
# Edit: version = "0.1.0"

# 2. Update CHANGELOG.md
# Add entry for the new version

# 3. Create and push the tag
git add pyproject.toml CHANGELOG.md
git commit -m "chore: Bump version to 0.1.0"
git push origin main

git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

**That's it!** The pipeline takes over from here.

---

## 📊 What Happens Next

### Automatic Pipeline Steps:

1. **Test Job** (3-5 minutes):
   ```
   ✓ Install dependencies
   ✓ Run pytest with coverage
   ✓ Run ruff linting
   ✓ Run mypy type checking
   ```

2. **Build Job** (1-2 minutes):
   ```
   ✓ Build wheel and source distribution
   ✓ Upload artifacts for other jobs
   ```

3. **Publish to PyPI** (1 minute):
   ```
   ✓ Download build artifacts
   ✓ Publish to PyPI using API token or trusted publishing
   ✓ Package is now live on PyPI!
   ```

4. **Create GitHub Release** (1 minute):
   ```
   ✓ Extract changelog for this version
   ✓ Create GitHub release with notes
   ✓ Attach wheel and source dist files
   ✓ Mark as published (not draft)
   ```

5. **Announce** (< 1 minute):
   ```
   ✓ Generate release summary
   ✓ Show install command
   ✓ List next steps
   ```

**Total time: ~7-10 minutes** ⚡

---

## 🔍 Monitoring the Release

### Watch the Pipeline:

1. Go to: https://github.com/yash-chauhan-dev/datacheck/actions
2. Click on the "Release" workflow run
3. Watch each job complete in real-time

### Check Release Status:

**GitHub Release:**
- https://github.com/yash-chauhan-dev/datacheck/releases

**PyPI Package:**
- https://pypi.org/project/datacheck-cli/

**Install Test:**
```bash
pip install datacheck-cli==0.1.0
datacheck version
```

---

## 🛡️ Safety Features

The pipeline includes several safety checks:

✅ **Tests must pass** - Won't publish if tests fail
✅ **Lint must pass** - Won't publish with code quality issues
✅ **Type checking must pass** - Won't publish with type errors
✅ **Version tag required** - Only publishes on version tags (v*.*.*)
✅ **Sequential jobs** - Each step depends on previous success
✅ **Protected environments** - Can require manual approval before PyPI

---

## 🔐 Security Best Practices

### Protect Your Secrets:

1. **Never commit API tokens** to the repository
2. **Use GitHub Secrets** for sensitive values
3. **Prefer Trusted Publishing** over API tokens
4. **Rotate tokens** periodically (every 6-12 months)
5. **Use project-scoped tokens** after first release

### Environment Protection (Optional):

Add manual approval before production:

1. Go to: https://github.com/yash-chauhan-dev/datacheck/settings/environments
2. Click "New environment"
3. Name: `pypi`
4. Check "Required reviewers"
5. Add yourself as a reviewer
6. Click "Save protection rules"

Now releases to PyPI will require your approval! 🛡️

---

## 🐛 Troubleshooting

### Pipeline Fails at Test Stage

**Cause:** Tests, linting, or type checking failed

**Fix:**
```bash
# Run locally to debug
poetry run pytest
poetry run ruff check datacheck tests
poetry run mypy datacheck

# Fix issues, commit, and re-tag
git tag -d v0.1.0  # Delete local tag
git push --delete origin v0.1.0  # Delete remote tag
# Fix issues, then create tag again
```

### Pipeline Fails at PyPI Publish

**Cause:** Missing or invalid `PYPI_API_TOKEN` secret

**Fix:**
1. Regenerate PyPI token
2. Update GitHub secret
3. Re-run the workflow (don't need to re-tag)

### "Version already exists" on PyPI

**Cause:** You can't publish the same version twice

**Fix:**
```bash
# Bump to next version
# Edit pyproject.toml: version = "0.1.1"
git add pyproject.toml
git commit -m "chore: Bump version to 0.1.1"
git push origin main
git tag -a v0.1.1 -m "Release v0.1.1"
git push origin v0.1.1
```

### GitHub Release Not Created

**Cause:** Missing `GITHUB_TOKEN` permissions

**Fix:** The workflow already has correct permissions. If it still fails:
1. Check repository settings
2. Ensure Actions have write permissions
3. Re-run the workflow

---

## 📝 Pre-Release Checklist

Before pushing a release tag:

- [ ] All tests passing locally: `poetry run pytest`
- [ ] Version updated in `pyproject.toml`
- [ ] `CHANGELOG.md` updated with new version
- [ ] All changes committed and pushed to `main`
- [ ] CI is green on main branch
- [ ] Ready to publish to PyPI!

---

## 🎓 Examples

### Example 1: v0.1.0 First Release

```bash
# Update version
echo 'version = "0.1.0"' >> pyproject.toml

# Update changelog
# (Edit CHANGELOG.md to add v0.1.0 section)

# Commit and tag
git add pyproject.toml CHANGELOG.md
git commit -m "chore: Release v0.1.0"
git push origin main

git tag -a v0.1.0 -m "Release v0.1.0 - Initial public release"
git push origin v0.1.0

# Wait 7-10 minutes, then check:
# - GitHub Actions: https://github.com/yash-chauhan-dev/datacheck/actions
# - PyPI: https://pypi.org/project/datacheck-cli/0.1.0/
# - GitHub Release: https://github.com/yash-chauhan-dev/datacheck/releases/tag/v0.1.0
```

### Example 2: v0.2.0 Feature Release

```bash
# After implementing new features...

# Update version
sed -i 's/version = "0.1.0"/version = "0.2.0"/' pyproject.toml

# Update changelog
# (Add v0.2.0 section to CHANGELOG.md)

# Commit and tag
git add pyproject.toml CHANGELOG.md
git commit -m "chore: Release v0.2.0"
git push origin main

git tag -a v0.2.0 -m "Release v0.2.0 - New features"
git push origin v0.2.0

# Automated release begins!
```

### Example 3: v0.1.1 Patch Release

```bash
# After fixing bugs...

# Update version
sed -i 's/version = "0.1.0"/version = "0.1.1"/' pyproject.toml

# Update changelog
# (Add v0.1.1 section to CHANGELOG.md)

# Commit and tag
git add pyproject.toml CHANGELOG.md
git commit -m "chore: Release v0.1.1 - Bug fixes"
git push origin main

git tag -a v0.1.1 -m "Release v0.1.1 - Bug fixes"
git push origin v0.1.1
```

---

## 🔄 Release Workflow Diagram

```
┌─────────────────┐
│  Push git tag   │
│   (v0.1.0)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Test Job      │  Run tests on 3 Python versions
│  ✓ pytest       │  Lint with ruff
│  ✓ ruff         │  Type check with mypy
│  ✓ mypy         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Build Job     │  Build wheel and source dist
│  ✓ poetry build │  Upload artifacts
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Publish PyPI   │  Download artifacts
│  ✓ Upload to    │  Publish to PyPI
│     PyPI        │  
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Create Release  │  Extract changelog
│  ✓ GitHub       │  Create GitHub release
│     Release     │  Attach distributions
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Announce      │  Generate summary
│  ✓ Summary      │  Show install command
└─────────────────┘
```

---

## 🎉 Benefits of Automated Releases

✅ **Consistent** - Same process every time
✅ **Fast** - 7-10 minutes from tag to PyPI
✅ **Safe** - Tests must pass before publishing
✅ **Auditable** - Full log of every release
✅ **Repeatable** - Easy to do frequent releases
✅ **Error-free** - No manual upload mistakes
✅ **Time-saving** - Focus on code, not releases

---

## 📚 Additional Resources

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **PyPI Publishing Action**: https://github.com/pypa/gh-action-pypi-publish
- **Trusted Publishing**: https://docs.pypi.org/trusted-publishers/
- **Semantic Versioning**: https://semver.org/

---

## 🆚 Manual vs Automated Release

| Step | Manual | Automated |
|------|--------|-----------|
| Run tests | ✋ Manual | ✅ Automatic |
| Build package | ✋ `poetry build` | ✅ Automatic |
| Publish to PyPI | ✋ `poetry publish` | ✅ Automatic |
| Create GitHub release | ✋ Manual clicks | ✅ Automatic |
| Upload artifacts | ✋ Manual upload | ✅ Automatic |
| Generate changelog | ✋ Copy/paste | ✅ Automatic |
| **Time required** | **~30 minutes** | **~10 minutes** |
| **Error prone** | **Yes** | **No** |

---

## 🎯 Next Steps

1. **Choose your setup method**: API Token or Trusted Publishing
2. **Configure GitHub secrets** (if using API token)
3. **Test with v0.1.0 release**
4. **Monitor the pipeline**
5. **Enjoy automated releases!** 🚀

---

**Questions?** Open an issue: https://github.com/yash-chauhan-dev/datacheck/issues

**Happy Releasing!** 🎉
