# Evidence-Backed Metrics Methodology

## Overview

This document describes the methodology behind the Evidence-Backed Metrics system. Every metric is computed deterministically from verifiable sources. No guessing, no estimation, no hallucination.

**Anti-Hallucination Contract:**
1. You MUST NOT invent, guess, estimate, or approximate any metric. Ever.
2. Every number shown must be reproducible from a verifiable source-of-truth.
3. All computation must be deterministic (same input = same output, always).
4. Complete evidence trail must be preserved for every metric.

---

## Metric Categories

### 1. Git Metrics (Always Available)

These metrics are computed directly from repository git history. They are reproducible and deterministic.

#### `commits.count`
**Definition:** Total number of commits in the specified date range.

**Source:** `git log --since=<date> --until=<date> --format=%H`

**Calculation:** Count unique commit hashes returned by git log.

**Range:** Any valid ISO8601 date range.

**Example:**
- Date range: 2026-01-01 to 2026-01-31
- Command: `git log --since=2026-01-01T00:00:00+00:00 --until=2026-01-31T23:59:59+00:00 --format=%H`
- Output: 42 commits
- Verification: Run same command again = 42 commits (deterministic ✓)

**Determinism Guarantee:**
- Input: Repository at specific commit SHA, date range
- Output: Identical commit count across multiple runs (as long as repository history unchanged)
- Non-determinism check: Would fail if running on different repository states

---

#### `diffs.loc_added` / `diffs.loc_deleted` / `diffs.files_changed`
**Definition:** Lines of code added, deleted, and files modified in the date range.

**Source:** `git diff --since=<date> --until=<date> --shortstat`

**Calculation:**
- Parse shortstat output for "files changed", "insertions", "deletions"
- Example output: `10 files changed, 250 insertions(+), 100 deletions(-)`
- Extract: files_changed=10, loc_added=250, loc_deleted=100

**Precision Note:**
- Measures only *changed* lines (not total LOC)
- Binary files excluded
- Does NOT count net change (that's a derived metric)

**Example:**
```bash
$ git diff --since=2026-01-01 --until=2026-01-31 --shortstat
10 files changed, 250 insertions(+), 100 deletions(-)

Extracted metrics:
- diffs.files_changed = 10
- diffs.loc_added = 250
- diffs.loc_deleted = 100
```

**Determinism Guarantee:**
- Same as commits: deterministic if repository history unchanged
- Regenerate manifest with same date range = identical numbers

---

### 2. Test Metrics (If CI Artifacts Exist)

These metrics are extracted from CI build artifacts (JUnit XML reports). Available only if artifacts exist.

#### `tests.total` / `tests.passed` / `tests.failed` / `tests.skipped`
**Definition:** Test counts extracted from JUnit XML reports.

**Source:** JUnit XML files in `ci_artifacts_path` directory

**Parsing Logic:**
1. Find all `TEST-*.xml` files in ci_artifacts_path (standard Maven/Surefire format)
2. For each XML file:
   - Read `<testsuite>` elements
   - Extract attributes: `tests`, `failures`, `skipped`
   - Sum across all suites
3. Alternative: Parse individual `<testcase>` elements
   - Count `<testcase>` with no child elements = passed
   - Count `<testcase>` with `<failure>` child = failed
   - Count `<testcase>` with `<skipped>` child = skipped

**Accuracy:**
- Depends on CI system properly writing JUnit XML
- Standard Maven, Gradle, JUnit 4/5 all produce compatible XML
- Coverage: "Should reflect what the CI system reports"

**Quality Gate Validation:**
- `passed + failed + skipped <= total` (data consistency check)
- All counts >= 0 (sanity check)

**Example JUnit File:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="api-tests" tests="100" failures="3" skipped="2">
  <testcase name="test_login_success"/>
  <testcase name="test_password_reset"><failure/></testcase>
  <testcase name="test_email_validation"><skipped/></testcase>
</testsuite>

Extracted:
- tests.total = 100
- tests.failed = 3
- tests.skipped = 2
- tests.passed = 100 - 3 - 2 = 95
```

**Determinism Guarantee:**
- Same JUnit file = same parsed numbers (always)
- Regenerate with same CI artifacts = identical metrics

**N/A Condition:**
- CI artifacts not found in configured path → marked N/A
- Reason: "No JUnit XML files found"
- To enable: Ensure CI publishes artifacts to configured location

---

#### `tests.pass_rate`
**Definition:** Percentage of non-skipped tests that passed.

**Formula:**
```
pass_rate = (total - failed - skipped) / (total - skipped) * 100
```

**Rationale:**
- Skipped tests excluded (not pass/fail)
- Only meaningful to compare passed vs failed among executed tests
- Example: 100 total, 90 passed, 5 failed, 5 skipped
  - pass_rate = (100 - 5 - 5) / (100 - 5) * 100 = 90 / 95 * 100 = 94.7%

**Quality Gate:** Must be 0-100%

---

### 3. Coverage Metrics (If Artifacts Exist)

Code coverage extracted from CI reports. Supports Jacoco (Java), Cobertura, LCOV, pytest-cov.

#### `coverage.statement_percent` / `coverage.line_percent` / `coverage.branch_percent`
**Definition:** Code coverage percentages by different coverage types.

**Supported Formats:**
- **Jacoco XML**: Parses `<counter type="LINE" covered="X" missed="Y"/>`
- **Cobertura XML**: Similar counter structure
- **LCOV (.info)**: Text format with `LH:` (lines hit) and `LF:` (lines found)
- **pytest-cov / coverage.py**: `.coverage` binary format (requires tool to parse)

**Parsing Logic:**
1. Scan ci_artifacts_path for coverage files
2. Detect format by filename or XML element type
3. Extract coverage percentages
4. Store per coverage type (line, branch, statement)

**Formula (for coverage types with counters):**
```
coverage_percent = covered / (covered + missed) * 100
```

**Example Jacoco XML:**
```xml
<counter type="LINE" covered="450" missed="50"/>
<counter type="BRANCH" covered="80" missed="20"/>

Extracted:
- coverage.line_percent = 450 / 500 * 100 = 90%
- coverage.branch_percent = 80 / 100 * 100 = 80%
```

**Quality Gate:** Must be 0-100%

**Adequacy Threshold:**
- `>= 70%`: Marked as "sufficient"
- `< 70%`: Marked as "needs_improvement"
(Configurable in quality_gates)

---

### 4. Documentation Coverage (Always Available)

Language-specific documentation scanning.

#### `docs.coverage_percent`
**Definition:** Percentage of public functions/classes with documentation.

**Python Implementation (`python_docstrings`):**
1. Find all Python files: `**/*.py`
2. Count functions: regex `def \w+`
3. Count classes: regex `class \w+`
4. Count docstrings: regex `"""..."""` or `'''...'''`
5. Coverage = docstrings / (functions + classes) * 100

**Java Implementation (`java_javadoc`):**
1. Find all Java files: `**/*.java`
2. Count public methods and classes: regex `public.*?class\s+\w+|public.*?\s+\w+(`
3. Count Javadoc: regex `/\*\*.*?\*/`
4. Coverage = javadoc / public_items * 100

**JavaScript/TypeScript Implementation (`javascript_jsdoc`):**
1. Find: `**/*.js`, `**/*.ts`, `**/*.tsx`
2. Count exports: regex `export\s+(async\s+)?function|export\s+const.*=`
3. Count JSDoc: regex `/\*\*.*?\*/`
4. Coverage = jsdoc / exports * 100

**Limitations:**
- Regex-based (not AST parsing) → approximate counts
- Can't distinguish public vs private perfectly
- Edge cases: inline documentation, README docs not counted
- Use this as guidance, not gospel truth

**Quality Gate:** Must be 0-100%

---

## Derived Metrics

Derived metrics are computed from raw metrics. They normalize and combine data.

### Activity Metrics

#### `activity.commits_per_day`
**Formula:**
```
commits_per_day = total_commits / days_in_range
```

**Example:**
- Raw: 30 commits in January (31 days)
- Derived: 30 / 31 = 0.97 commits/day

**Interpretation:**
- Trend indicator: ↑ increasing, ↓ decreasing, → stable
- Compares current vs previous period

---

### Quality Metrics

#### `quality.test_pass_rate`
**Source Metric:** `tests.pass_rate`
**Formula:** Direct copy (already normalized 0-100%)

---

#### `quality.coverage_adequacy`
**Source Metric:** `coverage.line_percent`
**Formula:** Threshold comparison
```
adequacy = "sufficient" if coverage >= 70 else "needs_improvement"
```

---

### Velocity Metrics

#### `velocity.loc_net`
**Formula:**
```
loc_net = loc_added - loc_deleted
```

**Interpretation:**
- Positive: Net code growth
- Negative: Net code reduction (refactoring/cleanup)
- Zero: Equal changes

---

#### `velocity.churn_ratio`
**Formula:**
```
churn_ratio = loc_deleted / loc_added
```

**Interpretation:**
- High ratio (>0.5): Heavy refactoring/rework
- Low ratio (<0.2): Focused additions with minimal cleanup
- Ratio > 1: More deletions than additions (code shrinking)

---

#### `velocity.files_per_commit`
**Formula:**
```
files_per_commit = files_changed / total_commits
```

**Interpretation:**
- Low (<2): Focused, small commits
- High (>5): Large, broad commits

---

## Evidence Preservation

Every metric has complete evidence trail.

### Evidence Record Structure
```json
{
  "metric_id": "TrailEquip/commits.count",
  "repo": "TrailEquip",
  "range": {
    "from": "2026-01-01T00:00:00+00:00",
    "to": "2026-01-31T23:59:59+00:00",
    "timezone": "UTC"
  },
  "collected_at": "2026-01-31T10:30:00+00:00",
  "collector_version": "a1b2c3d",
  "source": {
    "type": "git",
    "details": "/path/to/TrailEquip"
  },
  "commands": [
    "git log --since=2026-01-01T00:00:00+00:00 --until=2026-01-31T23:59:59+00:00 --format=%H"
  ],
  "raw_file": "artifacts/raw/TrailEquip_commits_count.json",
  "raw_file_hash": "abc123def456...",
  "derived_file": "artifacts/derived/activity_derived.json"
}
```

### Reproducibility Checks

To verify a metric:

1. **Extract command** from evidence: `"git log --since=... --until=... --format=%H"`
2. **Navigate to repo:** `cd /path/to/repo`
3. **Run command:** `git log --since=... --until=... --format=%H | wc -l`
4. **Compare result:** Should match reported count

**Example Reproduction:**
```bash
# Verify "TrailEquip/commits.count = 42" from manifest
cd ../TrailEquip
git log --since=2026-01-01T00:00:00+00:00 --until=2026-01-31T23:59:59+00:00 --format=%H | wc -l
# Output: 42 ✓ (matches)
```

---

## Quality Gates

Metrics pass through multiple validation gates.

### Gate 1: Evidence Completeness
**Check:** All metrics have complete evidence records
- ✓ PASS: Every metric has metric_id, repo, range, collected_at, commands, raw_file
- ✗ FAIL: Any metric missing required fields → reject batch

### Gate 2: Sanity Checks
**Check:** Metric values within expected ranges
- Percentages: 0-100
- Counts: >= 0
- Test logic: passed + failed + skipped <= total

**Violations:**
- coverage = 150% → FAIL
- commits = -5 → FAIL
- tests: passed=90, failed=20, skipped=5, total=100 (90+20+5>100) → FAIL

### Gate 3: Determinism Check
**Check:** Consecutive collection runs produce identical results (if repo unchanged)

**Process:**
1. Run collection twice
2. Compare all metric values
3. All must be identical

**Non-deterministic Sources (would fail):**
- Random number generation
- Timestamps in metric values
- System-dependent output
- Non-deterministic sort order

**Current Status:** Pending (requires historical baseline)

---

## Configuration

### repos.yaml Structure

```yaml
repos:
  - name: TrailEquip
    path: ../TrailEquip           # Path to repo (relative to config)
    default_branch: main
    language: java                # For docs scanning
    ci_artifacts_path: ../ci_artifacts/TrailEquip
    description: "..."

docs_coverage_strategy:
  TrailEquip: "java_javadoc"      # Language-specific strategy

quality_gates:
  coverage_min_percent: 70        # Minimum allowed coverage
  test_pass_rate_min_percent: 95  # Minimum allowed pass rate
  enforce_evidence_completeness: true
  enforce_determinism: true
```

---

## Time Ranges

### Preset Ranges
- **last_30_days**: Past 30 days from now
- **last_90_days**: Past 90 days from now
- **ytd**: Year to date (Jan 1 to today of current year)
- **all_2024**: All of 2024 (Jan 1 - Dec 31, 2024)
- **all_2025**: All of 2025 (Jan 1 - Dec 31, 2025)
- **custom**: User-specified start and end dates (ISO8601 format)

### Date Format
All dates are ISO8601 with UTC timezone:
- `2026-01-31T23:59:59+00:00`
- `2026-01-31T00:00:00Z` (Z = UTC)

### Implementation
```python
def compute_date_range(time_range):
    now = datetime.now(timezone.utc)
    if time_range == "last_30_days":
        from_dt = now - timedelta(days=30)
        to_dt = now
    elif time_range == "all_2024":
        from_dt = datetime(2024, 1, 1, tzinfo=timezone.utc)
        to_dt = datetime(2025, 1, 1, tzinfo=timezone.utc)
    # ...
    return from_dt.isoformat(), to_dt.isoformat()
```

---

## Artifacts Structure

```
artifacts/
├── raw/                          # Raw collected data
│   ├── TrailEquip_commits_count.json
│   ├── TrailEquip_diffs_stats.json
│   ├── TrailEquip_tests_summary.json
│   ├── TrailEquip_coverage_summary.json
│   ├── TrailEquip_docs_coverage.json
│   └── ... (same for other repos)
├── derived/                      # Computed derived metrics
│   ├── activity_derived.json     # commits_per_day, etc.
│   ├── quality_derived.json      # pass_rate, coverage adequacy
│   ├── velocity_derived.json     # churn ratio, files/commit, net LOC
│   └── derived_manifest.json
├── logs/                         # Collection logs (if applicable)
├── report/                       # Generated HTML report
│   └── index.html
└── manifest.json                 # Master manifest with evidence trail
```

### manifest.json Structure
```json
{
  "run_timestamp": "2026-01-31T10:30:00+00:00",
  "time_range": "last_30_days",
  "date_from": "2026-01-01T00:00:00+00:00",
  "date_to": "2026-01-31T00:00:00+00:00",
  "timezone": "UTC",
  "preflight": {...},               # Preflight audit results
  "metrics_collected": [...],       # List of metric IDs collected
  "evidence_map": {...},            # Evidence for each metric
  "quality_gates": {
    "evidence_completeness": "PASS",
    "determinism_check": "PENDING"
  }
}
```

---

## Running the System

### One-Command Collection
```bash
# Collect last 30 days with all default settings
./run_metrics.sh --range last_30_days

# Collect all of 2024
./run_metrics.sh --range all_2024

# Custom date range
./run_metrics.sh --range custom --from 2026-01-01 --to 2026-01-31

# Collect, derive, validate, and build dashboard
./run_metrics.sh --range last_30_days && ./build_dashboard.sh
```

### Output
```
artifacts/
├── raw/          # Raw metrics (verifiable sources)
├── derived/      # Normalized derived metrics
└── manifest.json # Complete evidence trail
```

### Test Suite
```bash
# Run tests with 80% coverage requirement
./run_tests.sh

# Output: artifacts/coverage.json and coverage_html/
```

---

## Anti-Hallucination Guarantees

1. **No Invented Metrics**
   - Every number comes from verifiable source (git, CI artifacts, code scan)
   - No estimated values
   - No filled-in defaults

2. **Complete Reproducibility**
   - Run collection again with same params = identical results
   - Run reported command manually = matches reported value
   - Evidence trail allows full audit

3. **Explicit N/A Handling**
   - If data unavailable (no CI artifacts), marked N/A with reason
   - Not filled in with guesses
   - Can be enabled when sources become available

4. **Quality Gate Protection**
   - Evidence completeness enforced
   - Sanity checks prevent invalid values
   - Determinism checks catch non-reproducible bugs

---

## Known Limitations

1. **Documentation Coverage:** Regex-based scanning (not AST) → approximate counts
2. **AI Code Detection:** No explicit signals tracked (would require commit metadata or code signatures)
3. **Hotspot Analysis:** Not yet implemented (would require line-level blame data)
4. **Time Span Bias:** Metrics only available for repos with git history during selected range
5. **Binary Files:** Excluded from LOC counts (git limitation)

---

## Future Enhancements

1. **Determinism Verification:** Baseline storage and comparison
2. **Historical Comparison:** Track metrics over time
3. **Anomaly Detection:** Identify unusual metric changes
4. **Custom Metrics:** Plugin system for repo-specific metrics
5. **Integration:** Slack/email notifications, web dashboard
6. **Archive:** Long-term metrics storage and analysis

---

**Document Version:** 1.0
**Last Updated:** January 31, 2026
**Status:** Production Ready
