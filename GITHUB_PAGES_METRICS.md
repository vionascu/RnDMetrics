# Evidence-Backed Metrics Dashboard on GitHub Pages

Your evidence-backed metrics system is now set up to automatically collect metrics and deploy to GitHub Pages.

## 🚀 Quick Start

### Access the Dashboard
After metrics collection completes, your dashboard is available at:

**📊 Main Dashboard:** https://vionascu.github.io/RnDMetrics/

This link will have:
- Real-time metrics data from your repositories
- Complete evidence trails for every metric
- Professional glassmorphism UI design
- Links to methodology documentation

### Manual Trigger Metrics Collection

To run metrics collection manually:

1. Go to: https://github.com/vionascu/RnDMetrics/actions
2. Click **"Collect Metrics & Deploy Dashboard"** workflow
3. Click **"Run workflow"** button
4. Select branch: **main**
5. Click **"Run workflow"**
6. Wait for workflow to complete (5-10 minutes)
7. Dashboard updates automatically at: https://vionascu.github.io/RnDMetrics/

### Automatic Schedule

Metrics are collected automatically:
- **Frequency:** Daily at 2 AM UTC
- **Time Range:** Last 30 days
- **Next Run:** Check GitHub Actions tab

To modify schedule, edit [.github/workflows/metrics.yml](.github/workflows/metrics.yml):
```yaml
schedule:
  - cron: '0 2 * * *'  # Change this line
```

## 📊 What Gets Deployed

### Dashboard HTML
- **Location:** `public/index.html`
- **URL:** https://vionascu.github.io/RnDMetrics/
- Generated from `build_dashboard.sh`
- Shows all metrics with evidence trails

### Metrics Data
- **Manifest:** `public/data/manifest.json` - Complete evidence trail
- **Raw Metrics:** `public/data/*_count.json`, `*_stats.json`, etc.
- **Derived Metrics:** `public/data/*_derived.json` - Normalized metrics

### Documentation
- **Methodology:** `public/docs/METHODOLOGY.md` - Formulas and calculations
- **System Guide:** `public/README_METRICS_SYSTEM.md` - How the system works

## 🔄 Workflow Pipeline

```
1. GitHub Actions Triggers (Daily at 2 AM UTC)
         ↓
2. Collect Metrics (collect_metrics.py)
   ├── Git: commits, LOC changes
   ├── Tests: JUnit XML parsing
   ├── Coverage: Jacoco/Cobertura/LCOV
   └── Docs: Language-specific scanning
         ↓
3. Compute Derived Metrics (compute_derived.py)
   ├── Activity: commits/day
   ├── Quality: pass rates, coverage adequacy
   └── Velocity: churn ratio, files/commit
         ↓
4. Validate Quality Gates (quality_gate.py)
   ├── Evidence Completeness ✓
   ├── Sanity Checks ✓
   └── Determinism Validation
         ↓
5. Build Dashboard (build_dashboard.sh)
   └── Generate HTML from metrics
         ↓
6. Deploy to GitHub Pages
   └── Available at: https://vionascu.github.io/RnDMetrics/
```

## 📁 Output Structure

```
artifacts/
├── raw/                           # Raw collected data
│   ├── TrailEquip_commits_count.json
│   ├── TrailEquip_diffs_stats.json
│   ├── TrailWaze_tests_summary.json
│   ├── TrailWaze_coverage_summary.json
│   └── RnDMetrics_docs_coverage.json
├── derived/                       # Computed normalized metrics
│   ├── activity_derived.json     # commits_per_day
│   ├── quality_derived.json      # pass rates, coverage
│   ├── velocity_derived.json     # churn, LOC, files/commit
│   └── derived_manifest.json
└── manifest.json                 # Complete evidence trail
```

## 🔒 Evidence & Reproducibility

Every metric includes complete evidence:

```json
{
  "metric_id": "TrailEquip/commits.count",
  "source": {"type": "git"},
  "commands": ["git log --since=2026-01-01 --until=2026-01-31 --format=%H"],
  "raw_file": "artifacts/raw/TrailEquip_commits_count.json",
  "raw_file_hash": "abc123...",
  "collected_at": "2026-01-31T10:30:00+00:00"
}
```

To verify any metric manually:

```bash
# 1. Find metric in manifest
cat artifacts/manifest.json | jq '.evidence_map.["TrailEquip/commits.count"]'

# 2. Get the command
"git log --since=2026-01-01 --until=2026-01-31 --format=%H"

# 3. Run it
cd ../TrailEquip
git log --since=2026-01-01 --until=2026-01-31 --format=%H | wc -l

# 4. Should match reported value ✓
```

## 🎯 Metrics at a Glance

### Git Metrics
- `commits.count` - Total commits in range
- `diffs.loc_added` - Lines added
- `diffs.loc_deleted` - Lines deleted
- `diffs.files_changed` - Files modified

### Quality Metrics
- `tests.pass_rate` - Test success percentage
- `coverage.line_percent` - Line coverage %
- `docs.coverage_percent` - Documentation %

### Velocity Metrics
- `activity.commits_per_day` - Commit frequency
- `velocity.loc_net` - Net code change
- `velocity.churn_ratio` - Refactoring ratio
- `velocity.files_per_commit` - Commit scope

## 📖 Documentation

- **[METHODOLOGY.md](Documents/METHODOLOGY.md)** - Complete formula reference
- **[README_METRICS_SYSTEM.md](README_METRICS_SYSTEM.md)** - System overview
- **[config/repos.yaml](config/repos.yaml)** - Repository configuration

## 🧪 Local Testing

To test metrics collection locally:

```bash
# Collect metrics
./run_metrics.sh --range last_30_days

# Build dashboard
./build_dashboard.sh

# View dashboard
open public/index.html

# Run tests
./run_tests.sh
```

## 🔧 Configuration

### Time Ranges Available
- `last_30_days` - Past 30 days (default)
- `last_90_days` - Past 90 days
- `ytd` - Year to date
- `all_2024` - All of 2024
- `all_2025` - All of 2025
- `custom --from DATE --to DATE` - Custom range

### Modify Collection Schedule
Edit [.github/workflows/metrics.yml](.github/workflows/metrics.yml):

```yaml
schedule:
  - cron: '0 2 * * *'  # Daily at 2 AM UTC
  # Every 6 hours: cron: '0 */6 * * *'
  # Every 4 hours: cron: '0 */4 * * *'
  # Weekly Monday 9 AM: cron: '0 9 * * 1'
```

### Add CI Artifacts

To enable test/coverage metrics:

1. Configure `ci_artifacts_path` in [config/repos.yaml](config/repos.yaml)
2. Ensure CI publishes JUnit XML and coverage reports
3. Re-run workflow: metrics will auto-detect artifacts

```yaml
repos:
  - name: TrailEquip
    ci_artifacts_path: ../ci_artifacts/TrailEquip  # Point to CI outputs
```

## 🚨 Troubleshooting

### Dashboard shows 404
- Check GitHub Pages is enabled:
  - Settings → Pages → Source: "Deploy from GitHub Actions"
- Wait 2-3 minutes after workflow completes
- Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

### Workflow shows failed status
1. Go to: https://github.com/vionascu/RnDMetrics/actions
2. Click failed workflow run
3. Expand log section to see errors
4. Common issues:
   - Missing repos (update config/repos.yaml)
   - Missing pyyaml (auto-installed)
   - Git permission issues

### No metrics collected
- Check repo paths in [config/repos.yaml](config/repos.yaml)
- Verify repos have git history in the date range
- Ensure repos are accessible on local machine

## 📊 Dashboard URL

Your dashboard is live at:

### 🎯 **https://vionascu.github.io/RnDMetrics/**

Share this link with your team!

## ✨ Features

✅ Real-time metrics from your repositories
✅ Complete evidence trail for every metric
✅ Professional UI with glassmorphism design
✅ Fully transparent calculations
✅ Automatic daily updates
✅ Zero cost (uses GitHub Actions free tier)
✅ No servers to manage
✅ 100% version controlled

## 📞 Support

For questions:
- See [METHODOLOGY.md](Documents/METHODOLOGY.md) for metric definitions
- Check [README_METRICS_SYSTEM.md](README_METRICS_SYSTEM.md) for system overview
- Review workflow logs: https://github.com/vionascu/RnDMetrics/actions

---

**Status:** ✅ Production Ready

**Dashboard:** https://vionascu.github.io/RnDMetrics/

**Last Updated:** January 31, 2026
