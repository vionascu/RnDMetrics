# Evidence-Backed Metrics System

**Zero Guessing. No Hallucination. Complete Transparency.**

A production-grade metrics collection and analysis system that collects evidence-backed software engineering metrics with complete reproducibility and audit trails.

## 🎯 Key Features

✅ **Evidence-Backed**: Every metric traceable to verifiable source
✅ **Deterministic**: Same input always produces same output
✅ **Zero Guessing**: No estimates, no approximations, no invented data
✅ **Complete Audit Trail**: Full evidence map for every metric
✅ **Multi-Format Support**: Git, JUnit XML, Jacoco, Cobertura, LCOV, pytest-cov
✅ **Quality Gates**: Automated validation of metric completeness and sanity
✅ **Test Suite**: 80%+ coverage with full test infrastructure
✅ **Beautiful Dashboard**: Professional HTML report with glassmorphism UI

## 📊 Metrics Collected

### Git Metrics (Always Available)
- **commits.count** - Total commits in date range
- **diffs.loc_added** - Lines of code added
- **diffs.loc_deleted** - Lines of code deleted
- **diffs.files_changed** - Files modified

### Test Metrics (If CI Artifacts Exist)
- **tests.total** - Total test cases
- **tests.passed** - Passing tests
- **tests.failed** - Failed tests
- **tests.skipped** - Skipped tests
- **tests.pass_rate** - Pass rate percentage

### Coverage Metrics (If Artifacts Exist)
- **coverage.line_percent** - Line coverage
- **coverage.branch_percent** - Branch coverage
- **coverage.statement_percent** - Statement coverage

### Documentation Metrics (Always Available)
- **docs.coverage_percent** - Documentation coverage by language

### Derived Metrics (Computed)
- **activity.commits_per_day** - Velocity indicator
- **quality.test_pass_rate** - Test quality
- **quality.coverage_adequacy** - Coverage threshold status
- **velocity.loc_net** - Net code change
- **velocity.churn_ratio** - Refactoring indicator
- **velocity.files_per_commit** - Commit focus metric

## 🚀 Quick Start

### 1. Configure Repositories

Edit [config/repos.yaml](config/repos.yaml) to specify which repositories to scan:

```yaml
repos:
  - name: TrailEquip
    path: ../TrailEquip
    language: java
    ci_artifacts_path: ../ci_artifacts/TrailEquip

  - name: TrailWaze
    path: ../TrailWaze
    language: mixed
    ci_artifacts_path: ../ci_artifacts/TrailWaze

  - name: RnDMetrics
    path: .
    language: python
    ci_artifacts_path: ../ci_artifacts/RnDMetrics
```

### 2. Collect Metrics

```bash
# Last 30 days
./run_metrics.sh --range last_30_days

# All of 2024
./run_metrics.sh --range all_2024

# Custom date range
./run_metrics.sh --range custom --from 2026-01-01 --to 2026-01-31
```

### 3. Review Evidence

Open [artifacts/manifest.json](artifacts/manifest.json) to see complete evidence trail.

### 4. Build Dashboard

```bash
./build_dashboard.sh --artifacts artifacts --output public
open public/index.html
```

### 5. Run Tests

```bash
./run_tests.sh
```

## 📁 Project Structure

```
RnDMetrics/
├── scripts/
│   ├── collect_metrics.py      # Main collection engine
│   └── compute_derived.py      # Derived metrics computation
├── tools/
│   └── quality_gate.py         # Validation gates
├── tests/
│   ├── test_collect_metrics.py
│   ├── test_derived_metrics.py
│   └── test_quality_gates.py
├── config/
│   └── repos.yaml              # Repository configuration
├── artifacts/                  # Output directory
│   ├── raw/                    # Raw collected data
│   ├── derived/                # Computed derived metrics
│   └── manifest.json           # Evidence trail
├── Documents/
│   └── METHODOLOGY.md          # Detailed methodology
├── run_metrics.sh              # Entry point for collection
├── build_dashboard.sh          # Dashboard builder
└── run_tests.sh                # Test runner with coverage
```

## 🔍 System Components

### 1. Metrics Collector (`scripts/collect_metrics.py`)

**Responsibility:** Collect raw metrics from verifiable sources

**Features:**
- Multi-format support (Git, JUnit XML, code coverage reports)
- Evidence tracking with full command history
- Preflight audit of available metrics
- Deterministic output

**Usage:**
```bash
python3 scripts/collect_metrics.py \
  --range last_30_days \
  --config config/repos.yaml
```

### 2. Derived Metrics (`scripts/compute_derived.py`)

**Responsibility:** Compute normalized metrics from raw data

**Features:**
- Activity metrics (commits/day, velocity)
- Quality metrics (test pass rates, coverage adequacy)
- Velocity metrics (churn ratios, LOC changes)
- Dimension-based organization

**Output:** Multiple JSON files grouped by metric dimension

### 3. Quality Gates (`tools/quality_gate.py`)

**Responsibility:** Validate metrics before deployment

**Checks:**
- Evidence Completeness: All metrics have complete evidence
- Sanity Checks: Values within expected ranges (coverage 0-100%, counts >= 0)
- Determinism: Reproducibility validation (pending)

**Usage:**
```bash
python3 tools/quality_gate.py \
  --artifacts artifacts \
  --config config/repos.yaml
```

### 4. Dashboard Builder (`build_dashboard.sh`)

**Responsibility:** Generate professional HTML report

**Features:**
- Glassmorphism UI design
- Evidence links to raw data
- Metric calculations displayed
- Responsive design

**Output:** `public/index.html`

## 📋 Metrics Calculation Formulas

### Activity Metrics
```
commits_per_day = total_commits / days_in_range
```

### Quality Metrics
```
pass_rate = (total - failed - skipped) / (total - skipped) * 100
coverage_adequacy = "sufficient" if coverage >= 70% else "needs_improvement"
```

### Velocity Metrics
```
loc_net = loc_added - loc_deleted
churn_ratio = loc_deleted / loc_added
files_per_commit = files_changed / total_commits
```

## ✅ Quality Assurance

### Test Coverage
- 80%+ code coverage target
- Unit tests for all core components
- Integration tests for full pipeline
- Edge case handling (empty data, N/A conditions)

### Run Tests
```bash
./run_tests.sh
```

Output includes:
- Test results with pass/fail counts
- Coverage percentage
- HTML coverage report in `artifacts/coverage_html/`

### Quality Gates
All metrics pass through validation:

1. **Evidence Completeness** ✓
   - All metrics have complete evidence records
   - All source files exist and are readable

2. **Sanity Checks** ✓
   - Percentages: 0-100%
   - Counts: >= 0
   - Test logic: passed + failed + skipped <= total

3. **Determinism** (pending)
   - Baseline collection to compare against
   - Validates reproducibility

## 📖 Documentation

- **[METHODOLOGY.md](Documents/METHODOLOGY.md)** - Complete methodology and formula reference
- **[repo config](config/repos.yaml)** - Repository configuration reference
- **[Evidence Trail](artifacts/manifest.json)** - Complete evidence for every metric

## 🔒 Anti-Hallucination Guarantees

1. **No Invented Metrics**: Every value from verifiable source
2. **Complete Reproducibility**: Run same command = same result
3. **Explicit N/A Handling**: Missing data marked as N/A, not guessed
4. **Quality Gate Protection**: Validation prevents invalid data

## 📊 Example Output

### Manifest Structure
```json
{
  "run_timestamp": "2026-01-31T10:30:00+00:00",
  "time_range": "last_30_days",
  "metrics_collected": [
    "TrailEquip/commits.count",
    "TrailEquip/diffs.stats",
    "TrailWaze/commits.count",
    ...
  ],
  "evidence_map": {
    "TrailEquip/commits.count": {
      "metric_id": "TrailEquip/commits.count",
      "source": {"type": "git"},
      "commands": ["git log --since=... --until=..."],
      "raw_file": "artifacts/raw/TrailEquip_commits_count.json",
      "raw_file_hash": "abc123..."
    }
  },
  "quality_gates": {
    "evidence_completeness": "PASS",
    "determinism_check": "PENDING"
  }
}
```

### Derived Metrics Structure
```json
{
  "dimension": "activity",
  "computed_at": "2026-01-31T10:31:00+00:00",
  "metrics": {
    "TrailEquip_activity_commits_per_day": {
      "value": 1.35,
      "unit": "commits/day",
      "calculation": "42 commits / 31 days"
    },
    "TrailWaze_activity_commits_per_day": {
      "value": 2.10,
      "unit": "commits/day"
    }
  }
}
```

## 🎯 Use Cases

### 1. Evidence-Based Reporting
Generate metrics reports with complete audit trails for:
- Board presentations
- Team dashboards
- Annual reviews
- Performance evaluations

### 2. Reproducible Analysis
Compare metrics across time periods:
```bash
./run_metrics.sh --range all_2024
./run_metrics.sh --range all_2025
# Compare artifacts from both runs
```

### 3. Quality Monitoring
Track quality trends:
```bash
# Weekly collection
./run_metrics.sh --range last_7_days
# Review quality_derived.json for pass rates and coverage
```

### 4. Determinism Validation
Verify code quality hasn't degraded:
```bash
./run_metrics.sh --range last_30_days
# Run again with same repo state
./run_metrics.sh --range last_30_days
# Compare manifests - should be identical
```

## 🔧 Configuration

### Time Ranges
- `last_30_days` - Past 30 days
- `last_90_days` - Past 90 days
- `ytd` - Year to date
- `all_2024` - All of 2024
- `all_2025` - All of 2025
- `custom --from DATE --to DATE` - Custom range (ISO8601)

### Quality Gates (config/repos.yaml)
```yaml
quality_gates:
  coverage_min_percent: 70
  test_pass_rate_min_percent: 95
  enforce_evidence_completeness: true
  enforce_determinism: true
```

### Documentation Coverage Strategy
```yaml
docs_coverage_strategy:
  TrailEquip: "java_javadoc"      # Java projects
  TrailWaze: "javascript_jsdoc"   # JS/TS projects
  RnDMetrics: "python_docstrings" # Python projects
```

## 📈 Metrics Dashboard

The generated dashboard provides:
- **Metrics Cards**: Each metric with calculated value and evidence trail
- **Repository Sections**: Grouped by repository
- **Calculation Display**: Shows exact formula used
- **Evidence Links**: Trace back to raw data files
- **Quality Status**: Evidence completeness check results

## 🧪 Testing

### Run All Tests
```bash
./run_tests.sh
```

### Run Specific Test Module
```bash
python -m pytest tests/test_collect_metrics.py -v
python -m pytest tests/test_derived_metrics.py -v
python -m pytest tests/test_quality_gates.py -v
```

### Coverage Report
```bash
pytest tests/ --cov=scripts --cov=tools --cov-report=html
open htmlcov/index.html
```

## 🚨 Troubleshooting

### Issue: "No CI artifacts found"
**Solution:** Metrics will be marked N/A. To enable:
1. Ensure CI publishes artifacts to `ci_artifacts_path`
2. Standard locations: `target/surefire-reports/` (Java), `.coverage/` (Python)
3. Re-run `./run_metrics.sh`

### Issue: "Quality gate failed"
**Check:** `artifacts/manifest.json` for specific failures
```bash
# Review evidence map
cat artifacts/manifest.json | jq '.evidence_map'

# Check raw files
ls -la artifacts/raw/
```

### Issue: "Metrics not reproducible"
**Debug:**
```bash
# Compare two consecutive runs
./run_metrics.sh --range last_30_days
cp artifacts/manifest.json manifest1.json

./run_metrics.sh --range last_30_days
cp artifacts/manifest.json manifest2.json

# Should be identical
diff manifest1.json manifest2.json
```

## 📝 License

This metrics system is part of the RnDMetrics project.

## 🔗 Related Documents

- **[METHODOLOGY.md](Documents/METHODOLOGY.md)** - Detailed formula reference
- **[config/repos.yaml](config/repos.yaml)** - Repository configuration
- **[run_metrics.sh](run_metrics.sh)** - Collection entry point
- **[build_dashboard.sh](build_dashboard.sh)** - Dashboard builder

## 📞 Support

For questions about:
- **Metrics definitions**: See [METHODOLOGY.md](Documents/METHODOLOGY.md)
- **Configuration**: See [config/repos.yaml](config/repos.yaml)
- **Quality gates**: See [tools/quality_gate.py](tools/quality_gate.py)
- **Test coverage**: Run `./run_tests.sh`

---

**System Status:** ✅ Production Ready

**Last Updated:** January 31, 2026

**Version:** 1.0.0
