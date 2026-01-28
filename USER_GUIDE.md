# RnDMetrics - User Guide

## Overview

RnDMetrics is a comprehensive GitLab analytics system that automatically collects metrics from your GitLab projects and displays them in an interactive dashboard. It tracks commits, code quality, coverage metrics, and custom epics over time.

### What RnDMetrics Does

- **Collects metrics** from your GitLab project daily (commits, branches, coverage)
- **Tracks epics** based on commit message patterns you define
- **Stores data** in a local SQLite database with configurable retention
- **Exports data** as JSON for easy integration
- **Displays metrics** in a static web dashboard

### What You Get

- 📊 **Interactive Dashboard** - Real-time visualization of your project metrics
- 📈 **Historical Data** - Track metrics over time (1 year by default)
- 📋 **JSON Exports** - Machine-readable data exports for custom analysis
- 🔒 **Privacy** - All data stays local, read-only access to GitLab

---

## Getting Started

### Prerequisites

- Python 3.9+
- GitLab account with a project
- GitLab personal access token (with `api` and `read_repository` scopes)
- Git installed

### Step 1: Prepare Your GitLab Token

1. Go to GitLab: **Settings → Access Tokens**
2. Create a new token with:
   - Name: `trailwaze-metrics-token`
   - Scopes: `api`, `read_repository`
   - Expiration: Set a date (recommended)
3. Copy the token immediately (you won't see it again)
4. Store it temporarily

### Step 2: Clone or Download Trailwaze Metrics

```bash
git clone <trailwaze-metrics-repo-url>
cd trailwaze-metrics
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure for Your Project

```bash
cp config.example.yml config.yml
```

Edit `config.yml` with your project details:

```yaml
project:
  gitlab_url: "https://gitlab.com"      # Your GitLab instance URL
  project_id: "YOUR_PROJECT_ID"          # Find in project Settings → General
  token_env: "GITLAB_TOKEN"              # Environment variable name
  repo_url: ""                           # Leave empty for auto-detection

collection:
  since_days: 365                        # How far back to collect metrics
  repo_path: "./.tmp/repo"               # Where to clone the repo
  shallow_clone: true                    # Use shallow clone (faster)
  clone_depth: 50                        # Commits to clone per batch
  include_paths: ["."]                   # Paths to analyze
  exclude_paths: ["node_modules", ".git"] # Paths to skip
  exclude_extensions: ["png", "jpg", "pdf"] # File types to skip

epics:                                   # Track commits by pattern
  rules:
    - key: "Epic-Auth"
      pattern: "auth|login|oauth"
    - key: "Epic-UI"
      pattern: "ui|frontend|dashboard"

retention:
  days: 365                              # Keep metrics for 1 year

ui:
  title: "My Project Metrics"            # Dashboard title
  theme: "dark"                          # Theme: dark or light
```

### Step 5: Set Your GitLab Token

Before running, set the GitLab token as an environment variable:

```bash
export GITLAB_TOKEN="your-token-here"
```

### Step 6: Run the Metrics Collection

```bash
./scripts/metrics run --config config.yml
```

This command:
1. Collects metrics from your GitLab project
2. Stores them in the database
3. Exports data as JSON
4. Builds the dashboard

### Step 7: View Your Dashboard

The dashboard is now available in the `public/` directory. To view it:

```bash
python3 -m http.server 8000 --directory public
```

Then open: **http://localhost:8000**

---

## Commands Reference

### Initialize Database

```bash
./scripts/metrics init --config config.yml
```

Initializes the SQLite database schema. Run this once before collecting data.

### Collect Metrics

```bash
./scripts/metrics collect --config config.yml
```

Collects current metrics from GitLab and stores a snapshot in the database.

### Export Data

```bash
./scripts/metrics export --config config.yml
```

Exports all metrics to JSON files:
- `output/latest.json` - Most recent snapshot
- `output/history.json` - All historical data

### Build Dashboard

```bash
./scripts/metrics build-dashboard --config config.yml
```

Copies UI files to `public/` directory and includes the latest data.

### Run All Steps

```bash
./scripts/metrics run --config config.yml
```

Runs collect → export → build-dashboard in sequence.

---

## Understanding the Dashboard

### Main Metrics Displayed

- **Daily Commits** - Number of commits per day over the collection period
- **Epic Commits** - Commits grouped by epic patterns you defined
- **Repository Metrics** - Code statistics (lines of code, files, etc.)
- **Code Coverage** - Test coverage percentage if available
- **Project Info** - Project name, URL, default branch

### Using the Dashboard

- **Zoom**: Scroll on the chart area to zoom in/out
- **Pan**: Click and drag to navigate time ranges
- **Hover**: Hover over data points to see exact values
- **Export**: Most browsers allow exporting charts as PNG

---

## Output Files

After running metrics, you'll have:

```
trailwaze-metrics/
├── data/metrics.db          # SQLite database with all snapshots
├── output/
│   ├── latest.json          # Most recent metrics snapshot
│   └── history.json         # All historical metrics
└── public/
    ├── index.html           # Dashboard HTML
    ├── app.js               # Dashboard logic
    ├── styles.css           # Dashboard styles
    └── data/
        ├── latest.json      # (Copy of output/latest.json)
        └── history.json     # (Copy of output/history.json)
```

---

## Automating with GitLab CI/CD

To run metrics collection automatically every day:

### Step 1: Add GitLab Token as Secret

1. Go to your project: **Settings → CI/CD → Variables**
2. Add a new variable:
   - **Key**: `GITLAB_TOKEN`
   - **Value**: Your personal access token
   - **Protect variable**: ✓ (checked)
   - **Mask variable**: ✓ (checked)

### Step 2: Set Up Pipeline

The included `.gitlab-ci.yml` has three stages:

- **test** - Runs unit tests
- **collect** - Collects metrics and exports data
- **build** - Builds the dashboard and prepares for deployment
- **pages** - Deploys to GitLab Pages (main branch only)

The pipeline runs automatically on every push. Metrics are collected daily if you configure a scheduled pipeline.

### Step 3: Deploy to GitLab Pages (Optional)

To publish your dashboard publicly on GitLab Pages:

1. Ensure your project has Pages enabled: **Settings → Pages**
2. The pipeline will automatically deploy the `public/` directory
3. Access it at: `https://your-username.gitlab.io/trailwaze-metrics/`

---

## Common Issues and Solutions

### "Missing GitLab token in env var: GITLAB_TOKEN"

**Solution**: Set the environment variable before running:
```bash
export GITLAB_TOKEN="your-token-here"
```

In CI/CD, add it to project variables as described above.

### "ModuleNotFoundError: No module named 'metrics'"

**Solution**: Ensure you're in the project root directory and have installed dependencies:
```bash
cd /path/to/trailwaze-metrics
pip install -r requirements.txt
```

### No data showing in dashboard

**Solution**:
1. Verify the token has correct permissions
2. Check that `project_id` in config.yml is correct
3. Run: `./scripts/metrics collect --config config.yml`
4. Check `output/latest.json` exists

### Dashboard won't load

**Solution**: Start the local server correctly:
```bash
cd /path/to/trailwaze-metrics
python3 -m http.server 8000 --directory public
```

---

## Configuration Details

### Epic Patterns

Epic patterns use regular expressions to categorize commits:

```yaml
epics:
  rules:
    - key: "Epic-Auth"
      pattern: "auth|login|oauth|sso"  # Matches auth-related commits
    - key: "Epic-Database"
      pattern: "db|database|sql|migration" # Matches database commits
    - key: "Epic-Performance"
      pattern: "perf|optimize|speed"    # Matches performance work
```

### Collection Settings

| Setting | Description |
|---------|-------------|
| `since_days` | Days to look back (365 = 1 year) |
| `shallow_clone` | Use shallow clone for speed |
| `clone_depth` | Number of commits per fetch |
| `include_paths` | Paths to analyze (`.` = all) |
| `exclude_paths` | Directories to skip |
| `exclude_extensions` | File types to skip |

### Retention Policy

Set how long metrics are stored:

```yaml
retention:
  days: 365  # Delete snapshots older than 365 days
```

---

## API Data Format

The exported JSON has this structure:

```json
{
  "project": {
    "name": "Project Name",
    "web_url": "https://gitlab.com/user/project",
    "default_branch": "main"
  },
  "snapshot_date": "2025-01-28",
  "daily_commits": {
    "2025-01-28": 5,
    "2025-01-27": 3
  },
  "epic_commits": {
    "Epic-Auth": 12,
    "Epic-UI": 24
  },
  "repo_metrics": {
    "files": 342,
    "lines_of_code": 25000,
    "branches": 8
  },
  "coverage": {
    "line_rate": 0.85,
    "branch_rate": 0.78
  }
}
```

---

## Support & Documentation

For more details, see:
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design and components
- [SECURITY.md](SECURITY.md) - Security considerations
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Detailed troubleshooting guide

---

## License

See LICENSE file in the repository.
