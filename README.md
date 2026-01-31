# RnDMetrics - Research & Development Metrics Dashboard

A comprehensive GitHub analytics system that automatically collects daily repository metrics, analyzes development patterns, stores data in SQLite, and publishes an interactive dashboard via GitHub Pages and GitHub Actions.

## 🚀 Live Dashboard

**Dashboard is automatically deployed to GitHub Pages!**

- **Main Dashboard:** https://vionascu.github.io/RnDMetrics/
- **Executive Dashboard:** https://vionascu.github.io/RnDMetrics/executive.html
- **Automatic Updates:** Daily at 2 AM UTC

For setup instructions, see [GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md)

## Quick start
1. Copy and edit the config:
   ```sh
   cp config.example.yml config.yml
   ```
2. Set your GitHub token in the environment (masked in CI):
   ```sh
   export GITHUB_TOKEN="..."
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
