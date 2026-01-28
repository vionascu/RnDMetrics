# Architecture

## Components
- **Collector**: Pulls read-only data from GitLab API and (optionally) a shallow clone.
- **Storage**: SQLite database with daily snapshots and time series tables.
- **Exporter**: Produces stable JSON (`latest.json`, `history.json`) for the UI.
- **UI**: Static dashboard (Vanilla JS + Chart.js) published via GitLab Pages.

## Data flow
1. `metrics collect` gathers GitLab metrics + repo signals.
2. Snapshot is stored in SQLite.
3. `metrics export` writes JSON exports.
4. `metrics build-dashboard` copies UI assets into `public/`.

## Key paths
- DB: `data/metrics.db`
- Exports: `output/latest.json`, `output/history.json`
- Site: `public/`
