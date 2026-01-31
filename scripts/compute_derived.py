#!/usr/bin/env python3
"""
Compute derived metrics from raw data.

Raw metrics are what we collected directly (git commits, test counts, etc.)
Derived metrics normalize and combine raw data into meaningful indicators.

No guessing. Every derived metric computed deterministically from raw sources.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


class DerivedMetricsCompute:
    """Compute derived metrics from raw data."""

    def __init__(self, raw_dir: Path, derived_dir: Path, manifest: Dict):
        """Initialize with paths to raw and derived data directories."""
        self.raw_dir = raw_dir
        self.derived_dir = derived_dir
        self.manifest = manifest
        self.raw_data = {}
        self.derived_data = {}

    def run(self) -> bool:
        """Execute derived metrics computation."""
        print("[DERIVED METRICS] Computing from raw data...")

        try:
            # Load all raw data
            self._load_raw_data()

            # Compute derived metrics per repo
            self._compute_activity_metrics()
            self._compute_quality_metrics()
            self._compute_velocity_metrics()
            self._compute_test_metrics()
            self._compute_epic_metrics()

            # Write derived metrics
            self._write_derived_data()

            print("✅ Derived metrics computed successfully")
            return True

        except Exception as e:
            print(f"❌ Derived metrics computation failed: {e}")
            return False

    def _extract_project_name(self, metric_id: str) -> str:
        """Extract project name from metric ID.

        Handles formats like:
        - vionascu_trailwaze_commits.count
        - vionascu_trail-equip_commits.count
        - trailwaze_commits.count

        Returns the full project prefix including hyphens/underscores.
        """
        # Remove the metric type suffix (.count, .stats, etc.)
        parts = metric_id.split('_')

        # Find where the metric type starts
        # Common metric types: commits, diffs, tests, coverage, docs
        metric_types = ['commits', 'diffs', 'tests', 'coverage', 'docs']

        for i in range(len(parts) - 1, -1, -1):
            if any(mt in parts[i].lower() for mt in metric_types):
                # Found metric type, everything before is project
                return '_'.join(parts[:i])

        # Fallback: assume it's all but the last part
        return '_'.join(parts[:-1]) if len(parts) > 1 else parts[0]

    def _load_raw_data(self):
        """Load all raw data files."""
        print("  Loading raw data...")

        for raw_file in self.raw_dir.glob("*.json"):
            try:
                with open(raw_file, 'r') as f:
                    self.raw_data[raw_file.stem] = json.load(f)
            except Exception as e:
                print(f"    ⚠️  Could not load {raw_file.name}: {e}")

        print(f"  ✅ Loaded {len(self.raw_data)} raw data files")

    def _compute_activity_metrics(self):
        """Compute activity-level derived metrics."""
        print("  Computing activity metrics...")

        for metric_id, raw_value in self.raw_data.items():
            if "commits.count" in metric_id or "commits_count" in metric_id:
                repo = self._extract_project_name(metric_id)
                commits = raw_value.get("count", 0)
                commits_by_week = raw_value.get("commits_by_week", {})

                # If we have weekly breakdown, use it; otherwise fall back to total
                if commits_by_week:
                    # Store weekly breakdown as the primary metric
                    self.derived_data[f"{repo}_activity_commits_weekly"] = {
                        "value": commits_by_week,
                        "unit": "commits by week",
                        "source_metrics": [metric_id],
                        "calculation": f"Grouped {commits} commits by ISO week number",
                        "total": commits
                    }

                    # Also store total for reference
                    self.derived_data[f"{repo}_activity_commits_total"] = {
                        "value": commits,
                        "unit": "commits",
                        "source_metrics": [metric_id],
                        "calculation": f"Total commits in period",
                        "weekly_breakdown": commits_by_week
                    }
                else:
                    # Fallback if no weekly data available (old data)
                    date_range = raw_value.get("range", {})
                    if "from" in date_range and "to" in date_range:
                        from_dt = datetime.fromisoformat(date_range["from"])
                        to_dt = datetime.fromisoformat(date_range["to"])
                        days = (to_dt - from_dt).days + 1

                        if days > 0:
                            self.derived_data[f"{repo}_activity_commits_total"] = {
                                "value": commits,
                                "unit": "commits",
                                "source_metrics": [metric_id],
                                "calculation": f"Total commits over {days} days"
                            }

    def _compute_quality_metrics(self):
        """Compute quality-level derived metrics."""
        print("  Computing quality metrics...")

        # Test pass rate
        for metric_id, raw_value in self.raw_data.items():
            if "tests_summary" in metric_id:
                repo = self._extract_project_name(metric_id)

                total = raw_value.get("total", 0)
                failed = raw_value.get("failed", 0)
                skipped = raw_value.get("skipped", 0)

                if total > skipped > 0:
                    pass_rate = ((total - failed - skipped) / (total - skipped)) * 100

                    self.derived_data[f"{repo}_quality_test_pass_rate"] = {
                        "value": round(pass_rate, 2),
                        "unit": "percent",
                        "source_metrics": [metric_id],
                        "calculation": f"({total} - {failed} - {skipped}) / ({total} - {skipped}) * 100"
                    }

            # Coverage adequacy
            if "coverage_summary" in metric_id:
                repo = self._extract_project_name(metric_id)

                line_coverage = raw_value.get("line_coverage")
                if line_coverage is not None:
                    self.derived_data[f"{repo}_quality_coverage_line"] = {
                        "value": line_coverage,
                        "unit": "percent",
                        "source_metrics": [metric_id],
                        "adequacy": "sufficient" if line_coverage >= 70 else "needs_improvement"
                    }

                branch_coverage = raw_value.get("branch_coverage")
                if branch_coverage is not None:
                    self.derived_data[f"{repo}_quality_coverage_branch"] = {
                        "value": branch_coverage,
                        "unit": "percent",
                        "source_metrics": [metric_id]
                    }

    def _compute_velocity_metrics(self):
        """Compute velocity-level derived metrics."""
        print("  Computing velocity metrics...")

        for metric_id, raw_value in self.raw_data.items():
            if "diffs.stats" in metric_id or "diffs_stats" in metric_id:
                repo = self._extract_project_name(metric_id)

                loc_added = raw_value.get("loc_added", 0)
                loc_deleted = raw_value.get("loc_deleted", 0)
                files_changed = raw_value.get("files_changed", 0)
                date_range = raw_value.get("range", {})

                # Net LOC change
                net_loc = loc_added - loc_deleted

                self.derived_data[f"{repo}_velocity_loc_net"] = {
                    "value": net_loc,
                    "unit": "lines",
                    "source_metrics": [metric_id],
                    "components": {
                        "added": loc_added,
                        "deleted": loc_deleted
                    }
                }

                # Churn ratio (how much code was changed relative to added)
                if loc_added > 0:
                    churn_ratio = loc_deleted / loc_added

                    self.derived_data[f"{repo}_velocity_churn_ratio"] = {
                        "value": round(churn_ratio, 2),
                        "unit": "ratio",
                        "source_metrics": [metric_id],
                        "interpretation": "deletions per insertion (higher = more refactoring)"
                    }

                # Files per commit
                commits_metric = [m for m in self.raw_data.keys() if "commits_count" in m and repo in m]
                if commits_metric:
                    commits = self.raw_data[commits_metric[0]].get("count", 0)
                    if commits > 0:
                        files_per_commit = files_changed / commits

                        self.derived_data[f"{repo}_velocity_files_per_commit"] = {
                            "value": round(files_per_commit, 2),
                            "unit": "files/commit",
                            "source_metrics": [metric_id, commits_metric[0]],
                            "calculation": f"{files_changed} files / {commits} commits"
                        }

    def _compute_test_metrics(self):
        """Compute test-related derived metrics."""
        print("  Computing test metrics...")

        for metric_id, raw_value in self.raw_data.items():
            if "tests_summary" in metric_id:
                repo = self._extract_project_name(metric_id)
                total_tests = raw_value.get("total", 0)
                passed_tests = raw_value.get("passed", 0)
                failed_tests = raw_value.get("failed", 0)

                # Store total test count
                self.derived_data[f"{repo}_test_total_count"] = {
                    "value": total_tests,
                    "unit": "tests",
                    "source_metrics": [metric_id],
                    "dimension": "test"
                }

                # Store test breakdown by type
                tests_by_type = raw_value.get("tests_by_type", {})
                for test_type, count in tests_by_type.items():
                    if count > 0:
                        self.derived_data[f"{repo}_test_{test_type}_count"] = {
                            "value": count,
                            "unit": "tests",
                            "source_metrics": [metric_id],
                            "category": test_type,
                            "dimension": "test"
                        }

                # Calculate pass rate
                if total_tests > 0:
                    pass_rate = (passed_tests / total_tests) * 100
                    self.derived_data[f"{repo}_test_pass_rate"] = {
                        "value": round(pass_rate, 2),
                        "unit": "percent",
                        "source_metrics": [metric_id],
                        "dimension": "test",
                        "calculation": f"{passed_tests} passed / {total_tests} total"
                    }

    def _compute_epic_metrics(self):
        """Compute epic coverage metrics."""
        print("  Computing epic metrics...")

        for metric_id, raw_value in self.raw_data.items():
            if "epics_summary" in metric_id:
                repo = self._extract_project_name(metric_id)

                total_epics = raw_value.get("total_epics", 0)
                epics_covered = raw_value.get("epics_covered", 0)
                epics_not_covered = raw_value.get("epics_not_covered", 0)

                # Total epics
                self.derived_data[f"{repo}_epic_total"] = {
                    "value": total_epics,
                    "unit": "epics",
                    "source_metrics": [metric_id],
                    "dimension": "epic"
                }

                # Epics covered
                self.derived_data[f"{repo}_epic_covered"] = {
                    "value": epics_covered,
                    "unit": "epics",
                    "source_metrics": [metric_id],
                    "dimension": "epic",
                    "percentage": (epics_covered / total_epics * 100) if total_epics > 0 else 0
                }

                # Epics not covered
                self.derived_data[f"{repo}_epic_not_covered"] = {
                    "value": epics_not_covered,
                    "unit": "epics",
                    "source_metrics": [metric_id],
                    "dimension": "epic",
                    "percentage": (epics_not_covered / total_epics * 100) if total_epics > 0 else 0
                }

    def _write_derived_data(self):
        """Write computed derived metrics to files."""
        print("  Writing derived metrics...")

        # Group by dimension
        by_dimension = {}
        for metric_id, value in self.derived_data.items():
            # Extract dimension: repo_dimension_metric
            parts = metric_id.split("_", 2)
            if len(parts) >= 2:
                dimension = parts[1]
                if dimension not in by_dimension:
                    by_dimension[dimension] = {}
                by_dimension[dimension][metric_id] = value

        # Write each dimension
        for dimension, metrics in by_dimension.items():
            output_file = self.derived_dir / f"{dimension}_derived.json"
            with open(output_file, 'w') as f:
                json.dump({
                    "dimension": dimension,
                    "computed_at": datetime.now(timezone.utc).isoformat(),
                    "metrics": metrics
                }, f, indent=2, default=str)

            print(f"    ✅ {output_file.name} ({len(metrics)} metrics)")

        # Write comprehensive derived manifest
        derived_manifest = {
            "computed_at": datetime.now(timezone.utc).isoformat(),
            "source_manifest": self.manifest.get("run_timestamp"),
            "total_derived_metrics": len(self.derived_data),
            "by_dimension": {dim: len(metrics) for dim, metrics in by_dimension.items()},
            "all_metrics": list(self.derived_data.keys())
        }

        manifest_file = self.derived_dir / "derived_manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(derived_manifest, f, indent=2, default=str)

        print(f"    ✅ {manifest_file.name}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: compute_derived.py <artifacts_dir>")
        return 1

    artifacts_dir = Path(sys.argv[1])
    raw_dir = artifacts_dir / "raw"
    derived_dir = artifacts_dir / "derived"
    manifest_file = artifacts_dir / "manifest.json"

    if not raw_dir.exists():
        print(f"❌ Raw data directory not found: {raw_dir}")
        return 1

    if not manifest_file.exists():
        print(f"❌ Manifest file not found: {manifest_file}")
        return 1

    # Load manifest
    with open(manifest_file, 'r') as f:
        manifest = json.load(f)

    # Compute derived metrics
    computer = DerivedMetricsCompute(raw_dir, derived_dir, manifest)
    success = computer.run()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
