# External Repositories Documentation

This document provides an overview of the external repositories integrated with the RnDMetrics system for comprehensive metrics collection and analysis.

## Repositories Overview

### 1. TrailEquip
**Repository URL:** https://github.com/vionascu/trail-equip

**Description:** TrailEquip is a comprehensive trail equipment recommendation system with services for trail management, weather forecasting, and intelligent equipment recommendations.

**Technology Stack:**
- **Backend:** Java with Spring Boot 3.x
- **Testing Framework:** JUnit 5 (Jupiter), Mockito, Spring Boot MockMvc
- **Build System:** Gradle
- **Architecture Pattern:** Microservices (adapter pattern)

**Services:**
- Trail Service - CRUD operations and geographic discovery
- Weather Service - Forecasting and caching
- Recommendation Service - Equipment and trail recommendations

### 2. TrailWaze
**Repository URL:** https://github.com/vionascu/trailwaze

**Description:** TrailWaze is a mobile and web application for trail navigation, providing real-time trail information and user community features.

**Technology Stack:**
- **Frontend:** React (web), React Native (mobile)
- **Build System:** Monorepo with multiple apps
- **Testing:** Custom test frameworks

**Applications:**
- Web application
- Mobile application

---

## Test Metrics Summary

### TrailEquip Test Metrics

| Service | Test Class | Test Count | Coverage Type |
|---------|-----------|-----------|---|
| Trail Service | TrailControllerTest | 9 | REST API, CRUD Operations |
| Weather Service | WeatherControllerTest | 6 | REST API, Caching |
| Recommendation Service | RecommendationControllerTest | 8 | REST API, Recommendations |
| **Total** | | **23** | |

**Test Details:**

#### Trail Service (9 tests)
- Get all trails
- Get trail by ID
- Handle trail not found
- Filter trails by difficulty
- Create trail
- Update trail
- Delete trail
- Suggest trails in geographic area
- Auto-classify trail difficulty

**Performance:** ~10-20ms per test

#### Weather Service (6 tests)
- Get weather forecast
- Get forecast with default date range
- Get cache statistics
- Clear cache
- Get weather for multiple locations
- Validate coordinate ranges

**Performance:** < 5ms to < 50ms per test

#### Recommendation Service (8 tests)
- Get equipment recommendations
- Get trail recommendations
- Equipment recommendations for easy trails
- Equipment recommendations for extreme weather
- Trail recommendations sorted by score
- Request validation
- Get best trail match
- Get risk assessment

**Performance:** ~10-20ms per test

**Total Suite Duration:** ~500ms

### TrailWaze Test Metrics

| Category | Status | Notes |
|----------|--------|-------|
| Test Suite | In Repository | Various test configurations available |
| Coverage Reporting | Available | Multiple test formats supported |
| CI/CD Integration | Implemented | Automated test execution |

**Test Data:**
- Sample trails: Omu Peak Loop and other Romanian mountain trails
- Geographic coordinates: 45.5°N, 25.3°E (Bucegi Mountains)
- Weather range: -20°C to +40°C, 0-60 km/h wind
- Risk levels: LOW, MODERATE, HIGH, EXTREME

---

## RnDMetrics Available Metrics

The RnDMetrics system collects and tracks the following metrics across all integrated repositories:

### Core Metrics

#### Repository Metrics
- **Files Count** - Total number of files in repository
- **Lines of Code (LOC)** - Total lines of source code
- **Branch Count** - Number of active git branches
- **Default Branch** - Main development branch

#### Commit Metrics
- **Daily Commits** - Number of commits per day
- **Epic/Feature Commits** - Commits categorized by feature pattern
- **Author Activity** - Commit distribution by developer
- **Commit Timeline** - Historical commit trends

#### Code Quality Metrics
- **Code Coverage** - Line rate and branch rate coverage
- **Coverage Trends** - Coverage changes over time
- **Test Detection** - Identification of test files
- **File Type Distribution** - Code breakdown by language/type

### Project Information
- Project name and URL
- Default branch
- Last updated timestamp
- Repository size

### Time-Series Data
- **365-day History** - All metrics stored with daily snapshots
- **Retention Policy** - Configurable data retention window
- **Historical Trends** - Long-term metric trends

---

## Data Collection Architecture

```
GitHub API
    ↓
Collector (Python)
    ├─ Parse commits
    ├─ Analyze repository
    └─ Calculate metrics
    ↓
SQLite Database
    │
    ├─ Snapshots Table
    ├─ Daily Commits
    ├─ Epic Commits
    ├─ Repository Metrics
    └─ Coverage Data
    ↓
JSON Export
    ├─ latest.json
    └─ history.json
    ↓
Web Dashboard
    └─ Interactive Visualization
```

---

## Configuration for External Repositories

### Adding a New Repository

Each repository requires a configuration entry:

```yaml
project:
  github_url: "https://github.com"
  owner: "vionascu"
  repo_name: "trail-equip"
  token_env: "GITHUB_TOKEN"

collection:
  since_days: 365
  shallow_clone: true
  exclude_paths:
    - "node_modules"
    - ".git"
    - "dist"
    - "build"

epics:
  rules:
    - key: "Feature-Auth"
      pattern: "auth|login|oauth"
    - key: "Feature-UI"
      pattern: "ui|frontend|dashboard"
    - key: "Feature-API"
      pattern: "api|endpoint|rest"
```

### TrailEquip Configuration
- **Project Type:** Microservices (Java/Spring Boot)
- **Metrics Focus:** Service-level metrics, test coverage
- **Epic Categories:** Authentication, Trail Management, Weather, Recommendations

### TrailWaze Configuration
- **Project Type:** Full-Stack Application (React/React Native)
- **Metrics Focus:** Frontend metrics, cross-platform coverage
- **Epic Categories:** Mobile, Web, Navigation, Community

---

## Metrics Export Format

### Latest.json Structure
```json
{
  "project": {
    "name": "TrailEquip",
    "web_url": "https://github.com/vionascu/trail-equip",
    "default_branch": "main"
  },
  "snapshot_date": "2025-01-31",
  "daily_commits": {
    "2025-01-31": 5,
    "2025-01-30": 3
  },
  "epic_commits": {
    "Trail-Service": 4,
    "Weather-Service": 3,
    "Recommendations": 2
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

### History.json Structure
```json
{
  "project": "TrailEquip",
  "snapshots": [
    { /* 2025-01-31 snapshot */ },
    { /* 2025-01-30 snapshot */ },
    { /* ... historical data ... */ }
  ]
}
```

---

## Related Documentation

- [TrailEquip Test Specifications](external-repos/TRAILEQUIP_TESTS.md)
- [TrailWaze Test Specifications](external-repos/TRAILWAZE_TESTS.md)
- [Test Metrics Report](TEST_METRICS_REPORT.md)
- [Metrics Integration Guide](../INTEGRATION_GUIDE.md)
- [Dashboard Documentation](../USER_GUIDE.md)

---

## Next Steps

1. **Configure Projects** - Update `config.yml` with GitHub owner and repository names
2. **Set GitHub Token** - Ensure `GITHUB_TOKEN` environment variable is set
3. **Collect Metrics** - Run `./scripts/metrics collect` for each project
4. **View Dashboard** - Access aggregated metrics in the web dashboard
5. **Enable Selectors** - Use project selector to filter metrics view

---

**Last Updated:** January 31, 2026
**Version:** 1.0.0
**Maintained by:** Metrics Team
