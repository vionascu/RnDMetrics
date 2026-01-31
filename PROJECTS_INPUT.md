# Projects Input Configuration

This document explains how to add projects for metrics analysis.

## How It Works

1. **Edit `projects.json`** - Add GitHub project URLs
2. **Run `./run_metrics.sh`** - Automatically clones repos and collects metrics
3. **View dashboard** - Results appear at https://vionascu.github.io/RnDMetrics/

## Edit projects.json

Open `projects.json` and add your GitHub projects:

```json
{
  "projects": [
    {
      "url": "https://github.com/vionascu/trailwaze",
      "language": "mixed",
      "description": "Trail navigation mobile/web app (React Native/React)"
    },
    {
      "url": "https://github.com/vionascu/trail-equip",
      "language": "java",
      "description": "Trail equipment recommendation system (microservices, Java/Spring)"
    }
  ]
}
```

### Fields

- **url** (required): Full GitHub URL (https://github.com/owner/repo)
- **language** (optional): Code language - `java`, `python`, `javascript`, `mixed`, etc.
- **description** (optional): Project description

## Workflow

```bash
# 1. Edit projects.json to add new projects

# 2. Run metrics collection
./run_metrics.sh --range last_30_days

# This automatically:
# - Reads projects.json
# - Clones any missing repositories
# - Generates config/repos.yaml
# - Collects git metrics (commits, LOC, files)
# - Collects test metrics (if present)
# - Collects coverage metrics (if present)
# - Computes derived metrics
# - Builds interactive dashboard
```

## Current Projects

The system currently analyzes:
1. **Trailwaze** - Trail navigation mobile/web app
2. **Trail-Equip** - Trail equipment recommendation system

## Adding More Projects

Simply add to `projects.json`:

```json
{
  "url": "https://github.com/username/new-project",
  "language": "python",
  "description": "My Python project"
}
```

Then run `./run_metrics.sh` again.

## Dashboard Features

After running metrics collection:

- **Date Range Selector**: Filter metrics by time period
- **Project Selector**: View individual projects or combined metrics
- **Dynamic Graphs**:
  - Daily Commits Trend
  - Lines of Code Over Time
- **Evidence Trails**: All metrics show calculation and source data

## Time Range Options

```bash
./run_metrics.sh --range last_30_days   # Last 30 days (default)
./run_metrics.sh --range last_90_days   # Last 90 days
./run_metrics.sh --range ytd            # Year to date
./run_metrics.sh --range all_2024       # All of 2024
./run_metrics.sh --range all_2025       # All of 2025
./run_metrics.sh --range custom --from 2026-01-01 --to 2026-01-31  # Custom range
```

## Architecture

```
projects.json
    ↓
scripts/setup_projects.py (clones repos, generates config)
    ↓
config/repos.yaml (auto-generated, DO NOT EDIT)
    ↓
scripts/collect_metrics.py (collects from repos)
    ↓
artifacts/
    ├── raw/          (raw metric data)
    ├── derived/      (computed metrics)
    └── manifest.json (metadata)
    ↓
public/index.html (interactive dashboard)
```

## No Guessing Policy

✅ All metrics are evidence-backed
✅ Every number traced to source
✅ Calculation formulas shown in dashboard
✅ Source data stored in artifacts/
