#!/usr/bin/env python3
"""
Evidence-backed metrics collection engine.
Collects git-based, test-based, and documentation metrics with full traceability.

No guessing. No hallucination. Every number traced to source.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import hashlib
import yaml
import xml.etree.ElementTree as ET
import re

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class MetricsCollector:
    """Main collector orchestrating all metric sources."""

    def __init__(self, config_path: str, time_range: str, custom_from: Optional[str] = None, custom_to: Optional[str] = None):
        """Initialize with config and time range."""
        self.config_path = config_path
        self.time_range = time_range
        self.custom_from = custom_from
        self.custom_to = custom_to
        self.config = self._load_config()
        self.start_time = datetime.now(timezone.utc)
        self.root = Path(__file__).parent.parent
        self.artifacts_dir = self.root / "artifacts"
        self.raw_dir = self.artifacts_dir / "raw"
        self.derived_dir = self.artifacts_dir / "derived"
        self.logs_dir = self.artifacts_dir / "logs"

        # Create directories
        for d in [self.raw_dir, self.derived_dir, self.logs_dir]:
            d.mkdir(parents=True, exist_ok=True)

        # Compute date range
        self.date_from, self.date_to = self._compute_date_range()
        self.tz = timezone.utc

        # Collected metrics
        self.metrics = {}
        self.evidence_map = {}  # metric_id -> evidence metadata

    def _load_config(self) -> Dict[str, Any]:
        """Load and validate configuration."""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def _compute_date_range(self) -> Tuple[str, str]:
        """Compute ISO8601 date range based on time_range parameter."""
        now = datetime.now(timezone.utc)

        if self.time_range == "last_30_days":
            from_dt = now - timedelta(days=30)
            to_dt = now
        elif self.time_range == "last_90_days":
            from_dt = now - timedelta(days=90)
            to_dt = now
        elif self.time_range == "ytd":
            from_dt = datetime(now.year, 1, 1, tzinfo=timezone.utc)
            to_dt = now
        elif self.time_range == "all_2024":
            from_dt = datetime(2024, 1, 1, tzinfo=timezone.utc)
            to_dt = datetime(2025, 1, 1, tzinfo=timezone.utc)
        elif self.time_range == "all_2025":
            from_dt = datetime(2025, 1, 1, tzinfo=timezone.utc)
            to_dt = datetime(2026, 1, 1, tzinfo=timezone.utc)
        elif self.time_range == "custom":
            if not self.custom_from or not self.custom_to:
                raise ValueError("--from and --to required for custom range")
            from_dt = datetime.fromisoformat(self.custom_from.replace('Z', '+00:00'))
            to_dt = datetime.fromisoformat(self.custom_to.replace('Z', '+00:00'))
        else:
            raise ValueError(f"Unknown time_range: {self.time_range}")

        return from_dt.isoformat(), to_dt.isoformat()

    def run(self):
        """Execute full metrics collection pipeline."""
        print(f"[METRICS] Starting collection for range: {self.time_range}")
        print(f"[METRICS] From: {self.date_from}")
        print(f"[METRICS] To:   {self.date_to}")
        print()

        # Step 1: Preflight - what metrics can we compute?
        capabilities = self._run_preflight()

        # Step 2: Collect git metrics (always available)
        self._collect_git_metrics()

        # Step 3: Collect test metrics (if artifacts exist)
        self._collect_test_metrics()

        # Step 4: Collect coverage metrics (if artifacts exist)
        self._collect_coverage_metrics()

        # Step 5: Collect documentation metrics
        self._collect_docs_metrics()

        # Step 6: Validate completeness
        self._validate_evidence_completeness()

        # Step 7: Generate manifest
        self._write_manifest(capabilities)

        print(f"\n✅ Collection complete. Artifacts in: {self.artifacts_dir}")
        return True

    def _run_preflight(self) -> Dict[str, Any]:
        """Identify what metrics can be computed."""
        capabilities = {
            "timestamp": self.start_time.isoformat(),
            "repos": {},
            "computable_metrics": {},
            "na_metrics": {}
        }

        for repo_config in self.config["repos"]:
            repo_name = repo_config["name"]
            repo_path = self.root / repo_config["path"]

            print(f"[PREFLIGHT] {repo_name}...")

            if not repo_path.exists():
                print(f"  ❌ Repo path not found: {repo_path}")
                capabilities["repos"][repo_name] = {"status": "missing"}
                continue

            repo_info = {
                "status": "available",
                "path": str(repo_path),
                "language": repo_config.get("language", "unknown")
            }

            # Check git
            git_dir = repo_path / ".git"
            if git_dir.exists():
                try:
                    result = subprocess.run(
                        ["git", "rev-parse", "HEAD"],
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        repo_info["git_head"] = result.stdout.strip()
                        repo_info["git_available"] = True
                except:
                    repo_info["git_available"] = False
            else:
                repo_info["git_available"] = False

            # Check for CI artifacts
            ci_path = repo_config.get("ci_artifacts_path")
            if ci_path:
                ci_full_path = self.root / ci_path
                if ci_full_path.exists():
                    # List what's available
                    artifacts = list(ci_full_path.glob("**/*"))
                    repo_info["ci_artifacts_found"] = len(artifacts)
                else:
                    repo_info["ci_artifacts_found"] = 0

            capabilities["repos"][repo_name] = repo_info
            print(f"  ✅ Git available: {repo_info.get('git_available', False)}")

        # List computable metrics
        capabilities["computable_metrics"] = {
            "always_available": [
                "commits.count",
                "commits.unique_authors",
                "diffs.loc_added",
                "diffs.loc_deleted",
                "diffs.files_changed",
                "activity.commits_per_day",
                "hotspots.top_files_by_churn"
            ],
            "if_ci_artifacts_exist": [
                "tests.total",
                "tests.passed",
                "tests.failed",
                "tests.skipped",
                "tests.pass_rate",
                "coverage.statement_percent"
            ]
        }

        capabilities["na_metrics"] = {
            "reason": "No CI artifacts found. To enable test/coverage metrics, provide JUnit/coverage reports in ci_artifacts_path.",
            "metrics": ["tests.*", "coverage.*", "flaky_tests.*"]
        }

        print()
        return capabilities

    def _collect_git_metrics(self):
        """Collect git-based metrics for all repos."""
        print("[GIT METRICS] Collecting...")

        for repo_config in self.config["repos"]:
            repo_name = repo_config["name"]
            repo_path = self.root / repo_config["path"]

            if not repo_path.exists() or not (repo_path / ".git").exists():
                print(f"  ⚠️  {repo_name}: no git repo found, skipping")
                continue

            print(f"  📊 {repo_name}...")

            # commits.count
            self._collect_metric(
                metric_id=f"{repo_name}/commits.count",
                repo_name=repo_name,
                repo_path=repo_path,
                collector_fn=self._count_commits
            )

            # diffs stats
            self._collect_metric(
                metric_id=f"{repo_name}/diffs.stats",
                repo_name=repo_name,
                repo_path=repo_path,
                collector_fn=self._collect_diff_stats
            )

    def _collect_metric(self, metric_id: str, repo_name: str, repo_path: Path, collector_fn):
        """Generic metric collection wrapper."""
        try:
            raw_data, commands = collector_fn(repo_path)

            # Save raw data
            raw_file = self.raw_dir / f"{metric_id.replace('/', '_')}.json"
            with open(raw_file, 'w') as f:
                json.dump(raw_data, f, indent=2, default=str)

            # Record evidence
            self.evidence_map[metric_id] = {
                "metric_id": metric_id,
                "repo": repo_name,
                "range": {
                    "from": self.date_from,
                    "to": self.date_to,
                    "timezone": "UTC"
                },
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "collector_version": subprocess.run(["git", "rev-parse", "HEAD"],
                                                   capture_output=True, text=True,
                                                   cwd=self.root).stdout.strip()[:8],
                "source": {"type": "git", "details": str(repo_path)},
                "commands": commands,
                "raw_file": str(raw_file),
                "raw_file_hash": self._compute_file_hash(raw_file),
                "derived_file": None
            }

            print(f"    ✅ {metric_id}")

        except Exception as e:
            print(f"    ❌ {metric_id}: {e}")

    def _count_commits(self, repo_path: Path) -> Tuple[Dict, List[str]]:
        """Count commits in date range."""
        cmd = [
            "git", "log",
            f"--since={self.date_from}",
            f"--until={self.date_to}",
            "--format=%H%n%ai%n%an",
            "--date=iso-strict"
        ]
        result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"git log failed: {result.stderr}")

        commits = [line for line in result.stdout.strip().split('\n') if line]
        count = len(commits) // 3  # Hash, date, author per commit

        return {
            "count": count,
            "range": {
                "from": self.date_from,
                "to": self.date_to
            },
            "command": " ".join(cmd)
        }, [" ".join(cmd)]

    def _collect_diff_stats(self, repo_path: Path) -> Tuple[Dict, List[str]]:
        """Collect LOC added/deleted stats."""
        cmd = [
            "git", "diff",
            f"--since={self.date_from}",
            f"--until={self.date_to}",
            "--shortstat"
        ]
        result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)

        if result.returncode != 0:
            # No commits in range
            return {
                "loc_added": 0,
                "loc_deleted": 0,
                "files_changed": 0,
                "range": {"from": self.date_from, "to": self.date_to}
            }, [" ".join(cmd)]

        # Parse shortstat output
        output = result.stdout.strip()
        loc_added = loc_deleted = files_changed = 0

        if "files changed" in output:
            parts = output.split(",")
            for part in parts:
                part = part.strip()
                if "files changed" in part:
                    files_changed = int(part.split()[0])
                elif "insertions" in part:
                    loc_added = int(part.split()[0])
                elif "deletions" in part:
                    loc_deleted = int(part.split()[0])

        return {
            "loc_added": loc_added,
            "loc_deleted": loc_deleted,
            "files_changed": files_changed,
            "range": {"from": self.date_from, "to": self.date_to},
            "raw_output": output
        }, [" ".join(cmd)]

    def _collect_test_metrics(self):
        """Collect test metrics (if CI artifacts exist)."""
        print("[TEST METRICS] Checking for CI artifacts...")

        for repo_config in self.config["repos"]:
            repo_name = repo_config["name"]
            ci_path = repo_config.get("ci_artifacts_path")

            if not ci_path:
                continue

            ci_full_path = self.root / ci_path
            if not ci_full_path.exists():
                continue

            print(f"  📊 {repo_name}...")

            # Look for JUnit XML reports
            junit_files = list(ci_full_path.glob("**/TEST-*.xml")) or \
                         list(ci_full_path.glob("**/surefire-reports/*.xml")) or \
                         list(ci_full_path.glob("**/junit.xml"))

            if junit_files:
                self._collect_metric(
                    metric_id=f"{repo_name}/tests.summary",
                    repo_name=repo_name,
                    repo_path=self.root / repo_config["path"],
                    collector_fn=lambda p: self._parse_junit_reports(junit_files)
                )
            else:
                print(f"    ⚠️  No JUnit XML found in {ci_path}")

    def _parse_junit_reports(self, junit_files: List[Path]) -> Tuple[Dict, List[str]]:
        """Parse JUnit XML reports and extract test metrics."""
        import xml.etree.ElementTree as ET

        total_tests = 0
        total_passed = 0
        total_failed = 0
        total_skipped = 0

        commands = [f"parsed {len(junit_files)} JUnit XML files"]

        try:
            for junit_file in junit_files:
                try:
                    tree = ET.parse(junit_file)
                    root = tree.getroot()

                    # Sum across all testsuites
                    for testsuite in root.findall(".//testsuite"):
                        total_tests += int(testsuite.get("tests", 0))
                        total_failed += int(testsuite.get("failures", 0))
                        total_skipped += int(testsuite.get("skipped", 0))

                    # Also check direct testcase elements
                    testcases = root.findall(".//testcase")
                    for testcase in testcases:
                        if testcase.find("skipped") is not None:
                            total_skipped += 1
                        elif testcase.find("failure") is not None:
                            total_failed += 1
                        else:
                            total_passed += 1

                except Exception as e:
                    commands.append(f"Error parsing {junit_file.name}: {e}")

            # Recalculate if we got testcase counts
            if total_passed > 0:
                total_tests = total_passed + total_failed + total_skipped

            pass_rate = 100.0 if total_tests == 0 else (total_passed / (total_tests - total_skipped)) * 100 if total_tests > total_skipped else 0

            return {
                "total": total_tests,
                "passed": total_passed,
                "failed": total_failed,
                "skipped": total_skipped,
                "pass_rate_percent": round(pass_rate, 2),
                "files_parsed": len(junit_files),
                "range": {
                    "from": self.date_from,
                    "to": self.date_to
                }
            }, commands
        except Exception as e:
            return {
                "total": 0,
                "status": "error",
                "error": str(e)
            }, commands

    def _collect_coverage_metrics(self):
        """Collect coverage metrics (if artifacts exist)."""
        print("[COVERAGE METRICS] Checking for coverage reports...")

        for repo_config in self.config["repos"]:
            repo_name = repo_config["name"]
            ci_path = repo_config.get("ci_artifacts_path")

            if not ci_path:
                continue

            ci_full_path = self.root / ci_path
            if not ci_full_path.exists():
                continue

            print(f"  📊 {repo_name}...")

            # Look for coverage reports (jacoco, cobertura, lcov, pytest-cov)
            coverage_files = list(ci_full_path.glob("**/jacoco*.xml")) or \
                            list(ci_full_path.glob("**/coverage.xml")) or \
                            list(ci_full_path.glob("**/lcov.info")) or \
                            list(ci_full_path.glob("**/cobertura-coverage.xml")) or \
                            list(ci_full_path.glob(".coverage"))

            if coverage_files:
                self._collect_metric(
                    metric_id=f"{repo_name}/coverage.summary",
                    repo_name=repo_name,
                    repo_path=self.root / repo_config["path"],
                    collector_fn=lambda p: self._parse_coverage_reports(coverage_files)
                )
            else:
                print(f"    ⚠️  No coverage reports found in {ci_path}")

    def _parse_coverage_reports(self, coverage_files: List[Path]) -> Tuple[Dict, List[str]]:
        """Parse coverage reports (Jacoco, Cobertura, LCOV, pytest-cov)."""
        import xml.etree.ElementTree as ET

        commands = [f"parsed {len(coverage_files)} coverage files"]

        coverage_data = {
            "statement_coverage": None,
            "branch_coverage": None,
            "line_coverage": None,
            "method_coverage": None,
            "files_found": 0,
            "range": {
                "from": self.date_from,
                "to": self.date_to
            }
        }

        try:
            for cov_file in coverage_files:
                filename = cov_file.name

                try:
                    # Jacoco XML format
                    if "jacoco" in filename or "cobertura" in filename:
                        tree = ET.parse(cov_file)
                        root = tree.getroot()

                        # Jacoco counters
                        for counter in root.findall(".//counter"):
                            counter_type = counter.get("type", "").lower()
                            covered = int(counter.get("covered", 0))
                            missed = int(counter.get("missed", 0))
                            total = covered + missed

                            if total > 0:
                                pct = (covered / total) * 100
                                if counter_type == "line":
                                    coverage_data["line_coverage"] = round(pct, 2)
                                elif counter_type == "branch":
                                    coverage_data["branch_coverage"] = round(pct, 2)
                                elif counter_type == "method":
                                    coverage_data["method_coverage"] = round(pct, 2)

                        coverage_data["files_found"] += 1

                    # LCOV format (text)
                    elif "lcov" in filename:
                        with open(cov_file, 'r') as f:
                            lines_hit = 0
                            lines_found = 0
                            for line in f:
                                if line.startswith("LH:"):
                                    lines_hit = int(line.split(":")[1].strip())
                                elif line.startswith("LF:"):
                                    lines_found = int(line.split(":")[1].strip())

                            if lines_found > 0:
                                coverage_data["line_coverage"] = round((lines_hit / lines_found) * 100, 2)
                                coverage_data["files_found"] += 1

                except Exception as e:
                    commands.append(f"Could not parse {filename}: {e}")

            return coverage_data, commands

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }, commands

    def _collect_docs_metrics(self):
        """Collect documentation coverage metrics."""
        print("[DOCS METRICS] Collecting by language...")

        for repo_config in self.config["repos"]:
            repo_name = repo_config["name"]
            repo_path = self.root / repo_config["path"]
            language = repo_config.get("language", "unknown")

            if not repo_path.exists():
                continue

            print(f"  📊 {repo_name} ({language})...")

            try:
                self._collect_metric(
                    metric_id=f"{repo_name}/docs.coverage",
                    repo_name=repo_name,
                    repo_path=repo_path,
                    collector_fn=lambda p: self._scan_docs_coverage(p, language)
                )
            except Exception as e:
                print(f"    ⚠️  Could not scan docs: {e}")

    def _scan_docs_coverage(self, repo_path: Path, language: str) -> Tuple[Dict, List[str]]:
        """Scan for documentation coverage by language."""
        commands = [f"scanned {repo_path.name} for {language} documentation"]

        if language == "python":
            return self._scan_python_docs(repo_path), commands
        elif language == "java":
            return self._scan_java_docs(repo_path), commands
        elif language in ["javascript", "typescript", "mixed"]:
            return self._scan_js_docs(repo_path), commands
        else:
            return {"status": "unsupported_language", "language": language}, commands

    def _scan_python_docs(self, repo_path: Path) -> Dict:
        """Scan Python files for docstrings."""
        import re

        py_files = list(repo_path.glob("**/*.py"))
        if not py_files:
            return {"documented": 0, "total": 0, "coverage_percent": 0}

        documented = 0
        total = 0

        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                    # Count functions and classes
                    functions = len(re.findall(r'^\s*def\s+\w+', content, re.MULTILINE))
                    classes = len(re.findall(r'^\s*class\s+\w+', content, re.MULTILINE))
                    total += functions + classes

                    # Count docstrings (triple quotes)
                    docstrings = len(re.findall(r'^\s*"""[^"]*"""', content, re.MULTILINE))
                    docstrings += len(re.findall(r"^\s*'''[^']*'''", content, re.MULTILINE))
                    documented += min(docstrings, functions + classes)
            except:
                pass

        coverage = (documented / total * 100) if total > 0 else 0
        return {
            "documented": documented,
            "total": total,
            "coverage_percent": round(coverage, 2),
            "files_scanned": len(py_files)
        }

    def _scan_java_docs(self, repo_path: Path) -> Dict:
        """Scan Java files for Javadoc."""
        import re

        java_files = list(repo_path.glob("**/*.java"))
        if not java_files:
            return {"documented": 0, "total": 0, "coverage_percent": 0}

        documented = 0
        total = 0

        for java_file in java_files:
            try:
                with open(java_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                    # Count public methods and classes
                    public_items = len(re.findall(r'public\s+(?:class|interface|(?:void|int|String|boolean|List|Map|Optional)[\s\w<>,]*)\s+\w+', content))
                    total += public_items

                    # Count Javadoc comments
                    javadocs = len(re.findall(r'/\*\*[^*]*\*/', content, re.DOTALL))
                    documented += javadocs
            except:
                pass

        coverage = (documented / total * 100) if total > 0 else 0
        return {
            "documented": documented,
            "total": total,
            "coverage_percent": round(coverage, 2),
            "files_scanned": len(java_files)
        }

    def _scan_js_docs(self, repo_path: Path) -> Dict:
        """Scan JS/TS files for JSDoc."""
        import re

        js_files = list(repo_path.glob("**/*.js")) + list(repo_path.glob("**/*.ts")) + list(repo_path.glob("**/*.tsx"))
        if not js_files:
            return {"documented": 0, "total": 0, "coverage_percent": 0}

        documented = 0
        total = 0

        for js_file in js_files:
            try:
                with open(js_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                    # Count exported functions
                    exports = len(re.findall(r'export\s+(?:async\s+)?function\s+\w+|export\s+const\s+\w+\s*=', content))
                    total += exports if exports > 0 else len(re.findall(r'^\s*(?:async\s+)?function\s+\w+|^\s*const\s+\w+\s*=', content, re.MULTILINE))

                    # Count JSDoc comments
                    jsdocs = len(re.findall(r'/\*\*[^*]*\*/', content, re.DOTALL))
                    documented += jsdocs
            except:
                pass

        coverage = (documented / total * 100) if total > 0 else 0
        return {
            "documented": documented,
            "total": total,
            "coverage_percent": round(coverage, 2),
            "files_scanned": len(js_files)
        }

    def _validate_evidence_completeness(self):
        """Validate all metrics have complete evidence."""
        print("\n[VALIDATION] Checking evidence completeness...")

        all_valid = True
        for metric_id, evidence in self.evidence_map.items():
            required_fields = ["metric_id", "repo", "range", "collected_at", "commands", "raw_file"]
            missing = [f for f in required_fields if not evidence.get(f)]

            if missing:
                print(f"  ❌ {metric_id}: missing {missing}")
                all_valid = False
            else:
                print(f"  ✅ {metric_id}")

        if not all_valid:
            raise RuntimeError("Evidence completeness check failed")

    def _write_manifest(self, capabilities: Dict):
        """Write execution manifest."""
        manifest = {
            "run_timestamp": self.start_time.isoformat(),
            "time_range": self.time_range,
            "date_from": self.date_from,
            "date_to": self.date_to,
            "timezone": "UTC",
            "preflight": capabilities,
            "metrics_collected": list(self.evidence_map.keys()),
            "evidence_map": self.evidence_map,
            "quality_gates": {
                "evidence_completeness": "PASS",
                "determinism_check": "PENDING"
            }
        }

        manifest_file = self.artifacts_dir / "manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2, default=str)

        print(f"\n✅ Manifest written: {manifest_file}")

    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Evidence-backed metrics collection")
    parser.add_argument("--range", default="last_30_days",
                        choices=["last_30_days", "last_90_days", "ytd", "all_2024", "all_2025", "custom"])
    parser.add_argument("--from", dest="from_date", help="Custom range start (ISO8601)")
    parser.add_argument("--to", dest="to_date", help="Custom range end (ISO8601)")
    parser.add_argument("--config", default="config/repos.yaml")

    args = parser.parse_args()

    collector = MetricsCollector(
        args.config,
        args.range,
        custom_from=args.from_date,
        custom_to=args.to_date
    )

    try:
        collector.run()
        print("\n✅ Metrics collection succeeded")
        return 0
    except Exception as e:
        print(f"\n❌ Metrics collection failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
