# Quick Start Guide - RnDMetrics Dashboard

## What You Have

A fully automated evidence-backed metrics system that analyzes GitHub projects with:
- ✅ Zero guessing policy
- ✅ Complete audit trail
- ✅ Interactive dashboard
- ✅ Real-time filtering

## 3-Step Workflow

### 1. Add Projects to `projects.json`

Edit the file and list GitHub project URLs:

```json
{
  "projects": [
    {
      "url": "https://github.com/vionascu/trailwaze",
      "language": "mixed",
      "description": "Trail navigation app"
    },
    {
      "url": "https://github.com/vionascu/trail-equip",
      "language": "java",
      "description": "Trail equipment system"
    }
  ]
}
```

### 2. Run Metrics Collection

```bash
./run_metrics.sh --range last_30_days
```

### 3. View Dashboard

Open: **https://vionascu.github.io/RnDMetrics/**

## Dashboard Features

- **Date Range Selector**: Filter metrics by time period
- **Project Selector**: View individual or combined projects
- **Dynamic Graphs**: Charts reload when filters change
- **Evidence Trails**: All calculations shown with sources

## Current Projects

1. **Trailwaze** - React/React Native mobile/web app
2. **Trail-Equip** - Java/Spring Boot microservices

