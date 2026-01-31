#!/usr/bin/env python3
"""
Compute derived metrics from epic coverage data.

Generates:
- Tests per epic
- Tests per user story
- Epic/US level detail metrics
"""

import json
from pathlib import Path
from datetime import datetime, timezone


def compute_epic_derived_metrics():
    """Compute metrics from epic coverage data."""
    root_dir = Path(__file__).parent.parent
    epic_coverage_file = root_dir / "artifacts" / "raw" / "epic_coverage.json"

    if not epic_coverage_file.exists():
        print("⚠️  No epic coverage data found, skipping epic-derived metrics")
        return {}

    with open(epic_coverage_file, 'r') as f:
        coverage_data = json.load(f)

    derived_metrics = {}

    for project_key, project_data in coverage_data.items():
        project = project_data.get("project", project_key)

        # Epic-level metrics
        for epic in project_data.get("epics", []):
            epic_id = epic["epic_id"]
            epic_num = epic["epic_number"]
            epic_title = epic["epic_title"]
            total_epic_tests = epic["total_tests"]
            us_count = epic["us_count"]

            # Metric: tests per epic
            metric_id = f"{project}_epic_{epic_id}_test_count"
            derived_metrics[metric_id] = {
                "value": total_epic_tests,
                "unit": "tests",
                "dimension": "epic",
                "epic_id": epic_id,
                "epic_number": epic_num,
                "epic_title": epic_title,
                "user_stories": us_count,
                "source_metrics": ["epic_coverage"],
                "calculation": f"Total tests in {epic_title}"
            }

            # User story metrics
            for us in epic.get("user_stories", []):
                us_id = us["id"]
                us_title = us["title"]
                us_test_count = us["test_count"]

                metric_id_us = f"{project}_epic_{epic_id}_us_{us_id}_test_count"
                derived_metrics[metric_id_us] = {
                    "value": us_test_count,
                    "unit": "tests",
                    "dimension": "epic",
                    "epic_id": epic_id,
                    "epic_title": epic_title,
                    "us_id": us_id,
                    "us_title": us_title,
                    "source_metrics": ["epic_coverage"],
                    "calculation": f"Tests for {us_title}"
                }

        # Project-level summary
        total_epics = project_data.get("total_epics", 0)
        total_us = project_data.get("total_user_stories", 0)
        total_tests = project_data.get("total_tests", 0)

        metric_id_summary = f"{project}_epic_summary"
        derived_metrics[metric_id_summary] = {
            "value": {
                "epics": total_epics,
                "user_stories": total_us,
                "tests": total_tests
            },
            "dimension": "epic",
            "unit": "summary",
            "source_metrics": ["epic_coverage"],
            "calculation": "Aggregated epic/US/test counts"
        }

    return derived_metrics


def write_epic_derived_metrics(derived_metrics):
    """Write derived epic metrics to file."""
    root_dir = Path(__file__).parent.parent
    derived_dir = root_dir / "artifacts" / "derived"
    derived_dir.mkdir(parents=True, exist_ok=True)

    output_file = derived_dir / "epic_detail_derived.json"

    output_data = {
        "dimension": "epic_detail",
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "metrics": derived_metrics
    }

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"✅ Epic-detail derived metrics written to: {output_file}")


def main():
    """Main entry point."""
    print("[EPIC DERIVED METRICS] Computing from epic coverage data...")
    print()

    try:
        derived_metrics = compute_epic_derived_metrics()

        if derived_metrics:
            write_epic_derived_metrics(derived_metrics)
            print(f"✅ Generated {len(derived_metrics)} epic-detail metrics")
        else:
            print("⚠️  No epic coverage data to process")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
