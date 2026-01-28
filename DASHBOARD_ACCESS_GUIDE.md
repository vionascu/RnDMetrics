# RnDMetrics Dashboard Access Guide

## 🎯 Dashboard Locations

### Option 1: GitLab Pages (Recommended - Live Deployment)
Once GitLab CI builds and deploys, access at:
- **Main Dashboard**: https://vic-ionascu.gitlab.io/RnDMetrics/
- **Direct Link**: https://vic-ionascu.gitlab.io/RnDMetrics/dashboard.html

**Status**: Will be available after next pipeline run

### Option 2: Local Development Server

#### Start Server
```bash
cd /Users/viionascu/Projects/RnDMetrics
python3 -m http.server 8888
```

#### Access Dashboard
- **Index**: http://localhost:8888/
- **Dashboard**: http://localhost:8888/public/dashboard.html
- **Analysis Data**: http://localhost:8888/public/data/latest.json

### Option 3: Direct File Access
Open in browser:
```
file:///Users/viionascu/Projects/RnDMetrics/public/dashboard.html
```

## 📊 Dashboard Features

### Metrics Displayed
- **Total Commits**: 15
- **AI-Written Code**: 73% (11 commits)
- **Human Code**: 27% (4 commits)
- **Code Reviews**: 12 total
- **Lines Refactored**: 1,247
- **Test Pass Rate**: 100% (56/56)

### Interactive Elements
- **Time Selector**: Filter data by 7/30/90 days or all time
- **Interactive Charts**: 
  - AI vs Human Code distribution
  - Code reviews trend
  - Refactored lines breakdown
  - Test distribution

### Analysis Tables
1. **AI vs Human Code Analysis**
2. **Code Review Metrics**
3. **Refactoring Breakdown**
4. **Test Metrics**

## 🔧 Troubleshooting

### Dashboard Not Loading
1. **Check File Exists**:
   ```bash
   ls -la /Users/viionascu/Projects/RnDMetrics/public/dashboard.html
   ```

2. **Start Local Server**:
   ```bash
   cd /Users/viionascu/Projects/RnDMetrics
   python3 -m http.server 8888
   ```

3. **Test Connectivity**:
   ```bash
   curl http://localhost:8888/public/dashboard.html | head -20
   ```

### GitLab Pages Not Updated
- Push changes to main branch
- Check GitLab CI/CD pipeline: https://gitlab.com/vic.ionascu/RnDMetrics/-/pipelines
- Wait for build and pages deployment
- Clear browser cache and refresh

## 📝 Files Structure
```
RnDMetrics/
├── public/
│   ├── index.html          ← Redirect page
│   └── dashboard.html      ← Main dashboard
├── output/
│   ├── latest.json         ← Current metrics
│   └── analysis.json       ← AI/Human analysis
└── DASHBOARD_ACCESS_GUIDE.md
```

## 🚀 Next Steps

1. **GitLab CI/CD**: Will automatically deploy dashboard on next commit
2. **Browser Access**: 
   - Once deployed: https://vic-ionascu.gitlab.io/RnDMetrics/
   - Or locally: http://localhost:8888/public/dashboard.html
3. **Updates**: Dashboard updates when metrics are recollected

---
Generated: 2026-01-28 | RnDMetrics v2.0
