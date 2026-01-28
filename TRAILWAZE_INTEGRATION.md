# RnDMetrics - Trailwaze Integration Guide

## Overview

**RnDMetrics** is a non-intrusive metrics collection and visualization system for the **Trailwaze** project. It extracts comprehensive development metrics without modifying any source code or project configuration.

## Integration Status

✅ **ACTIVE & LIVE**
- Source Project: Trailwaze (Project ID: 77854212)
- Metrics Dashboard: https://vic.ionascu.gitlab.io/RnDMetrics/
- Collection Frequency: Automatic on every pipeline run
- Access Level: Read-only via GitLab API

---

## What Data is Collected from Trailwaze

### 1. Commit Analytics
- **Daily Commits**: Count of commits per day over 365 days
- **Commit Messages**: Analyzed for epic/feature patterns
- **Commit Timeline**: Historical development activity
- **Collection Method**: GitLab API (read-only)

### 2. Repository Metrics
- **File Count**: Total number of files in repository
- **Lines of Code**: Total LOC across all tracked files
- **Active Branches**: Number of branches
- **Default Branch**: Current main development branch
- **Collection Method**: Repository analysis via shallow clone

### 3. Epic Tracking
- **Epic-Auth**: Commits related to authentication/login (pattern: `auth|login|oauth|sso`)
- **Epic-UI**: Commits related to UI/frontend (pattern: `ui|frontend|dashboard|chart`)
- **Collection Method**: Commit message pattern matching
- **Customizable**: Add more patterns in `config.yml`

### 4. Code Coverage (if available)
- **Line Coverage**: Test coverage percentage
- **Branch Coverage**: Branch coverage metrics
- **Collection Method**: LCOV format parsing from `lcov.info`
- **Location**: `coverage/lcov.info` or `lcov.info` in repo

### 5. Project Metadata
- **Project Name**: "trailwaze"
- **Project URL**: https://gitlab.com/vic.ionascu/trailwaze
- **Default Branch**: main
- **Last Updated**: Auto-refreshed with each collection
- **Collection Method**: GitLab API project endpoint

---

## Why This Integration is Non-Intrusive

### ✅ Zero Code Changes
- No modifications to Trailwaze source code
- No new files added to Trailwaze repository
- No branch creation or modification
- Original code remains completely untouched

### ✅ Read-Only Access
- Uses GitLab API with read-only token scopes
- `api` - API access (read)
- `read_repository` - Repository read access
- No push/write permissions granted

### ✅ No Infrastructure Changes
- No webhooks added to Trailwaze
- No runners configured in Trailwaze
- No CI/CD modifications to Trailwaze
- Trailwaze project runs independently

### ✅ Minimal Resource Impact
- Shallow clone (50 commits) for speed
- Temporary local clone (`./.tmp/repo` in RnDMetrics)
- Data stored in RnDMetrics project only
- No permanent modifications to Trailwaze

### ✅ Independent Operation
- RnDMetrics has separate CI/CD pipeline
- Separate database and storage
- Separate dashboard and UI
- Trailwaze pipelines unaffected

---

## How It Works

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    GitLab.com                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────┐    ┌──────────────────────────┐  │
│  │   Trailwaze Project  │    │  RnDMetrics Project      │  │
│  │  (Source Project)    │    │  (Metrics Collector)     │  │
│  │                      │    │                          │  │
│  ├─ source code         │    ├─ metrics collection code │  │
│  ├─ commits            │◄───┤─ analysis scripts        │  │
│  ├─ branches           │ Read└─ dashboard UI           │  │
│  ├─ coverage reports   │ Only └─ CI/CD pipeline        │  │
│  └──────────────────────┘    └──────────────────────────┘  │
│         ↑                              ↓                    │
│         └──────────────────────────────┘                   │
│         GitLab API (read-only access)                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
         ↓
    ┌────────────────┐
    │  Live Dashboard│
    │  (GitLab Pages)│
    └────────────────┘
```

### Data Collection Flow

```
1. Pipeline Trigger (automatic or manual)
   ↓
2. RnDMetrics CI/CD Pipeline Runs
   ├─ test stage: Verify metrics collection code
   ├─ collect stage:
   │  ├─ Connect to GitLab API with token
   │  ├─ Fetch project metadata
   │  ├─ Fetch commits (365 days)
   │  ├─ Clone repository (shallow, 50 commits)
   │  ├─ Analyze code metrics
   │  ├─ Check for coverage reports
   │  └─ Store snapshot in database
   ├─ build stage:
   │  ├─ Export data to JSON
   │  ├─ Generate dashboard HTML
   │  └─ Prepare for deployment
   └─ pages stage: Deploy to GitLab Pages
   ↓
3. Dashboard Live at:
   https://vic.ionascu.gitlab.io/RnDMetrics/
```

---

## Configuration

### Current Setup (RnDMetrics)

```yaml
project:
  gitlab_url: "https://gitlab.com"
  project_id: "77854212"           # Trailwaze project
  token_env: "GITLAB_TOKEN"        # Read-only token
  repo_url: "https://gitlab.com/vic.ionascu/trailwaze.git"

collection:
  since_days: 365                  # Collect 1 year of data
  shallow_clone: true              # Fast, minimal impact
  clone_depth: 50                  # 50 commits per batch
  repo_path: "./.tmp/repo"         # Temporary local path
  include_paths: ["."]             # Analyze all paths
  exclude_paths:                   # Skip these dirs
    - "node_modules"
    - "dist"
    - "build"
    - ".git"
  exclude_extensions:              # Skip these file types
    - "mbtiles"
    - "png"
    - "jpg"
    - "jpeg"
    - "gif"
    - "zip"
    - "pdf"
    - "mp4"
    - "mp3"

epics:
  rules:
    - key: "Epic-Auth"
      pattern: "auth|login|oauth|sso"
    - key: "Epic-UI"
      pattern: "ui|frontend|dashboard|chart"
```

### Customize Epic Patterns

Add more patterns to track additional features:

```yaml
epics:
  rules:
    - key: "Epic-Auth"
      pattern: "auth|login|oauth|sso"
    - key: "Epic-UI"
      pattern: "ui|frontend|dashboard|chart"
    - key: "Epic-Maps"
      pattern: "map|mapbox|trail|navigation"
    - key: "Epic-Offline"
      pattern: "offline|sync|cache"
    - key: "Epic-Mobile"
      pattern: "mobile|app|expo|react-native"
```

Then commit to RnDMetrics project:
```bash
git add config.yml
git commit -m "Add custom epic patterns for Trailwaze"
git push
```

---

## Collected Data Examples

### Latest Metrics (from latest collection)

```json
{
  "project": {
    "name": "trailwaze",
    "web_url": "https://gitlab.com/vic.ionascu/trailwaze",
    "default_branch": "main"
  },
  "snapshot_date": "2026-01-28",
  "daily_commits": {
    "2026-01-28": 2,
    "2026-01-27": 1,
    "2026-01-26": 3
  },
  "epic_commits": {
    "Epic-Auth": 5,
    "Epic-UI": 12
  },
  "repo_metrics": {
    "files": 45,
    "lines_of_code": 8234,
    "branches": 3
  },
  "coverage": {
    "line_rate": 0.75,
    "branch_rate": 0.68
  }
}
```

---

## Managing the Integration

### Running Manual Collections

Trigger a new collection manually:

```bash
# Via GitLab Web UI:
GitLab → RnDMetrics → CI/CD → Pipelines → Run Pipeline

# Via API:
curl -X POST \
  -H "PRIVATE-TOKEN: your-token" \
  https://gitlab.com/api/v4/projects/78050938/pipeline \
  -d "ref=main"
```

### Viewing Collection Results

1. **Dashboard**: https://vic.ionascu.gitlab.io/RnDMetrics/
2. **Pipeline Logs**: https://gitlab.com/vic.ionascu/RnDMetrics/-/pipelines
3. **JSON Data**: https://vic.ionascu.gitlab.io/RnDMetrics/data/latest.json

### Scheduling Automated Collections

Set up daily metrics collection:

1. Go to RnDMetrics project
2. Navigate to: **CI/CD → Schedules**
3. Click: **New schedule**
4. Configure:
   - Description: "Daily Trailwaze metrics collection"
   - Cron: `0 2 * * *` (2 AM daily)
   - Timezone: Your timezone
   - Target branch: `main`
5. Click: **Create pipeline schedule**

---

## Data Security & Privacy

### What is NOT Collected
- ❌ Sensitive credentials (API keys, tokens)
- ❌ Personal data from commit metadata
- ❌ Private file contents
- ❌ Build artifacts or binaries
- ❌ Configuration secrets

### What IS Protected
- ✅ Token stored as masked CI/CD variable
- ✅ Database isolated in RnDMetrics project
- ✅ Read-only API permissions
- ✅ No data modifications in Trailwaze
- ✅ Dashboard accessible based on project visibility

### Access Control

- **RnDMetrics Token**: `GITLAB_TOKEN` in project variables
  - Scopes: `api`, `read_repository`
  - Protected: Yes (only on protected branches)
  - Masked: Yes (hidden in logs)

---

## Troubleshooting

### No Data Showing in Dashboard

**Check 1**: Verify pipeline ran successfully
```
GitLab → RnDMetrics → CI/CD → Pipelines
```

**Check 2**: Verify data files exist
```
https://vic.ionascu.gitlab.io/RnDMetrics/data/latest.json
```

**Check 3**: Check collection logs
```
GitLab → RnDMetrics → CI/CD → Pipelines → Click pipeline → View logs
```

### Pipeline Fails at Collect Stage

**Solution 1**: Verify token has correct permissions
- Token needs: `api` + `read_repository` scopes

**Solution 2**: Verify Trailwaze project is accessible
```bash
curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  https://gitlab.com/api/v4/projects/77854212
```

**Solution 3**: Check project configuration
```
RnDMetrics → config.yml → project_id must be "77854212"
```

---

## Advanced Configuration

### Monitoring Different Timeframes

Change collection window:

```yaml
collection:
  since_days: 90   # Monitor last 90 days instead of 365
```

### Performance Tuning

For faster collection:

```yaml
collection:
  since_days: 30         # Shorter period
  shallow_clone: true    # Already enabled
  clone_depth: 25        # Reduce commits per batch
  exclude_paths:
    - "node_modules"
    - "dist"
    - ".git"
    - "vendor"           # Add more exclusions
```

### Custom Retention Policy

Keep metrics for specific period:

```yaml
retention:
  days: 180   # Delete snapshots older than 180 days
```

---

## Comparison: Intrusive vs Non-Intrusive

| Aspect | Non-Intrusive (Current) | Intrusive (Not Used) |
|--------|------------------------|------------------|
| Code Changes | None | Modified source |
| Trailwaze Config | Unchanged | Updated .gitlab-ci.yml |
| Webhooks | None | Added to Trailwaze |
| Runners | Separate project | Added to Trailwaze |
| Database | RnDMetrics only | Shared/Trailwaze |
| Pipeline Impact | Independent | Affects Trailwaze |
| Maintenance | Simple | Complex |
| Risk Level | None | Moderate |

---

## Benefits of This Setup

✅ **Zero Risk**: No changes to production code
✅ **Independent**: RnDMetrics works regardless of Trailwaze status
✅ **Scalable**: Can add other projects without modifying them
✅ **Maintainable**: All configuration in one place (RnDMetrics)
✅ **Auditable**: All collection logged separately
✅ **Portable**: Can be used with any GitLab project
✅ **Non-Breaking**: Trailwaze development continues normally

---

## Next Steps

1. **View Dashboard**
   - https://vic.ionascu.gitlab.io/RnDMetrics/

2. **Customize Metrics**
   - Edit `config.yml` to add epic patterns
   - Push to trigger new collection

3. **Schedule Collections**
   - Setup daily/weekly automated runs
   - Monitor trends over time

4. **Integrate with Tools**
   - Use JSON exports for custom analysis
   - Build reports from the data

5. **Expand Monitoring**
   - Add other projects using same pattern
   - Create centralized metrics hub

---

## Support

- **Documentation**: [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)
- **User Guide**: [USER_GUIDE.md](USER_GUIDE.md)
- **Integration Guide**: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
- **Dashboard**: https://vic.ionascu.gitlab.io/RnDMetrics/
- **Project**: https://gitlab.com/vic.ionascu/RnDMetrics

---

## Summary

RnDMetrics provides **non-intrusive metrics collection** for Trailwaze through:

- **Read-only GitLab API access** (no code modifications)
- **Separate CI/CD infrastructure** (independent operation)
- **Automatic data collection** (scheduled pipeline runs)
- **Beautiful dashboard** (visual metrics representation)
- **Extensible design** (add more projects easily)

**Trailwaze development continues completely unaffected while you get comprehensive metrics and insights!** 📊
