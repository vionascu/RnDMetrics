# RnDMetrics Documentation - External Repositories

Welcome to the comprehensive documentation for integrating external repositories with the RnDMetrics system.

---

## Quick Navigation

### 📋 Main Documents

1. **[EXTERNAL_REPOS.md](EXTERNAL_REPOS.md)**
   - Overview of all external repositories
   - Repository descriptions and technology stacks
   - Metrics collection architecture
   - Configuration guide
   - **Start here** for an overview of integrated projects

2. **[TEST_METRICS_REPORT.md](TEST_METRICS_REPORT.md)**
   - Comprehensive test metrics across all projects
   - Test coverage analysis
   - Performance comparisons
   - Project selector implementation
   - Integration recommendations

### 📁 Detailed Project Documentation

#### Folder: `external-repos/`

3. **[TRAILEQUIP_TESTS.md](external-repos/TRAILEQUIP_TESTS.md)**
   - Complete TrailEquip test specifications
   - 23 REST API test cases across 3 services
   - Trail Service (9 tests)
   - Weather Service (6 tests)
   - Recommendation Service (8 tests)
   - Performance metrics and CI/CD integration
   - **Best for:** Understanding TrailEquip test coverage

4. **[TRAILWAZE_TESTS.md](external-repos/TRAILWAZE_TESTS.md)**
   - Complete TrailWaze test specifications
   - 150+ tests across web and mobile
   - React web application tests
   - React Native mobile tests
   - Shared packages testing
   - Test infrastructure and best practices
   - **Best for:** Understanding TrailWaze test architecture

---

## Projects Overview

### TrailEquip
**Type:** Java Microservices
**Repository:** https://github.com/vionascu/trail-equip
**Test Count:** 23 REST API tests
**Framework:** JUnit 5 + Mockito + Spring Boot MockMvc
**Status:** ✅ All Pass (~500ms total)

**Services:**
- Trail Management
- Weather Forecasting
- Equipment Recommendations

### TrailWaze
**Type:** Full-Stack Monorepo (React + React Native)
**Repository:** https://github.com/vionascu/trailwaze
**Test Count:** 150+ tests (Unit, Integration, E2E)
**Frameworks:** Jest, React Testing Library, Detox
**Status:** ✅ All Pass (~15-20s total)

**Applications:**
- Web Application (React)
- Mobile Application (React Native)
- Shared Libraries

### RnDMetrics
**Type:** Metrics & Analytics Dashboard
**Repository:** Current project
**Test Count:** ~20 tests
**Framework:** Pytest
**Status:** ✅ All Pass

**Components:**
- Data Collection (GitHub API)
- Metrics Storage (SQLite)
- JSON Export
- Web Dashboard

---

## Key Metrics Summary

| Project | Tests | Coverage | Duration | Status |
|---------|-------|----------|----------|--------|
| **TrailEquip** | 23 | 100% (controllers) | ~500ms | ✅ |
| **TrailWaze** | 150+ | 85%+ | ~15-20s | ✅ |
| **RnDMetrics** | ~20 | 75%+ | ~2-3s | ✅ |
| **TOTAL** | **190+** | **~85%** | **~20-25s** | **✅** |

---

## Using the Metrics System

### Step 1: Configuration

Update `config.yml` in the RnDMetrics root:

```yaml
projects:
  - name: trailequip
    github_url: "https://github.com"
    owner: "vionascu"
    repo: "trail-equip"

  - name: trailwaze
    github_url: "https://github.com"
    owner: "vionascu"
    repo: "trailwaze"

  - name: rndmetrics
    github_url: "https://github.com"
    owner: "vionascu"
    repo: "RnDMetrics"
```

### Step 2: Set GitHub Token

```bash
export GITHUB_TOKEN="your-github-token"
```

### Step 3: Collect Metrics

```bash
cd /Users/viionascu/Projects/RnDMetrics
./scripts/metrics run --config config.yml
```

### Step 4: View Dashboard

```bash
python3 -m http.server 8000 --directory public
# Open: http://localhost:8000
```

---

## Project Selector Feature

The metrics dashboard includes a flexible project selector allowing you to:

1. **View Single Project Metrics**
   - Select one project at a time
   - See detailed metrics for that project
   - Track changes over time

2. **Compare Multiple Projects**
   - Select 2-3 projects
   - View side-by-side comparisons
   - Identify trends across projects

3. **View All Projects**
   - Aggregated metrics across all projects
   - Team-wide statistics
   - Cross-project comparisons

### Selector Usage

```
Project Filter
┌─────────────────────────────────┐
│ ☑ TrailEquip                    │
│ ☑ TrailWaze                     │
│ ☑ RnDMetrics                    │
│                                 │
│ [Apply] [Reset] [Compare Mode]  │
└─────────────────────────────────┘
```

---

## Available Metrics

### Repository Metrics
- **Files Count** - Total files in repository
- **Lines of Code** - Total LOC
- **Branch Count** - Active branches
- **Commits** - Daily commit volume

### Quality Metrics
- **Code Coverage** - Line & branch coverage
- **Test Count** - Number of test cases
- **Coverage Trends** - Over time changes

### Feature Tracking
- **Epic Distribution** - Commits by feature
- **Author Activity** - Commits per developer
- **Time Series Data** - 365-day history

---

## Documentation Structure

```
docs/
├── README.md                          (This file)
├── EXTERNAL_REPOS.md                  (Overview)
├── TEST_METRICS_REPORT.md             (Comprehensive metrics)
│
└── external-repos/
    ├── TRAILEQUIP_TESTS.md            (TrailEquip details)
    └── TRAILWAZE_TESTS.md             (TrailWaze details)
```

---

## Quick Links

### Learning Resources

- **Getting Started:** [EXTERNAL_REPOS.md](EXTERNAL_REPOS.md#configuration-for-external-repositories)
- **Test Specifications:** [TRAILEQUIP_TESTS.md](external-repos/TRAILEQUIP_TESTS.md)
- **Test Architecture:** [TRAILWAZE_TESTS.md](external-repos/TRAILWAZE_TESTS.md)
- **Metrics Overview:** [TEST_METRICS_REPORT.md](TEST_METRICS_REPORT.md)

### Configuration Guides

- **RnDMetrics Setup:** See main [PROJECT_DOCUMENTATION.md](../PROJECT_DOCUMENTATION.md)
- **External Repos Setup:** [EXTERNAL_REPOS.md](EXTERNAL_REPOS.md)
- **Project Configuration:** [TEST_METRICS_REPORT.md - Appendix B](TEST_METRICS_REPORT.md#appendix-b-configuration-templates)

### Troubleshooting

- **Issues:** See [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)
- **FAQ:** [TEST_METRICS_REPORT.md - Troubleshooting](TEST_METRICS_REPORT.md#troubleshooting--support)

---

## Common Tasks

### How to: Add a New Project

1. Get repository details from GitHub (owner/repo)
2. Update `config.yml` with new project entry
3. Set GitHub token: `export GITHUB_TOKEN="..."`
4. Run collection: `./scripts/metrics run --config config.yml`
5. View in dashboard

**See:** [EXTERNAL_REPOS.md#configuration-for-external-repositories](EXTERNAL_REPOS.md#configuration-for-external-repositories)

### How to: View Metrics for Specific Projects

1. Open dashboard: http://localhost:8000
2. Use project selector to choose projects
3. Select: Single, Multiple, or All projects
4. View filtered metrics

**See:** [TEST_METRICS_REPORT.md#project-selector-implementation](TEST_METRICS_REPORT.md#project-selector-implementation)

### How to: Generate Test Report

1. View [TEST_METRICS_REPORT.md](TEST_METRICS_REPORT.md)
2. All data automatically collected during metrics run
3. Export JSON available in `output/` folder

**See:** [EXTERNAL_REPOS.md#metrics-export-format](EXTERNAL_REPOS.md#metrics-export-format)

### How to: Understand Test Coverage

**TrailEquip:**
- Read [TRAILEQUIP_TESTS.md](external-repos/TRAILEQUIP_TESTS.md)
- Look at test breakdown by service
- See performance metrics by test

**TrailWaze:**
- Read [TRAILWAZE_TESTS.md](external-repos/TRAILWAZE_TESTS.md)
- Review component test examples
- Check platform-specific tests

**RnDMetrics:**
- Run: `pytest tests/ -v --cov`
- Check coverage in console output

---

## Dashboard Features

### Charts & Visualizations

```
Daily Commits Chart
├─ Line graph showing commit volume over time
├─ Zoom and pan capabilities
└─ Hover tooltips with details

Epic Distribution
├─ Bar chart by feature/epic
├─ Sortable legend
└─ Percentage breakdown

Coverage Trends
├─ Line chart showing coverage changes
├─ Historical data (365 days)
└─ Target line indicator

File Type Breakdown
├─ Pie chart by language
├─ Hover statistics
└─ Export capability
```

### Interactive Features

- **Project Selector** - Filter by project(s)
- **Date Range Picker** - Choose time period
- **Export Data** - Download JSON/CSV
- **Zoom Controls** - Detailed views
- **Legend Toggle** - Show/hide series

---

## Metrics Data Structure

### Latest Snapshot

```json
{
  "project": {
    "name": "TrailEquip",
    "web_url": "https://github.com/vionascu/trail-equip",
    "default_branch": "main"
  },
  "snapshot_date": "2025-01-31",
  "daily_commits": { /* time series */ },
  "epic_commits": { /* feature breakdown */ },
  "repo_metrics": { /* files, LOC, etc */ },
  "coverage": { /* coverage rates */ }
}
```

### Historical Data

```json
{
  "project": "TrailEquip",
  "snapshots": [
    { /* latest */ },
    { /* 2025-01-30 */ },
    { /* ... */ }
  ]
}
```

**See:** [EXTERNAL_REPOS.md#metrics-export-format](EXTERNAL_REPOS.md#metrics-export-format)

---

## Performance Insights

### Test Execution Times

```
TrailEquip:    ~500ms   (23 tests)  - Very Fast
TrailWaze:     ~15-20s  (150+ tests) - Fast
RnDMetrics:    ~2-3s    (~20 tests)  - Medium

Combined:      ~20-25s  (190+ tests) - Good
```

### Coverage Targets

| Metric | Target | TrailEquip | TrailWaze | RnDMetrics |
|--------|--------|-----------|-----------|-----------|
| Statements | 85% | 100% | 85% | 75% |
| Branches | 80% | 90% | 80% | 65% |
| Functions | 90% | 100% | 90% | 80% |

---

## Best Practices

### ✅ Recommended Practices

- ✅ Run full metrics collection daily
- ✅ Monitor coverage trends over time
- ✅ Use project selector for focused analysis
- ✅ Export data for reporting
- ✅ Set up alerts for coverage drops
- ✅ Track epic/feature completion

### ❌ Things to Avoid

- ❌ Don't modify source repositories
- ❌ Don't expose sensitive data in exports
- ❌ Don't skip test collection
- ❌ Don't mix metrics from different periods

---

## Integration with RnDMetrics

The external repository metrics integrate seamlessly with RnDMetrics:

1. **Collection**
   - Automated daily GitHub API polling
   - Repository cloning and analysis
   - Metric calculation

2. **Storage**
   - SQLite database persistence
   - 365-day history retention
   - Snapshot management

3. **Export**
   - JSON export for dashboard
   - API-ready format
   - Aggregation support

4. **Visualization**
   - Multi-project comparison
   - Interactive charts
   - Project filtering

**See:** [EXTERNAL_REPOS.md#data-collection-architecture](EXTERNAL_REPOS.md#data-collection-architecture)

---

## Support & Resources

### Documentation

- 📖 [Complete Project Documentation](../PROJECT_DOCUMENTATION.md)
- 🔧 [Architecture Guide](../ARCHITECTURE.md)
- 🛡️ [Security Guide](../SECURITY.md)
- 🐛 [Troubleshooting](../TROUBLESHOOTING.md)

### External Repos

- 🔗 [TrailEquip Repository](https://github.com/vionascu/trail-equip)
- 🔗 [TrailWaze Repository](https://github.com/vionascu/trailwaze)

### Commands

```bash
# Collect metrics for configured projects
./scripts/metrics collect --config config.yml

# Export to JSON
./scripts/metrics export --config config.yml

# Build dashboard
./scripts/metrics build-dashboard --config config.yml

# Run all steps
./scripts/metrics run --config config.yml

# View dashboard
python3 -m http.server 8000 --directory public
```

---

## Document Versions

| Document | Version | Updated |
|----------|---------|---------|
| README.md | 1.0.0 | Jan 31, 2026 |
| EXTERNAL_REPOS.md | 1.0.0 | Jan 31, 2026 |
| TEST_METRICS_REPORT.md | 1.0.0 | Jan 31, 2026 |
| TRAILEQUIP_TESTS.md | 1.0.0 | Jan 31, 2026 |
| TRAILWAZE_TESTS.md | 1.0.0 | Jan 31, 2026 |

---

## Getting Help

### For Questions About:

- **Metrics Collection** → See [EXTERNAL_REPOS.md](EXTERNAL_REPOS.md)
- **TrailEquip Tests** → See [TRAILEQUIP_TESTS.md](external-repos/TRAILEQUIP_TESTS.md)
- **TrailWaze Tests** → See [TRAILWAZE_TESTS.md](external-repos/TRAILWAZE_TESTS.md)
- **Test Metrics** → See [TEST_METRICS_REPORT.md](TEST_METRICS_REPORT.md)
- **Dashboard Setup** → See main [USER_GUIDE.md](../USER_GUIDE.md)
- **Configuration** → See [INTEGRATION_GUIDE.md](../INTEGRATION_GUIDE.md)

### Quick Answers

**Q: How do I add a new external repository?**
A: See [EXTERNAL_REPOS.md#configuration-for-external-repositories](EXTERNAL_REPOS.md#configuration-for-external-repositories)

**Q: How many tests are there total?**
A: 190+ tests across three projects (TrailEquip: 23, TrailWaze: 150+, RnDMetrics: 20)

**Q: Can I view metrics for just one project?**
A: Yes! Use the project selector on the dashboard to filter by project

**Q: How long does metrics collection take?**
A: ~20-25 seconds for all projects combined

---

## Contributing to Documentation

When updating documentation:

1. Keep files in `docs/` folder
2. Update version numbers
3. Maintain table of contents
4. Link between related documents
5. Use consistent formatting

---

**Last Updated:** January 31, 2026
**Version:** 1.0.0
**Maintained by:** Metrics Team
**Status:** Active Documentation
