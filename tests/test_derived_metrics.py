#!/usr/bin/env python3
"""
Unit tests for derived metrics computation.
Tests that derived metrics are computed correctly from raw data.
"""

import json
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timezone

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from compute_derived import DerivedMetricsCompute


class TestActivityMetricsDerivation(unittest.TestCase):
    """Test activity metrics derivation."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.raw_dir = Path(self.temp_dir.name) / "raw"
        self.derived_dir = Path(self.temp_dir.name) / "derived"
        self.raw_dir.mkdir()
        self.derived_dir.mkdir()

    def tearDown(self):
        """Clean up."""
        self.temp_dir.cleanup()

    def test_commits_per_day_calculation(self):
        """Test commits per day is calculated correctly."""
        # Create raw data file
        raw_data = {
            "count": 30,
            "range": {
                "from": "2026-01-01T00:00:00+00:00",
                "to": "2026-01-31T00:00:00+00:00"  # 30 days
            }
        }

        raw_file = self.raw_dir / "TestRepo_commits_count.json"
        with open(raw_file, 'w') as f:
            json.dump(raw_data, f)

        # Create manifest
        manifest = {"run_timestamp": datetime.now(timezone.utc).isoformat()}

        # Compute derived
        computer = DerivedMetricsCompute(self.raw_dir, self.derived_dir, manifest)
        computer.run()

        # Check result
        activity_file = self.derived_dir / "activity_derived.json"
        self.assertTrue(activity_file.exists())

        with open(activity_file, 'r') as f:
            data = json.load(f)

        # Should have TestRepo_activity_commits_per_day
        metrics = data.get("metrics", {})
        self.assertIn("TestRepo_activity_commits_per_day", metrics)

        metric = metrics["TestRepo_activity_commits_per_day"]
        # 30 commits / 31 days = 0.97 commits/day
        self.assertAlmostEqual(metric["value"], 0.97, places=1)


class TestQualityMetricsDerivation(unittest.TestCase):
    """Test quality metrics derivation."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.raw_dir = Path(self.temp_dir.name) / "raw"
        self.derived_dir = Path(self.temp_dir.name) / "derived"
        self.raw_dir.mkdir()
        self.derived_dir.mkdir()

    def tearDown(self):
        """Clean up."""
        self.temp_dir.cleanup()

    def test_test_pass_rate_calculation(self):
        """Test pass rate is calculated correctly."""
        # Create raw test data
        raw_data = {
            "total": 100,
            "passed": 95,
            "failed": 3,
            "skipped": 2
        }

        raw_file = self.raw_dir / "TestRepo_tests_summary.json"
        with open(raw_file, 'w') as f:
            json.dump(raw_data, f)

        manifest = {"run_timestamp": datetime.now(timezone.utc).isoformat()}

        computer = DerivedMetricsCompute(self.raw_dir, self.derived_dir, manifest)
        computer.run()

        # Check result
        quality_file = self.derived_dir / "quality_derived.json"
        self.assertTrue(quality_file.exists())

        with open(quality_file, 'r') as f:
            data = json.load(f)

        metrics = data.get("metrics", {})
        self.assertIn("TestRepo_quality_test_pass_rate", metrics)

        metric = metrics["TestRepo_quality_test_pass_rate"]
        # Pass rate = (100 - 3 - 2) / (100 - 2) = 95/98 = 96.94%
        self.assertAlmostEqual(metric["value"], 96.94, places=1)

    def test_coverage_adequacy_threshold(self):
        """Test coverage adequacy is determined correctly."""
        # Create raw coverage data - sufficient
        raw_data = {
            "line_coverage": 80,
            "branch_coverage": 75
        }

        raw_file = self.raw_dir / "TestRepo_coverage_summary.json"
        with open(raw_file, 'w') as f:
            json.dump(raw_data, f)

        manifest = {"run_timestamp": datetime.now(timezone.utc).isoformat()}

        computer = DerivedMetricsCompute(self.raw_dir, self.derived_dir, manifest)
        computer.run()

        quality_file = self.derived_dir / "quality_derived.json"
        with open(quality_file, 'r') as f:
            data = json.load(f)

        metrics = data.get("metrics", {})
        self.assertIn("TestRepo_quality_coverage_line", metrics)

        metric = metrics["TestRepo_quality_coverage_line"]
        self.assertEqual(metric["value"], 80)
        self.assertEqual(metric["adequacy"], "sufficient")


class TestVelocityMetricsDerivation(unittest.TestCase):
    """Test velocity metrics derivation."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.raw_dir = Path(self.temp_dir.name) / "raw"
        self.derived_dir = Path(self.temp_dir.name) / "derived"
        self.raw_dir.mkdir()
        self.derived_dir.mkdir()

    def tearDown(self):
        """Clean up."""
        self.temp_dir.cleanup()

    def test_net_loc_calculation(self):
        """Test net LOC is calculated correctly."""
        # Create raw diff data
        raw_data = {
            "loc_added": 500,
            "loc_deleted": 200,
            "files_changed": 10,
            "range": {
                "from": "2026-01-01T00:00:00+00:00",
                "to": "2026-01-31T00:00:00+00:00"
            }
        }

        raw_file = self.raw_dir / "TestRepo_diffs_stats.json"
        with open(raw_file, 'w') as f:
            json.dump(raw_data, f)

        manifest = {"run_timestamp": datetime.now(timezone.utc).isoformat()}

        computer = DerivedMetricsCompute(self.raw_dir, self.derived_dir, manifest)
        computer.run()

        velocity_file = self.derived_dir / "velocity_derived.json"
        self.assertTrue(velocity_file.exists())

        with open(velocity_file, 'r') as f:
            data = json.load(f)

        metrics = data.get("metrics", {})
        self.assertIn("TestRepo_velocity_loc_net", metrics)

        metric = metrics["TestRepo_velocity_loc_net"]
        self.assertEqual(metric["value"], 300)  # 500 - 200

    def test_churn_ratio_calculation(self):
        """Test churn ratio is calculated correctly."""
        raw_data = {
            "loc_added": 400,
            "loc_deleted": 200,
            "files_changed": 8,
            "range": {
                "from": "2026-01-01T00:00:00+00:00",
                "to": "2026-01-31T00:00:00+00:00"
            }
        }

        raw_file = self.raw_dir / "TestRepo_diffs_stats.json"
        with open(raw_file, 'w') as f:
            json.dump(raw_data, f)

        manifest = {"run_timestamp": datetime.now(timezone.utc).isoformat()}

        computer = DerivedMetricsCompute(self.raw_dir, self.derived_dir, manifest)
        computer.run()

        velocity_file = self.derived_dir / "velocity_derived.json"
        with open(velocity_file, 'r') as f:
            data = json.load(f)

        metrics = data.get("metrics", {})
        self.assertIn("TestRepo_velocity_churn_ratio", metrics)

        metric = metrics["TestRepo_velocity_churn_ratio"]
        self.assertAlmostEqual(metric["value"], 0.5, places=1)  # 200 / 400

    def test_files_per_commit_calculation(self):
        """Test files per commit is calculated correctly."""
        # Create raw files
        commits_data = {
            "count": 20,
            "range": {
                "from": "2026-01-01T00:00:00+00:00",
                "to": "2026-01-31T00:00:00+00:00"
            }
        }

        diffs_data = {
            "loc_added": 500,
            "loc_deleted": 100,
            "files_changed": 60,
            "range": {
                "from": "2026-01-01T00:00:00+00:00",
                "to": "2026-01-31T00:00:00+00:00"
            }
        }

        with open(self.raw_dir / "TestRepo_commits_count.json", 'w') as f:
            json.dump(commits_data, f)

        with open(self.raw_dir / "TestRepo_diffs_stats.json", 'w') as f:
            json.dump(diffs_data, f)

        manifest = {"run_timestamp": datetime.now(timezone.utc).isoformat()}

        computer = DerivedMetricsCompute(self.raw_dir, self.derived_dir, manifest)
        computer.run()

        velocity_file = self.derived_dir / "velocity_derived.json"
        with open(velocity_file, 'r') as f:
            data = json.load(f)

        metrics = data.get("metrics", {})
        self.assertIn("TestRepo_velocity_files_per_commit", metrics)

        metric = metrics["TestRepo_velocity_files_per_commit"]
        self.assertAlmostEqual(metric["value"], 3.0, places=1)  # 60 / 20


class TestDerivedManifestGeneration(unittest.TestCase):
    """Test derived metrics manifest generation."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.raw_dir = Path(self.temp_dir.name) / "raw"
        self.derived_dir = Path(self.temp_dir.name) / "derived"
        self.raw_dir.mkdir()
        self.derived_dir.mkdir()

    def tearDown(self):
        """Clean up."""
        self.temp_dir.cleanup()

    def test_manifest_created(self):
        """Test derived manifest is created."""
        # Create sample raw data
        raw_data = {"count": 10, "range": {
            "from": "2026-01-01T00:00:00+00:00",
            "to": "2026-01-31T00:00:00+00:00"
        }}

        with open(self.raw_dir / "TestRepo_commits_count.json", 'w') as f:
            json.dump(raw_data, f)

        manifest = {"run_timestamp": datetime.now(timezone.utc).isoformat()}

        computer = DerivedMetricsCompute(self.raw_dir, self.derived_dir, manifest)
        computer.run()

        manifest_file = self.derived_dir / "derived_manifest.json"
        self.assertTrue(manifest_file.exists())

        with open(manifest_file, 'r') as f:
            manifest_data = json.load(f)

        self.assertIn("computed_at", manifest_data)
        self.assertIn("source_manifest", manifest_data)
        self.assertIn("total_derived_metrics", manifest_data)
        self.assertIn("by_dimension", manifest_data)


if __name__ == "__main__":
    unittest.main()
