# Metrics Quick Reference Guide
## Fast Lookup for Metric Definitions and Formulas

---

## Core Metrics

### 📊 Lines of Code (LOC)
**What:** Total lines of source code
**Formula:** `SUM(lines in all source files) - blank lines`
**Includes:** All source files except tests and build artifacts
**Example:** TrailEquip = 50,000 LOC
**Update Frequency:** Daily with collection cycle

---

### 📁 File Count
**What:** Number of source files
**Formula:** `COUNT(source files with valid extensions)`
**Extensions:** .java, .py, .js, .ts, .tsx, .jsx, .go, .rs, .rb, .php, .sql
**Example:** TrailEquip = 342 files
**Update Frequency:** Daily with collection cycle

---

### 🌳 Branch Count
**What:** Number of active development branches
**Formula:** `COUNT(branches with commits in last 30 days)`
**Example:** TrailEquip = 8 active branches
**Update Frequency:** Daily with collection cycle

---

## AI & Automation Metrics

### 🤖 AI-Generated Code %
**What:** Percentage of commits detected as AI-generated
**Formula:** `(AI-detected commits / total commits) × 100`
**Detection Method:** Keyword analysis in commit messages
**Keywords:** "copilot", "chatgpt", "claude", "ai generated", "auto-generated", etc.
**Accuracy:** 85-90% confidence
**Example:** TrailEquip = 25% AI
**Range:** 0-100%

**Critical Insight:**
- No correlation with quality degradation
- Same test pass rates (100%) for AI and human code
- Quality scores: 8.7-9.2/10 regardless of origin

---

### ⚡ Code Velocity Improvement
**What:** Percentage increase in development speed with AI
**Formula:** `((Current Velocity - Baseline Velocity) / Baseline Velocity) × 100`
**Components:** Features + Bug Fixes + LOC Generated
**Baseline:** Q4 2025 (pre-AI)
**Current:** Q1 2026 (with AI)
**Example:** +42% improvement
**Expected Range:** +30-60% (depending on team composition)

**Calculation Details:**
```
Baseline (Q4): 12 features + 34 bugs + 175K LOC
Current (Q1):  17 features + 41 bugs + 248K LOC
Improvement:   +42%
```

---

### 🔧 Automation Improvement %
**What:** Percentage improvement in process automation
**Formula:** `Average of (test automation, deployment automation, build speed, success rate)`
**Metrics Tracked:**
- Test Automation: 85% → 99% (+16.5%)
- Deploy Automation: 60% → 100% (+66.7%)
- Build Speed: 5.2m → 4.2m (+19.2%)
- Build Success: 98.5% → 99.8% (+1.3%)

**Example:** +34% overall improvement
**Expected Range:** +20-50%

---

## Quality Metrics

### ✅ Test Coverage
**What:** Percentage of code executed by tests
**Formula:** `(Statements Covered / Total Statements) × 100`
**Types:**
- Line Coverage: 85%
- Branch Coverage: 80%
- Function Coverage: 90%

**By Project:**
- TrailEquip: 100% ✅
- TrailWaze: 85% 🟡
- RnDMetrics: 75% 🟡

**Update Frequency:** Per test run (CI pipeline)
**Target:** ≥85%

---

### 📚 Documentation Coverage
**What:** Percentage of components with documentation
**Formula:** `(Components with Docs / Total Components) × 100`
**Doc Types Checked:**
- README.md
- API Documentation
- Architecture Guide
- Examples
- Setup Guide

**By Project:**
- RnDMetrics: 98% ⭐
- TrailEquip: 95% ⭐
- TrailWaze: 88% 🟡

**Update Frequency:** Upon documentation changes
**Target:** ≥90%

---

### 🎯 Code Quality Score
**What:** Overall code quality rating
**Formula:**
```
Quality Score = (Coverage × 0.35)
              + (Complexity × 0.25)
              + (Documentation × 0.20)
              + (Build Success × 0.15)
              + (Review Compliance × 0.05)
```
**Scale:** 0-10 (10 = perfect)

**By Project:**
- TrailEquip: 9.2/10 ⭐
- TrailWaze: 8.7/10 ⭐
- RnDMetrics: 9.1/10 ⭐

**Target:** ≥8.0/10

---

## Feature & Coverage Metrics

### 🎯 Feature Coverage
**What:** Percentage of features with passing tests
**Formula:** `(Features with Tests / Total Features) × 100`
**Overall:** 54/62 features = 87%

**Fully Covered (54 features):**
- Trail Management: 9 tests
- Weather Forecasting: 6 tests
- Equipment Recommendations: 8 tests
- User Authentication: 12 tests
- Trail Discovery: 18 tests
- (+ 10 more)

**Uncovered (8 features):**
1. Advanced Filters - HIGH priority
2. Export Functionality - HIGH priority
3. Push Notifications - MEDIUM priority
4. Social Sharing - MEDIUM priority
5. Analytics Dashboard - MEDIUM priority
6. Batch Operations - LOW priority
7. Real-time Sync - LOW priority
8. Offline Mode - LOW priority

**Action:** Allocate 1 dev for 5 weeks to close gaps

---

### 📈 Feature Testing Priority
**What:** Ranking of uncovered features by importance
**Formula:** `Priority = Impact Weight / Effort`

**Impact Weights:**
- HIGH (user-facing): 10 points
- MEDIUM (system): 5 points
- LOW (administrative): 1 point

**Example:**
```
Advanced Filters: 10 / 1.5 days = 6.67 priority
Export: 10 / 1.5 days = 6.67 priority
Push Notifications: 5 / 2 days = 2.5 priority
```

---

## Refactoring Metrics

### 🔄 Legacy Code Refactored %
**What:** Percentage of legacy code that has been modernized
**Formula:** `(LOC Modernized / Total Legacy LOC) × 100`
**Example:** 45K of 250K = 18%
**Timeline:** 42 events over 12 months
**Pace:** 3,750 LOC/month
**Projected Completion:** Q3 2026

**Modules Status:**
- ✅ Authentication: 3 refactors (Modernized)
- ✅ Database Layer: 2 refactors (Updated)
- 🔄 API Gateway: 1 refactor (In Progress)
- ❌ Frontend Components: 0 refactors (PENDING)
- ❌ Reporting Module: 0 refactors (PENDING)

---

### 📊 Refactoring Frequency
**What:** How often refactoring occurs
**Formula:** `Number of Refactoring Commits / Time Period`
**Example:** 42 events / 12 months = 3.5/month average
**Trend:** Consistent monthly frequency

---

## Velocity & Performance

### ⚙️ Build Success Rate
**What:** Percentage of builds that succeed
**Formula:** `(Successful Builds / Total Build Attempts) × 100`
**Example:** 99.8%
**Target:** ≥99%
**Update Frequency:** Per build (multiple per day)

---

### 🚀 Deployment Frequency
**What:** How often code is deployed to production
**Example:** Multiple times per day
**Average Deploy Time:** 15 minutes
**Rollback Time:** <2 minutes
**Automation Level:** 100%

---

### ⏱️ Build Duration
**What:** Time to complete full build pipeline
**Baseline (Q4):** 5.2 minutes
**Current (Q1):** 4.2 minutes
**Improvement:** 19.2% faster
**Target:** <5 minutes

---

## Summary Scorecard

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Code Velocity** | +42% | +30% | ✅ Exceeded |
| **AI Integration** | 28% | 20% | ✅ Above Target |
| **Test Coverage** | 85% | 85% | ✅ At Target |
| **Documentation** | 92% | 90% | ✅ Exceeded |
| **Code Quality** | 8.9/10 | 8.0/10 | ✅ Excellent |
| **Build Success** | 99.8% | 99% | ✅ Excellent |
| **Feature Coverage** | 87% | 90% | 🟡 Close |
| **Legacy Refactored** | 18% | 15% | ✅ Ahead |
| **Automation Gain** | 34% | 25% | ✅ Exceeded |

---

## How Metrics Are Updated

### Collection Cycle
1. **Daily Trigger:** 2 AM UTC (configurable)
2. **Data Pull:** GitHub API queries all commits (past 365 days)
3. **Repository Analysis:** Shallow clone & code analysis
4. **Calculation:** All metrics computed from collected data
5. **Storage:** Snapshot saved to SQLite database
6. **Export:** JSON files generated for dashboard
7. **Display:** Dashboard updated automatically

### Processing Time
- API Queries: 2-5 minutes
- Repository Analysis: 3-10 minutes
- Calculations: <1 minute
- Export: <1 minute
- **Total:** ~10-15 minutes per project

---

## Common Questions

### Q: Why is AI Detection Only 85-90% Accurate?
**A:** Relies on commit message keywords. Some AI code lacks attribution, and some "automated" keywords are false positives. Manual review recommended for borderline cases.

### Q: How Are Features Identified?
**A:** Combination of:
- Analyzing test file names
- Parsing feature branches
- Reading commit messages
- Code file organization

### Q: What If Tests Don't Run in CI?
**A:** Coverage reports must be generated and committed. If not present, coverage is marked as unavailable for that build.

### Q: How Frequently Should Metrics Be Reviewed?
**A:**
- Weekly: Team leads (spot check)
- Biweekly: Managers (trending)
- Monthly: Directors (strategic)
- Quarterly: Executive review

### Q: Can I Export These Metrics?
**A:** Yes! JSON exports available in `output/` folder:
- `latest.json` - Current snapshot
- `history.json` - All historical data

---

## Detailed Formula Reference

### AI Detection Algorithm
```
FOR each commit in past 365 days:
  IF commit.message.contains(ai_keyword):
    confidence = keyword_confidence_score
  ELSE IF code_has_ai_patterns(commit):
    confidence = pattern_confidence
  ELSE:
    confidence = 0

  IF confidence ≥ 0.50:
    ai_commits += 1

ai_percentage = (ai_commits / total_commits) × 100
```

### Quality Score Algorithm
```
score = (
  test_coverage         × 0.35 × 10 +
  complexity_score      × 0.25 × 10 +
  doc_coverage          × 0.20 × 10 +
  build_success_rate    × 0.15 × 10 +
  review_compliance     × 0.05 × 10
) / 10

# Result: 0-10 scale
```

### Feature Coverage Algorithm
```
FOR each feature in feature_list:
  tests = find_tests_for_feature(feature)

  IF tests exist AND all tests pass:
    covered_features += 1
  ELSE:
    uncovered_features.add(feature)

coverage = (covered_features / total_features) × 100
```

---

## Data Sources

| Metric | Source | Format | Frequency |
|--------|--------|--------|-----------|
| Commits | GitHub API | JSON | Daily |
| Code Analysis | Repository Clone | File System | Daily |
| Test Coverage | Coverage Reports | LCOV/XML | Per test run |
| Documentation | File System | Markdown | Upon change |
| Build Status | CI/CD Pipeline | XML | Per build |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Jan 31, 2026 | Initial methodology documentation |

---

**Quick Reference Version:** 1.0.0
**Full Methodology:** See [METRICS_CALCULATION_METHODOLOGY.md](METRICS_CALCULATION_METHODOLOGY.md)
**Dashboard:** [dashboard-executive.html](dashboard-executive.html)
**Report:** [EXECUTIVE_METRICS_REPORT.md](EXECUTIVE_METRICS_REPORT.md)
