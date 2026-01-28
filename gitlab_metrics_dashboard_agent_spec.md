
# GitLab Project Metrics Dashboard – Agent Specification

## Epic 0: Vision & Scope
- Build a read-only GitLab analytics system
- Separate dashboard repository
- Daily automated execution
- Static dashboard via GitLab Pages
- Vanilla JS + Chart.js
- SQLite persistence (free)

---

## Epic 1: Security & Read-Only Constraints
- Never modify source repo
- Clone read-only
- Use GitLab API (read-only)
- No secrets in logs, files, or public output
- Masked CI variables

---

## Epic 2: Repository Architecture
- Dedicated Dashboard Repo
- Mandatory file tree
- Separation of collector, storage, export, UI
- Versioned SQLite DB

---

## Epic 3: Configuration & CLI
- CLI tool: `metrics`
- Commands: init, collect, export, build-dashboard, run
- YAML-based configuration
- Epics mapping via regex rules

---

## Epic 4: Data Collection Engine
- GitLab API integration
- Shallow clone support
- Commit metrics
- LOC metrics
- Test detection
- Coverage parsing (lcov, junit, etc.)

---

## Epic 5: Metrics Model & Database
- SQLite schema
- Daily snapshots
- Time series storage
- 365-day history retention

---

## Epic 6: Export & JSON Schema
- latest.json
- history.json
- Stable schema for frontend
- No raw code leakage

---

## Epic 7: Dashboard UI (Vanilla + Chart.js)
- Dark theme
- Responsive grid
- Cards, charts, tables
- Charts: commits, LOC, tests, file types
- Tables: Epics & Source Files

---

## Epic 8: GitLab CI/CD
- Stages: collect, build, pages
- Daily schedule
- Commit DB + JSON to dashboard repo
- Publish via GitLab Pages

---

## Epic 9: Testing & Validation
- Unit tests for metrics
- Epic mapping validation
- Export schema validation

---

## Epic 10: Documentation & DoD
- README with setup
- Architecture docs
- Security docs
- Troubleshooting
- Definition of Done checklist

---

## Epic 11: Final Acceptance
- Source repo unchanged
- Dashboard live
- History growing daily
- No secrets exposed
