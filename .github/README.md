# GitHub Actions & CI/CD Configuration

This directory contains all GitHub Actions workflows and configuration files for automating RnDMetrics dashboard deployment and metrics collection.

## Workflows

### 1. `metrics.yml` - Daily Metrics Collection & Dashboard Deployment
**Trigger:** Daily at 2 AM UTC (or manual via `workflow_dispatch`)

**Jobs:**
- **collect-metrics:** Runs metrics collection from GitHub API
  - Collects commit history and code metrics
  - Exports data to `output/latest.json`
  - Generates metrics artifacts

- **deploy-dashboard:** Builds and deploys to GitHub Pages
  - Copies dashboard HTML files to public directory
  - Includes metrics data and documentation
  - Deploys to `https://vionascu.github.io/RnDMetrics/`

- **notify-completion:** Sends completion status notification

**Environment Variables:**
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions

### 2. `pages-build-deployment.yml` - Push-Triggered Pages Deployment
**Trigger:** Push to `main` branch with changes to docs or workflows

**Jobs:**
- **build:** Prepares dashboard files and documentation
- **deploy:** Deploys to GitHub Pages

## Configuration Files

### `CODEOWNERS`
Defines code ownership and review requirements:
- `@vionascu` owns all code by default
- Documentation and workflows require review from code owner

### `pages-config.yml`
GitHub Pages configuration for Jekyll build (disabled for custom HTML):
- No theme (using custom HTML dashboards)
- Specifies build settings and file exclusions

## Setting Up CI/CD

### 1. Enable GitHub Pages
1. Go to **Settings** → **Pages**
2. Select **Deploy from a branch** or **GitHub Actions**
3. For branch method: Select `gh-pages` branch (auto-created by workflows)
4. Save

### 2. Configure Secrets (if needed)
If using personal GitHub token:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add `GITHUB_TOKEN` secret (optional - auto-provided)

### 3. Enable Workflows
1. Go to **Actions** tab
2. Workflows should be auto-enabled
3. Can manually run via **Run workflow** button

## Dashboard Access

After first deployment, dashboards are available at:
- **Main Dashboard:** `https://vionascu.github.io/RnDMetrics/`
- **Executive Dashboard:** `https://vionascu.github.io/RnDMetrics/executive.html`

## Monitoring Deployments

### View Workflow Status
1. Go to **Actions** tab
2. Check for:
   - Green checkmarks (success) ✅
   - Red X marks (failure) ❌
   - Orange dots (in progress) ⏳

### Troubleshooting
If deployment fails:
1. Click workflow run name
2. Review logs in each job
3. Check for errors related to:
   - File permissions
   - Missing dependencies
   - Path issues

## Manual Triggers

To manually run metrics collection:
1. Go to **Actions** tab
2. Select **"Collect Metrics & Deploy Dashboard"**
3. Click **Run workflow** → **Run workflow**

## Integration with External Workflows

These workflows can be called from other repositories:
- Trigger external repo tests before metrics collection
- Update cross-project metrics
- Generate comparative reports

## Scheduled Workflow Examples

Current schedule: **Daily at 2 AM UTC**
```
0 2 * * *
```

Other common schedules:
- Every 6 hours: `0 */6 * * *`
- Weekly (Monday 9 AM): `0 9 * * 1`
- Twice daily: `0 2,14 * * *`

To change schedule, edit `metrics.yml` line with cron expression.

## Performance & Limits

GitHub Actions free tier includes:
- 2,000 free minutes per month
- Each workflow run counted in minutes
- Estimated per-run time: 5-10 minutes

For high-frequency updates, consider:
- Increasing cron interval
- Running only on repository changes
- Using `workflow_dispatch` for manual runs

## Security Considerations

✅ **Good Practices Implemented:**
- Uses GITHUB_TOKEN (auto-scoped)
- No sensitive credentials in workflows
- Read-only operations for metrics collection
- Deployment restricted to main branch

🔒 **Recommendations:**
- Keep workflows up-to-date
- Review workflow changes in pull requests
- Monitor for unexpected job failures
- Use branch protection on main

---

**Last Updated:** January 31, 2026
**Maintained by:** vionascu
