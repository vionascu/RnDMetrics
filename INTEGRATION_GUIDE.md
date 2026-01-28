# RnDMetrics - Integration Guide (Plug & Play)

This guide explains how to integrate RnDMetrics into any GitLab project in under 10 minutes.

---

## Quick Start (5 Minutes)

### For Local Testing

#### Step 1: Prepare Your GitLab Token

If you haven't already, create a GitLab personal access token:

1. Go to GitLab: **Settings → Access Tokens**
2. Create a token with scopes: `api`, `read_repository`
3. Copy the token

#### Step 2: Copy RnDMetrics to Your Project

Option A: Add as a submodule:
```bash
cd your-project
git submodule add <rndmetrics-repo-url> rndmetrics
cd trailwaze-metrics
```

Option B: Copy files directly:
```bash
cp -r rndmetrics/* your-project/metrics-tools/
cd your-project/metrics-tools
```

#### Step 3: Install and Configure

```bash
# Install dependencies
pip install -r requirements.txt

# Copy configuration template
cp config.example.yml config.yml
```

Edit `config.yml` - change these lines:
```yaml
project:
  project_id: "YOUR_PROJECT_ID"    # Get from: Settings → General → Project ID
  gitlab_url: "https://gitlab.com"  # Your GitLab instance
```

#### Step 4: Run It

```bash
export GITLAB_TOKEN="your-token-here"
./scripts/metrics run --config config.yml
```

#### Step 5: View the Dashboard

```bash
python3 -m http.server 8000 --directory public
# Open browser: http://localhost:8000
```

---

## Full Integration (CI/CD Setup)

### For Automated Collection in GitLab CI/CD

#### Step 1: Add RnDMetrics to Your Repository

**Option A: Recommended - As a Git Submodule**

```bash
cd your-project
git submodule add <rndmetrics-repo-url> rndmetrics
git add .gitmodules trailwaze-metrics
git commit -m "Add Trailwaze Metrics submodule"
git push
```

**Option B: Copy All Files**

```bash
cp -r /path/to/rndmetrics/* your-project/
git add .
git commit -m "Add Trailwaze Metrics"
git push
```

#### Step 2: Add GitLab Token to Project Secrets

1. Go to your project on GitLab
2. Navigate to: **Settings → CI/CD → Variables**
3. Click **Add variable**
4. Fill in:
   - **Key**: `GITLAB_TOKEN`
   - **Value**: Your personal access token
   - **Protect variable**: ✓
   - **Mask variable**: ✓
5. Click **Add variable**

#### Step 3: Create/Update `.gitlab-ci.yml`

If you already have `.gitlab-ci.yml`, add the collect and build stages:

```yaml
stages:
  - test
  - collect
  - build
  - pages

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip

# Your existing tests...
test:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - pytest
  # ... rest of your test config

# Collect metrics
collect:
  stage: collect
  image: python:3.11
  script:
    - pip install -r rndmetrics/requirements.txt
    - cp rndmetrics/config.example.yml rndmetrics/config.yml
    - ./rndmetrics/scripts/metrics collect --config rndmetrics/config.yml
    - ./rndmetrics/scripts/metrics export --config rndmetrics/config.yml
  artifacts:
    paths:
      - rndmetrics/data/metrics.db
      - rndmetrics/output/
    expire_in: 1 week

# Build dashboard
build:
  stage: build
  image: python:3.11
  script:
    - pip install -r rndmetrics/requirements.txt
    - cp rndmetrics/config.example.yml rndmetrics/config.yml
    - ./rndmetrics/scripts/metrics collect --config rndmetrics/config.yml
    - ./rndmetrics/scripts/metrics export --config rndmetrics/config.yml
    - mkdir -p public/metrics
    - ./rndmetrics/scripts/metrics build-dashboard --config rndmetrics/config.yml
    - cp -r rndmetrics/public/* public/metrics/
  artifacts:
    paths:
      - public
    expire_in: 1 week

# Deploy to GitLab Pages
pages:
  stage: pages
  script:
    - echo "Deploying metrics dashboard"
  artifacts:
    paths:
      - public
  dependencies:
    - build
  only:
    - main  # Only deploy on main branch
```

If you don't have `.gitlab-ci.yml`, create a new one with the above content.

#### Step 4: Customize Configuration

Edit `rndmetrics/config.yml`:

```yaml
project:
  project_id: "YOUR_PROJECT_ID"

collection:
  since_days: 365           # How far back to collect
  repo_path: "./.tmp/repo"  # Where to cache the cloned repo

epics:                      # Define your work categories
  rules:
    - key: "Feature"
      pattern: "feat|feature|add"
    - key: "Bug"
      pattern: "bug|fix|hotfix"
    - key: "Refactor"
      pattern: "refactor|clean|improve"
    - key: "Performance"
      pattern: "perf|optimize|speed"

ui:
  title: "My Project Metrics"
  theme: "dark"
```

#### Step 5: Test the Pipeline

1. Commit and push your changes:
```bash
git add .gitlab-ci.yml rndmetrics/
git commit -m "Add Trailwaze Metrics integration"
git push
```

2. Go to your project: **CI/CD → Pipelines**
3. You should see the pipeline running
4. After the `build` stage completes, check your dashboard at:
   - **Deployments → Pages** (if main branch)
   - Or locally: `rndmetrics/public/index.html`

---

## Integration Scenarios

### Scenario 1: Multi-Project Monitoring (Recommended)

If you want to monitor multiple projects:

**Option A: Separate Repo Per Project**

```
project-metrics/
├── projects/
│   ├── project-1/
│   │   ├── config.yml
│   │   ├── data/
│   │   └── public/
│   ├── project-2/
│   │   ├── config.yml
│   │   ├── data/
│   │   └── public/
│   └── ...
├── .gitlab-ci.yml  (loops through all projects)
└── rndmetrics/ (shared)
```

**Option B: Centralized Metrics Dashboard**

Create a separate repo just for metrics:
```bash
git new-repo my-org-metrics
cd my-org-metrics
git submodule add <trailwaze-repo-url>

# Monitor all projects
./scripts/collect-all-projects.sh
```

### Scenario 2: Embed in Documentation

Include the JSON data in your documentation:

```markdown
# Project Metrics

Latest metrics available at: `/public/data/latest.json`

You can embed the dashboard as an iframe:
<iframe src="https://your-domain.com/metrics/"></iframe>
```

### Scenario 3: Custom Analytics

Use the exported JSON for custom analysis:

```python
import json

with open('output/latest.json') as f:
    metrics = json.load(f)

# Use in your tools
commits_today = metrics['daily_commits'].get('2025-01-28', 0)
auth_work = metrics['epic_commits'].get('Epic-Auth', 0)
coverage = metrics['coverage']['line_rate']
```

---

## Environment Variables (CI/CD Only)

When running in GitLab CI/CD, these variables are automatically available:

| Variable | Example | Usage |
|----------|---------|-------|
| `GITLAB_TOKEN` | `glpat-...` | GitLab API access |
| `CI_PROJECT_ID` | `77854212` | Current project ID |
| `CI_PROJECT_NAME` | `my-project` | Project name |
| `CI_COMMIT_REF_NAME` | `main` | Current branch |

You can reference them in `config.yml`:

```yaml
project:
  project_id: "${CI_PROJECT_ID}"  # Uses environment variable
```

---

## Scheduling Regular Runs

To collect metrics on a fixed schedule:

### Option 1: GitLab Scheduled Pipelines

1. Go to: **CI/CD → Schedules**
2. Click **New schedule**
3. Set:
   - **Description**: "Daily metrics collection"
   - **Cron**: `0 2 * * *` (2 AM daily)
   - **Timezone**: Your timezone
   - **Target branch**: `main`
4. Click **Create pipeline schedule**

### Option 2: Webhook Trigger

Set up a webhook to trigger on repository events:

```bash
curl -X POST \
  https://gitlab.com/api/v4/projects/YOUR_PROJECT_ID/pipeline \
  -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ref": "main"
  }'
```

---

## Troubleshooting Integration

### Error: "Project not found"
- Check `project_id` in `config.yml`
- Verify token has `api` scope

### Error: "Token not found in environment"
- Ensure `GITLAB_TOKEN` is set in CI/CD Variables
- In local testing: `export GITLAB_TOKEN="..."`

### Dashboard shows no data
1. Check the collect job completed successfully
2. Verify `output/latest.json` exists
3. Check browser console for JavaScript errors

### Pipeline fails at collect stage
1. Verify token permissions (Settings → Access Tokens)
2. Check project visibility
3. Review job logs: **CI/CD → Pipelines → Job**

---

## File Structure After Integration

```
your-project/
├── .gitlab-ci.yml           # Updated with metrics stages
├── rndmetrics/       # (Submodule or copied)
│   ├── metrics/             # Main Python package
│   ├── scripts/
│   │   └── metrics          # CLI script
│   ├── config.example.yml
│   ├── config.yml           # Your config (copy of example)
│   ├── requirements.txt
│   ├── data/
│   │   └── metrics.db       # SQLite database
│   ├── output/
│   │   ├── latest.json
│   │   └── history.json
│   └── public/              # Dashboard files
│       ├── index.html
│       ├── app.js
│       ├── styles.css
│       └── data/
└── ... (your project files)
```

---

## Performance Considerations

### For Large Projects

If your repository is very large:

1. **Use shallow cloning** (default):
```yaml
collection:
  shallow_clone: true
  clone_depth: 50
```

2. **Exclude large directories**:
```yaml
collection:
  exclude_paths: ["node_modules", "dist", "build", ".git", "vendor"]
  exclude_extensions: ["mbtiles", "png", "jpg", "zip", "mp4"]
```

3. **Reduce collection period**:
```yaml
collection:
  since_days: 90  # Instead of 365
```

### Database Optimization

The database grows over time. To keep it manageable:

```yaml
retention:
  days: 365  # Delete snapshots older than 1 year
```

---

## Security Considerations

1. **GitLab Token**:
   - Use a dedicated token with minimal scopes
   - Mask token in CI/CD logs (done automatically)
   - Rotate token regularly

2. **Dashboard Access**:
   - If on GitLab Pages, inherits project visibility
   - Private projects → Private dashboard
   - Public projects → Public dashboard

3. **Data Retention**:
   - Metrics are read-only
   - Database stored in `data/` directory
   - No sensitive data is collected

---

## Next Steps

1. ✅ Set up Trailwaze in your project
2. ✅ Run the first collection
3. ✅ View the dashboard
4. ✅ Customize epic patterns to match your workflow
5. ✅ (Optional) Deploy to GitLab Pages for team access
6. ✅ (Optional) Set up scheduled collection

---

## Support

For issues or questions:
- Check [USER_GUIDE.md](USER_GUIDE.md) for detailed documentation
- Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Check `.gitlab-ci.yml` job logs for error details

---

## License

Trailwaze Metrics is licensed under [your license]. See LICENSE file.
