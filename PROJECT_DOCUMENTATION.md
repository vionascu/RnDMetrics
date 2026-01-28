# RnDMetrics - Complete Project Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Project Structure](#project-structure)
4. [Installation Steps](#installation-steps)
5. [Configuration Guide](#configuration-guide)
6. [Running the System](#running-the-system)
7. [Component Details](#component-details)
8. [Data Flow](#data-flow)
9. [Database Schema](#database-schema)
10. [API Reference](#api-reference)
11. [Dashboard Features](#dashboard-features)
12. [Development Guide](#development-guide)
13. [Deployment](#deployment)
14. [Troubleshooting](#troubleshooting)

---

## Project Overview

**RnDMetrics** (Research & Development Metrics) is an automated GitLab analytics platform that:

- **Collects** real-time metrics from GitLab projects (commits, branches, coverage)
- **Stores** historical data in SQLite database
- **Analyzes** code development patterns using custom epic tracking
- **Exports** metrics as JSON for integration
- **Visualizes** metrics in an interactive web dashboard

### Key Features

✅ Automated daily metrics collection
✅ Epic/feature tracking by commit message pattern
✅ Code coverage tracking
✅ Repository analysis (LOC, file count, branches)
✅ Historical data retention with configurable policies
✅ Static web dashboard for visualization
✅ JSON API exports for custom tools
✅ GitLab Pages integration for team access

---

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    RnDMetrics System                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐      ┌──────────────┐     ┌────────────┐ │
│  │ GitLab API  │──→   │  Collector   │──→  │  SQLite DB │ │
│  └─────────────┘      │   (Python)   │     └────────────┘ │
│       │                └──────────────┘          │         │
│       │                     │                    │         │
│  • Commits              • Parse commits      • Snapshots   │
│  • Branches             • Calculate metrics  • History     │
│  • Coverage             • Track epics        • Retention   │
│  • Project info         • Clone repository                 │
│                                                 │         │
│                              ┌──────────────────┘         │
│                              │                             │
│                         ┌────▼──────┐      ┌────────────┐ │
│                         │ Exporter  │──→   │   JSON     │ │
│                         └───────────┘      │   Files    │ │
│                                            └────────────┘ │
│                                                 │         │
│                                    ┌────────────┘         │
│                                    │                      │
│                            ┌───────▼────────┐             │
│                            │  Dashboard UI  │             │
│                            │  (HTML/JS/CSS) │             │
│                            └────────────────┘             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Components

| Component | Purpose | Language |
|-----------|---------|----------|
| **Collector** | Fetches data from GitLab, analyzes repo | Python |
| **Storage** | SQLite database management | Python |
| **Exporter** | Converts DB data to JSON | Python |
| **CLI** | Command-line interface | Python |
| **Dashboard** | Web-based visualization | HTML/JavaScript/CSS |

---

## Project Structure

```
RnDMetrics/
├── metrics/                    # Main Python package
│   ├── __init__.py
│   ├── cli.py                 # Command-line interface
│   ├── collector.py           # Data collection from GitLab
│   ├── storage.py             # Database operations
│   ├── exporter.py            # JSON export
│   ├── config.py              # Configuration loader
│   ├── gitlab.py              # GitLab API client
│   ├── metrics_calc.py        # Metrics calculations
│   └── utils.py               # Utility functions
│
├── ui/                         # Dashboard frontend
│   ├── index.html             # Dashboard HTML
│   ├── app.js                 # Dashboard logic
│   └── styles.css             # Styling
│
├── scripts/                    # Executable scripts
│   └── metrics                # Main CLI entry point
│
├── sql/                        # Database schema
│   └── schema.sql             # SQLite schema
│
├── tests/                      # Unit tests
│   ├── conftest.py            # Pytest configuration
│   └── test_metrics_calc.py   # Test cases
│
├── data/                       # Data storage (created at runtime)
│   └── metrics.db             # SQLite database
│
├── output/                     # Export output (created at runtime)
│   ├── latest.json            # Current snapshot
│   └── history.json           # All historical data
│
├── public/                     # Dashboard deployment (created at runtime)
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   └── data/
│       ├── latest.json
│       └── history.json
│
├── config.example.yml         # Configuration template
├── config.yml                 # Active configuration (git ignored)
├── requirements.txt           # Python dependencies
├── requirements-dev.txt       # Development dependencies
├── .gitlab-ci.yml             # CI/CD pipeline
├── .gitignore                 # Git ignore rules
├── README.md                  # Quick start
├── USER_GUIDE.md              # User documentation
├── INTEGRATION_GUIDE.md       # Integration instructions
├── ARCHITECTURE.md            # Architecture details
├── SECURITY.md                # Security guide
├── TROUBLESHOOTING.md         # Troubleshooting
└── PROJECT_DOCUMENTATION.md   # This file
```

---

## Installation Steps

### Step 1: Prerequisites

Verify you have:
- **Python 3.9+**: `python3 --version`
- **Git**: `git --version`
- **pip**: `pip3 --version`
- **GitLab Account**: With at least one project

### Step 2: Clone Repository

```bash
git clone <repository-url> RnDMetrics
cd RnDMetrics
```

### Step 3: Create Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

Installs:
- `pyyaml` - YAML configuration parsing
- `requests` - HTTP library for GitLab API
- `pytest` - Testing framework
- `pytest-cov` - Code coverage tracking

### Step 5: Create Configuration

```bash
cp config.example.yml config.yml
```

### Step 6: Prepare GitLab Token

Create personal access token at: **GitLab Settings → Access Tokens**

Required scopes:
- `api` - Full API access
- `read_repository` - Repository read access

Export the token:
```bash
export GITLAB_TOKEN="glpat-xxxxx"
```

### Step 7: Verify Installation

```bash
./scripts/metrics --help
```

Should show available commands.

---

## Configuration Guide

### Main Configuration File: `config.yml`

```yaml
project:
  # GitLab connection settings
  gitlab_url: "https://gitlab.com"           # GitLab instance URL
  project_id: "YOUR_PROJECT_ID"              # Project ID (Settings → General)
  token_env: "GITLAB_TOKEN"                  # Environment variable for token
  repo_url: ""                               # Leave empty for auto-detection

collection:
  # Data collection settings
  since_days: 365                            # Days to collect (365 = 1 year)
  shallow_clone: true                        # Use shallow clone (faster)
  clone_depth: 50                            # Commits per fetch batch
  repo_path: "./.tmp/repo"                   # Local clone location

  # Path filtering
  include_paths: ["."]                       # Paths to analyze
  exclude_paths:                             # Paths to skip
    - "node_modules"
    - ".git"
    - "dist"
    - "build"
  exclude_extensions:                        # File types to skip
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
  # Feature/epic tracking by commit pattern
  rules:
    - key: "Epic-Auth"
      pattern: "auth|login|oauth|sso"
    - key: "Epic-UI"
      pattern: "ui|frontend|dashboard|chart"
    - key: "Epic-Database"
      pattern: "db|database|sql|migration"
    - key: "Epic-API"
      pattern: "api|endpoint|rest|graphql"
    - key: "Epic-Performance"
      pattern: "perf|optimize|speed|cache"

retention:
  # Data retention policy
  days: 365                                  # Delete snapshots older than this

export:
  # Export settings
  output_dir: "./output"                     # JSON export directory
  public_dir: "./public"                     # Dashboard deployment directory

ui:
  # Dashboard appearance
  title: "R&D Metrics Dashboard"             # Dashboard title
  theme: "dark"                              # Theme: dark or light

storage:
  # Database settings
  db_path: "./data/metrics.db"               # SQLite database location
  schema_path: "./sql/schema.sql"            # Schema file location
```

### Finding Your Project ID

1. Go to your GitLab project
2. Click **Settings** → **General**
3. Look for "Project ID" near the top
4. Copy the numeric ID

### Customizing Epic Patterns

Modify `config.yml` `epics.rules` section:

```yaml
epics:
  rules:
    - key: "Feature-Development"
      pattern: "feat|feature|add|implement"
    - key: "Bug-Fixes"
      pattern: "bug|fix|hotfix|patch"
    - key: "Documentation"
      pattern: "doc|docs|readme|guide"
```

Patterns are **case-insensitive** regular expressions. Commits matching the pattern are counted in the epic.

---

## Running the System

### Command: `metrics init`

Initializes the database schema.

```bash
./scripts/metrics init --config config.yml
```

**When to use**: Once, before first collection or to reset database.

### Command: `metrics collect`

Collects current metrics from GitLab project.

```bash
./scripts/metrics collect --config config.yml
```

**Process**:
1. Loads configuration
2. Initializes database if needed
3. Connects to GitLab API using token
4. Fetches project information
5. Retrieves all commits since `since_days`
6. Clones repository to analyze
7. Calculates repository metrics
8. Checks for code coverage
9. Tracks commits by epic pattern
10. Stores snapshot in database

**Output**:
- Database updated: `data/metrics.db`
- Console logs showing progress

### Command: `metrics export`

Exports database data to JSON files.

```bash
./scripts/metrics export --config config.yml
```

**Output**:
- `output/latest.json` - Most recent snapshot
- `output/history.json` - All historical data

### Command: `metrics build-dashboard`

Prepares dashboard files for deployment.

```bash
./scripts/metrics build-dashboard --config config.yml
```

**Process**:
1. Copies UI files from `ui/` to `public/`
2. Copies JSON exports to `public/data/`
3. Creates necessary directories

**Output**:
- `public/index.html` - Deployable dashboard
- `public/app.js` - Dashboard logic
- `public/styles.css` - Styling
- `public/data/latest.json` - Current metrics
- `public/data/history.json` - Historical metrics

### Command: `metrics run`

Runs all steps: collect → export → build-dashboard.

```bash
./scripts/metrics run --config config.yml
```

**Recommended**: Use this for production/CI-CD.

### Full Workflow Example

```bash
# 1. Ensure token is set
export GITLAB_TOKEN="your-token-here"

# 2. Run everything
./scripts/metrics run --config config.yml

# 3. View dashboard locally
python3 -m http.server 8000 --directory public

# 4. Open browser: http://localhost:8000
```

---

## Component Details

### 1. Collector (`metrics/collector.py`)

**Purpose**: Gathers metrics from GitLab

**Key Methods**:
- `collect()` - Main collection orchestrator
- `_gitlab_client()` - Creates authenticated API client
- `_clone_repo()` - Clones repository for analysis

**Data Collected**:
- Commits (date, message, title)
- Project metadata (name, URL, branch)
- Repository structure (files, LOC)
- Code coverage (if available)

### 2. Storage (`metrics/storage.py`)

**Purpose**: Manages SQLite database

**Key Methods**:
- `init_db()` - Creates schema from `sql/schema.sql`
- `store_snapshot()` - Inserts new data point
- `purge_old()` - Deletes data older than retention policy

**Tables**:
- `snapshots` - Metric snapshots with timestamp
- `daily_commits` - Per-day commit counts
- `epic_commits` - Per-epic commit counts
- `repo_metrics` - Repository statistics

### 3. Exporter (`metrics/exporter.py`)

**Purpose**: Converts database data to JSON

**Key Methods**:
- `export_json()` - Exports all data

**Output Format**:
```json
{
  "project": { "name": "...", "web_url": "...", "default_branch": "..." },
  "snapshot_date": "2025-01-28",
  "daily_commits": { "2025-01-28": 5, "2025-01-27": 3 },
  "epic_commits": { "Epic-Auth": 12, "Epic-UI": 24 },
  "repo_metrics": { "files": 342, "lines_of_code": 25000 },
  "coverage": { "line_rate": 0.85, "branch_rate": 0.78 }
}
```

### 4. CLI (`metrics/cli.py`)

**Purpose**: Command-line interface

**Commands**:
- `init` - Initialize database
- `collect` - Collect metrics
- `export` - Export to JSON
- `build-dashboard` - Build UI
- `run` - Run all steps

### 5. GitLab Client (`metrics/gitlab.py`)

**Purpose**: Wraps GitLab API calls

**Key Methods**:
- `get_project()` - Fetch project info
- `list_commits()` - Get commits since date

**API Endpoints Used**:
- `/projects/{id}` - Project information
- `/projects/{id}/repository/commits` - Commits list

### 6. Metrics Calculator (`metrics/metrics_calc.py`)

**Purpose**: Calculates repository metrics

**Key Functions**:
- `calculate_repo_metrics()` - Analyze repo structure
- `parse_lcov()` - Parse code coverage reports
- `is_test_file()` - Identify test files

**Metrics Calculated**:
- Lines of code (LOC)
- File count
- Branch count
- Test file identification
- Code coverage percentage

---

## Data Flow

### Collection Flow

```
1. User runs: ./scripts/metrics collect
2. CLI loads config.yml
3. Collector initializes:
   - Creates GitLab client with token
   - Gets project info from API
   - Lists commits since last collection
4. For each commit:
   - Extract date and message
   - Match against epic patterns
   - Increment daily_commits[date]
   - Increment epic_commits[epic_key]
5. Clone repository:
   - Use shallow clone for speed
   - Analyze file structure
   - Count lines of code
6. Calculate metrics:
   - File statistics
   - Code coverage (if lcov.info exists)
7. Store snapshot:
   - Insert into database with timestamp
   - Keep data within retention policy
8. Report results
```

### Data Processing Pipeline

```
GitLab API
    ↓
Collector.collect()
    ↓ (Parse commits)
Daily commits dict + Epic commits dict
    ↓ (Analyze repo)
Repository metrics + Coverage data
    ↓ (Combine)
Snapshot object
    ↓ (Store)
SQLite database
    ↓ (Export)
JSON files
    ↓ (Visualize)
Web dashboard
```

---

## Database Schema

### Schema File: `sql/schema.sql`

```sql
CREATE TABLE IF NOT EXISTS snapshots (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  project_name TEXT,
  project_url TEXT,
  default_branch TEXT,
  daily_commits JSON,
  epic_commits JSON,
  repo_metrics JSON,
  coverage JSON,
  retention_days INTEGER
);
```

### Table: `snapshots`

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Auto-increment primary key |
| `timestamp` | DATETIME | When snapshot was created |
| `project_name` | TEXT | Project name |
| `project_url` | TEXT | Project web URL |
| `default_branch` | TEXT | Default branch (main/master) |
| `daily_commits` | JSON | `{date: count, ...}` |
| `epic_commits` | JSON | `{epic_key: count, ...}` |
| `repo_metrics` | JSON | `{files: N, lines_of_code: N, ...}` |
| `coverage` | JSON | `{line_rate: 0.85, branch_rate: 0.78}` |
| `retention_days` | INTEGER | Retention policy in days |

### Example Data

```json
{
  "daily_commits": {
    "2025-01-28": 5,
    "2025-01-27": 3,
    "2025-01-26": 7
  },
  "epic_commits": {
    "Epic-Auth": 4,
    "Epic-UI": 8,
    "Epic-Database": 3
  },
  "repo_metrics": {
    "files": 342,
    "lines_of_code": 25847,
    "branches": 8
  },
  "coverage": {
    "line_rate": 0.847,
    "branch_rate": 0.758
  }
}
```

---

## API Reference

### Environment Variables

```bash
GITLAB_TOKEN      # Required: GitLab personal access token
GITLAB_URL        # Optional: GitLab instance URL (default: https://gitlab.com)
```

### Configuration Options

All configuration is in `config.yml`. See [Configuration Guide](#configuration-guide) section.

### JSON Export Format

#### `output/latest.json`

Latest metrics snapshot:

```json
{
  "project": {
    "name": "My Project",
    "web_url": "https://gitlab.com/user/project",
    "default_branch": "main"
  },
  "snapshot_date": "2025-01-28",
  "daily_commits": {...},
  "epic_commits": {...},
  "repo_metrics": {...},
  "coverage": {...},
  "retention_days": 365
}
```

#### `output/history.json`

All historical snapshots:

```json
{
  "snapshots": [
    { /* 2025-01-28 snapshot */ },
    { /* 2025-01-27 snapshot */ },
    { /* ... */ }
  ]
}
```

---

## Dashboard Features

### Dashboard Overview

Located at `public/index.html` when deployed.

**Features**:

1. **Daily Commits Chart**
   - Line chart showing commits per day
   - Zoom and pan capabilities
   - Hover tooltips

2. **Epic Distribution**
   - Bar chart showing commits per epic
   - Breakdown of work by category
   - Sortable legends

3. **Repository Statistics**
   - Total files
   - Lines of code
   - Active branches
   - Code coverage percentage

4. **Project Information**
   - Project name and URL
   - Default branch
   - Last updated date

### Dashboard Technology

- **Frontend**: HTML5, vanilla JavaScript (no framework)
- **Charts**: Built-in canvas charts
- **Styling**: Custom CSS with dark/light theme support
- **Data**: Loads from `data/latest.json`

### Customizing Dashboard

Edit `ui/styles.css` for theme colors:

```css
:root {
  --primary-color: #007bff;
  --background-color: #1a1a1a;
  --text-color: #ffffff;
  --border-color: #333333;
}
```

Edit `ui/app.js` to add new charts or modify behavior.

---

## Development Guide

### Running Tests

```bash
pip install -r requirements-dev.txt
pytest tests/
```

### Test Files

- `tests/conftest.py` - Pytest configuration
- `tests/test_metrics_calc.py` - Metric calculation tests

### Adding Tests

Create test file in `tests/`:

```python
from metrics.metrics_calc import is_test_file

def test_my_feature():
    result = is_test_file("tests/test_api.py")
    assert result == True
```

Run with:
```bash
pytest tests/test_my_feature.py -v
```

### Code Structure

- **Metrics package**: `metrics/` - All business logic
- **UI**: `ui/` - Frontend files
- **Scripts**: `scripts/metrics` - CLI entry point
- **Configuration**: `config.yml` - Runtime settings

### Adding New Features

1. Add logic to appropriate module in `metrics/`
2. Update CLI command in `metrics/cli.py` if needed
3. Write tests in `tests/`
4. Update documentation
5. Create git commit with changes

---

## Deployment

### Local Deployment

Start web server:

```bash
python3 -m http.server 8000 --directory public
```

Access at: `http://localhost:8000`

### GitLab Pages Deployment

The `.gitlab-ci.yml` pipeline automatically:
1. Collects metrics
2. Exports JSON
3. Builds dashboard
4. Deploys to GitLab Pages

Dashboard becomes public at: `https://your-username.gitlab.io/RnDMetrics/`

### Docker Deployment (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["./scripts/metrics", "run", "--config", "config.yml"]
```

Build and run:

```bash
docker build -t rndmetrics .
docker run -e GITLAB_TOKEN=$GITLAB_TOKEN rndmetrics
```

---

## Troubleshooting

### Issue: "Missing GitLab token in env var: GITLAB_TOKEN"

**Solution**: Set environment variable before running:
```bash
export GITLAB_TOKEN="your-token-here"
./scripts/metrics run --config config.yml
```

### Issue: "Project not found"

**Solution**:
- Verify `project_id` in `config.yml`
- Check token has `api` scope
- Ensure project is accessible to token owner

### Issue: "ModuleNotFoundError: No module named 'metrics'"

**Solution**:
```bash
cd /path/to/RnDMetrics
pip install -r requirements.txt
python3 -m pytest tests/  # Verify installation
```

### Issue: No data in dashboard

**Solution**:
1. Run: `./scripts/metrics collect --config config.yml`
2. Check: `output/latest.json` exists
3. Verify: GitLab token has `api` scope
4. Check: Browser console for JavaScript errors

### Issue: Dashboard won't load

**Solution**: Start server from correct directory:
```bash
cd /path/to/RnDMetrics
python3 -m http.server 8000 --directory public
```

Then visit: `http://localhost:8000`

### Issue: Collection is very slow

**Solution**: Enable shallow clone in `config.yml`:
```yaml
collection:
  shallow_clone: true
  clone_depth: 50
```

Also exclude large directories:
```yaml
collection:
  exclude_paths: ["node_modules", "dist", ".git", "vendor"]
```

---

## Support & Resources

- **User Guide**: [USER_GUIDE.md](USER_GUIDE.md)
- **Integration Guide**: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Security**: [SECURITY.md](SECURITY.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## Version Information

- **Project**: RnDMetrics
- **Version**: 1.0.0
- **Python**: 3.9+
- **Database**: SQLite3
- **Last Updated**: 2025-01-28

---

## License

See LICENSE file in repository.
