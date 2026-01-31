# Multi-Project Metrics Setup Guide

**Document:** Setup and Integration Guide for TrailEquip, TrailWaze, and RnDMetrics
**Date:** January 31, 2026
**Version:** 1.0.0

---

## Overview

This guide walks you through setting up and configuring the RnDMetrics system to collect and visualize metrics from multiple external repositories (TrailEquip and TrailWaze) alongside RnDMetrics itself.

---

## Prerequisites

Before starting, ensure you have:

- ✅ **Python 3.9+** - Check with: `python3 --version`
- ✅ **Git** - Check with: `git --version`
- ✅ **pip** - Check with: `pip3 --version`
- ✅ **GitHub Account** - With API access
- ✅ **GitHub Personal Access Token** - With `repo` and `read:org` scopes

### Getting Your GitHub Token

1. Log in to GitHub (github.com)
2. Click your avatar → **Settings** → **Developer settings** → **Personal access tokens**
3. Create a new token (classic) with scopes:
   - `repo` - Full control of private repositories
   - `read:org` - Read organization data
4. Copy the token (you won't see it again)

---

## Step 1: Clone/Navigate to RnDMetrics

```bash
# If not already there
cd /Users/viionascu/Projects/RnDMetrics
```

---

## Step 2: Create Configuration File

Copy the example configuration:

```bash
cp config.example.yml config.yml
```

### Edit config.yml

Open `config.yml` and update with the following template for all three projects:

```yaml
# ─────────────────────────────────────────────────────────────
# Multi-Project Configuration for RnDMetrics
# ─────────────────────────────────────────────────────────────

# Project Configuration
# Note: Add each project you want to track

projects:
  # Project 1: TrailEquip (Java Microservices)
  - name: trailequip
    github_url: "https://github.com"
    project_id: YOUR_TRAILEQUIP_PROJECT_ID
    token_env: "GITHUB_TOKEN"
    repo_url: "https://github.com/vionascu/trail-equip.git"

    collection:
      since_days: 365
      shallow_clone: true
      clone_depth: 50
      repo_path: "./.tmp/repo-trailequip"
      include_paths: ["."]
      exclude_paths:
        - "node_modules"
        - ".git"
        - "dist"
        - "build"
        - "target"
        - ".gradle"

    epics:
      rules:
        - key: "Trail-Service"
          pattern: "trail|hiking|geo"
        - key: "Weather-Service"
          pattern: "weather|forecast|climate"
        - key: "Recommendation"
          pattern: "recommend|equipment|gear"
        - key: "Bug-Fix"
          pattern: "fix|bug|hotfix|patch"
        - key: "Feature"
          pattern: "feat|feature|add|implement"

  # Project 2: TrailWaze (React Full-Stack)
  - name: trailwaze
    github_url: "https://github.com"
    project_id: YOUR_TRAILWAZE_PROJECT_ID
    token_env: "GITHUB_TOKEN"
    repo_url: "https://github.com/vionascu/trailwaze.git"

    collection:
      since_days: 365
      shallow_clone: true
      clone_depth: 50
      repo_path: "./.tmp/repo-trailwaze"
      include_paths: ["."]
      exclude_paths:
        - "node_modules"
        - ".git"
        - "dist"
        - "build"
        - "coverage"
        - ".cache"

    epics:
      rules:
        - key: "Web-App"
          pattern: "web|react|frontend|ui"
        - key: "Mobile-App"
          pattern: "mobile|native|app"
        - key: "API"
          pattern: "api|endpoint|backend"
        - key: "Test"
          pattern: "test|spec|coverage"
        - key: "Documentation"
          pattern: "doc|readme|guide"

  # Project 3: RnDMetrics (Python Metrics)
  - name: rndmetrics
    github_url: "https://github.com"
    project_id: YOUR_RNDMETRICS_PROJECT_ID
    token_env: "GITHUB_TOKEN"
    repo_url: ""  # Current repo, leave empty

    collection:
      since_days: 365
      shallow_clone: true
      clone_depth: 50
      repo_path: "."
      include_paths: ["."]
      exclude_paths:
        - "node_modules"
        - ".git"
        - "data"
        - "output"
        - "public"

    epics:
      rules:
        - key: "Collector"
          pattern: "collector|collection|gather"
        - key: "Storage"
          pattern: "storage|database|db"
        - key: "Export"
          pattern: "export|json|output"
        - key: "Dashboard"
          pattern: "dashboard|ui|frontend|app"

# Data Retention Policy
retention:
  days: 365

# Export Settings
export:
  output_dir: "./output"
  public_dir: "./public"

# UI Settings
ui:
  title: "Multi-Project Metrics Dashboard"
  theme: "dark"

# Storage Settings
storage:
  db_path: "./data/metrics.db"
  schema_path: "./sql/schema.sql"
```

---

## Step 3: Configure Project Information

For each GitHub repository, gather the owner and repository name:

### For TrailEquip:
1. Go to: https://github.com/vionascu/trail-equip
2. Owner: `vionascu`
3. Repository: `trail-equip`
4. Update config: `owner: "vionascu"` and `repo: "trail-equip"`

### For TrailWaze:
1. Go to: https://github.com/vionascu/trailwaze
2. Owner: `vionascu`
3. Repository: `trailwaze`
4. Update config: `owner: "vionascu"` and `repo: "trailwaze"`

### For RnDMetrics:
1. Go to: https://github.com/vionascu/RnDMetrics
2. Owner: `vionascu`
3. Repository: `RnDMetrics`
4. Copy → Update `YOUR_RNDMETRICS_PROJECT_ID`

---

## Step 4: Set GitHub Token

```bash
# Export your GitHub token
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxx"

# Verify it's set
echo $GITLAB_TOKEN
```

**For permanent setup** (optional):

Add to your shell profile (`~/.zshrc` or `~/.bash_profile`):

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxx"
```

Then reload:
```bash
source ~/.zshrc  # or ~/.bash_profile
```

---

## Step 5: Install Dependencies

```bash
# Ensure you're in RnDMetrics directory
cd /Users/viionascu/Projects/RnDMetrics

# Install Python dependencies
pip install -r requirements.txt
```

---

## Step 6: Initialize Database

```bash
./scripts/metrics init --config config.yml
```

This creates:
- `data/metrics.db` - SQLite database
- Database schema for storing metrics

---

## Step 7: Collect Metrics

### First Collection (Initial Data)

```bash
./scripts/metrics collect --config config.yml
```

This will:
1. Connect to GitHub API for each project
2. Fetch all commits from the past 365 days
3. Clone each repository
4. Analyze code structure
5. Calculate metrics
6. Store snapshots in database

**Expected output:**
```
Collecting metrics for: trailequip
  ✓ Fetched project info
  ✓ Listed commits (123 commits found)
  ✓ Cloned repository
  ✓ Analyzed repository
  ✓ Stored snapshot

Collecting metrics for: trailwaze
  ✓ Fetched project info
  ✓ Listed commits (456 commits found)
  ✓ Cloned repository
  ✓ Analyzed repository
  ✓ Stored snapshot

Collecting metrics for: rndmetrics
  ✓ Fetched project info
  ✓ Listed commits (78 commits found)
  ✓ Analyzed repository
  ✓ Stored snapshot
```

---

## Step 8: Export Metrics

```bash
./scripts/metrics export --config config.yml
```

This creates:
- `output/latest.json` - Most recent metrics
- `output/history.json` - All historical data

---

## Step 9: Build Dashboard

```bash
./scripts/metrics build-dashboard --config config.yml
```

This prepares:
- `public/` - Deployable dashboard files
- All necessary assets and data

---

## Step 10: Run Complete Workflow (Recommended)

All steps in one command:

```bash
./scripts/metrics run --config config.yml
```

Equivalent to: `collect` → `export` → `build-dashboard`

---

## Step 11: View Dashboard

### Local Viewing (Development)

```bash
python3 -m http.server 8000 --directory public
```

Then open: **http://localhost:8000**

### Deployment to GitHub Pages

The `.github/workflows/metrics.yml` pipeline automatically:
1. Runs metrics collection
2. Exports data
3. Builds dashboard
4. Publishes to GitHub Pages

Dashboard URL will be: `https://vionascu.github.io/RnDMetrics/`

---

## Using the Project Selector

### Access the Selector

The project selector is available on the dashboard:

1. Look for **"Project Selector"** panel
2. Find the project checkboxes:
   - ☑ TrailEquip
   - ☑ TrailWaze
   - ☑ RnDMetrics

### Selection Modes

**Mode 1: Single Project**
- Select one project
- View detailed metrics
- Full analytics for that project

**Mode 2: Multiple Projects**
- Select 2-3 projects
- Compare metrics side-by-side
- Identify trends

**Mode 3: All Projects**
- Select all projects
- Aggregated view
- Team-wide metrics

### Using Selectors

1. Click project checkboxes to select/deselect
2. Choose view mode (Single, Multiple, All)
3. Click **"Apply Selection"**
4. Dashboard updates with filtered metrics

---

## Metrics Available

### All Projects Track

- **Daily Commits** - Per day over 365 days
- **Epic Distribution** - By feature/category
- **Lines of Code** - Total LOC in repository
- **File Count** - Total files
- **Branch Count** - Active branches
- **Code Coverage** - Line and branch coverage

### TrailEquip Specific

- Service-level metrics (Trail, Weather, Recommendation)
- API test coverage (23 tests)
- Performance metrics

### TrailWaze Specific

- Application metrics (Web, Mobile, Shared)
- Component coverage
- Test suite metrics (150+ tests)

### RnDMetrics Specific

- Collector metrics
- Database metrics
- Dashboard metrics
- API metrics

---

## Scheduling Automatic Collection

### Using cron (Linux/Mac)

Edit your crontab:
```bash
crontab -e
```

Add a daily collection at 2 AM:
```bash
0 2 * * * cd /Users/viionascu/Projects/RnDMetrics && GITHUB_TOKEN=ghp_xxx ./scripts/metrics run --config config.yml
```

### Using GitHub Actions

The `.github/workflows/metrics.yml` includes a scheduled workflow:

```yaml
name: Collect Metrics
on:
  schedule:
    - cron: '0 2 * * *'
jobs:
  metrics:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: ./scripts/metrics run --config config.yml
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Configure in GitHub: **Settings** → **Secrets and variables** → **Actions** → Add `GITHUB_TOKEN`

---

## Troubleshooting

### Issue: "Missing GitHub token"

**Solution:**
```bash
export GITHUB_TOKEN="your-token"
./scripts/metrics run --config config.yml
```

### Issue: "Project not found"

**Solution:**
1. Verify project ID in `config.yml`
2. Check token has `api` scope
3. Ensure you have access to the project

### Issue: "Connection timed out"

**Solution:**
1. Check internet connection
2. Verify GitHub is accessible
3. Try again in a few minutes
4. Check GitHub status: https://status.github.com

### Issue: Collection is very slow

**Solution:**
Enable shallow clone in `config.yml`:
```yaml
collection:
  shallow_clone: true
  clone_depth: 50
```

### Issue: No data in dashboard

**Solution:**
1. Run: `./scripts/metrics collect`
2. Check: `cat output/latest.json`
3. Verify: Browser console for JS errors

---

## Maintenance

### Regular Tasks

**Daily:**
- Automatic collection (via cron/CI/CD)
- Dashboard available
- Historical data accumulating

**Weekly:**
- Review metrics trends
- Check for anomalies
- Export reports if needed

**Monthly:**
- Archive old data (optional)
- Review retention policy
- Update documentation

### Database Maintenance

**View database info:**
```bash
sqlite3 data/metrics.db ".schema"
sqlite3 data/metrics.db "SELECT COUNT(*) FROM snapshots;"
```

**Backup database:**
```bash
cp data/metrics.db data/metrics.backup.db
```

**Reset database:**
```bash
rm data/metrics.db
./scripts/metrics init --config config.yml
```

---

## Performance Tips

### Optimize Collection Speed

1. **Use shallow clone:**
   ```yaml
   collection:
     shallow_clone: true
     clone_depth: 50
   ```

2. **Exclude large directories:**
   ```yaml
   exclude_paths:
     - "node_modules"
     - ".git"
     - "vendor"
     - "dist"
   ```

3. **Filter by paths:**
   ```yaml
   include_paths:
     - "src"
     - "app"
   ```

### Optimize Dashboard

1. **Limit historical data:**
   ```yaml
   retention:
     days: 180  # Keep 6 months instead of 365
   ```

2. **Compress JSON exports:**
   ```bash
   gzip output/history.json
   ```

---

## Next Steps

1. ✅ **Setup Complete** - Configuration done
2. 📊 **First Collection** - Run initial metrics collection
3. 📈 **View Dashboard** - Access metrics visualization
4. 🔄 **Schedule Automation** - Set up daily collection
5. 📚 **Documentation** - Read detailed guides in `/docs`

---

## Resources

### Documentation Files

- [External Repositories Overview](EXTERNAL_REPOS.md)
- [Test Metrics Report](TEST_METRICS_REPORT.md)
- [TrailEquip Tests](external-repos/TRAILEQUIP_TESTS.md)
- [TrailWaze Tests](external-repos/TRAILWAZE_TESTS.md)
- [Main User Guide](../USER_GUIDE.md)
- [Integration Guide](../INTEGRATION_GUIDE.md)

### External Repositories

- [TrailEquip](https://github.com/vionascu/trail-equip)
- [TrailWaze](https://github.com/vionascu/trailwaze)

### Commands Reference

```bash
# Initialize
./scripts/metrics init --config config.yml

# Collect metrics
./scripts/metrics collect --config config.yml

# Export data
./scripts/metrics export --config config.yml

# Build dashboard
./scripts/metrics build-dashboard --config config.yml

# Run all
./scripts/metrics run --config config.yml

# View dashboard
python3 -m http.server 8000 --directory public

# Run tests
pytest tests/ -v

# View database
sqlite3 data/metrics.db
```

---

## Support

For help:
1. Check [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)
2. Review documentation in `/docs`
3. Check console output for error messages
4. Verify configuration in `config.yml`

---

**Document Version:** 1.0.0
**Last Updated:** January 31, 2026
**Status:** Complete
