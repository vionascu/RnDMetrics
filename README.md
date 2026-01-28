# RnDMetrics - Research & Development Metrics Dashboard

A comprehensive GitLab analytics system that automatically collects daily repository metrics, analyzes development patterns, stores data in SQLite, and publishes an interactive dashboard via GitLab Pages.

## Quick start
1. Copy and edit the config:
   ```sh
   cp config.example.yml config.yml
   ```
2. Set your GitLab token in the environment (masked in CI):
   ```sh
   export GITLAB_TOKEN="..."
   ```
3. Run the pipeline locally:
   ```sh
   ./scripts/metrics run --config config.yml
   ```

## Commands
- `scripts/metrics init` – initialize database and folders
- `scripts/metrics collect` – collect metrics and persist snapshot
- `scripts/metrics export` – write JSON export (`output/latest.json`, `output/history.json`)
- `scripts/metrics build-dashboard` – copy UI assets into `public/`
- `scripts/metrics run` – `collect` + `export` + `build-dashboard`

## Output
- SQLite DB: `data/metrics.db`
- JSON exports: `output/latest.json`, `output/history.json`
- Static site: `public/`

See `ARCHITECTURE.md`, `SECURITY.md`, and `TROUBLESHOOTING.md` for details.
