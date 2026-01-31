#!/usr/bin/env python3
"""
Unit tests for metrics collection engine.
Tests that metrics are collected correctly from git and CI artifacts.
"""

import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from collect_metrics import MetricsCollector


class TestDateRangeComputation(unittest.TestCase):
    """Test date range computation for different time range types."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_file = Path(self.temp_dir.name) / "config.yaml"
        self._write_minimal_config()

    def tearDown(self):
        """Clean up."""
        self.temp_dir.cleanup()

    def _write_minimal_config(self):
        """Write minimal config file."""
        config_content = """
repos:
  - name: TestRepo
    path: .
    language: python
"""
        with open(self.config_file, 'w') as f:
            f.write(config_content)

    def test_last_30_days(self):
        """Test last_30_days range computation."""
        collector = MetricsCollector(str(self.config_file), "last_30_days")

        from_dt = datetime.fromisoformat(collector.date_from)
        to_dt = datetime.fromisoformat(collector.date_to)

        # Should span ~30 days
        delta = to_dt - from_dt
        self.assertGreaterEqual(delta.days, 29)
        self.assertLessEqual(delta.days, 31)

    def test_all_2024(self):
        """Test all_2024 range computation."""
        collector = MetricsCollector(str(self.config_file), "all_2024")

        from_dt = datetime.fromisoformat(collector.date_from)
        to_dt = datetime.fromisoformat(collector.date_to)

        # Should span all of 2024
        self.assertEqual(from_dt.year, 2024)
        self.assertEqual(from_dt.month, 1)
        self.assertEqual(from_dt.day, 1)

        self.assertEqual(to_dt.year, 2025)
        self.assertEqual(to_dt.month, 1)
        self.assertEqual(to_dt.day, 1)

    def test_custom_range(self):
        """Test custom date range."""
        custom_from = "2026-01-01T00:00:00Z"
        custom_to = "2026-01-31T23:59:59Z"

        collector = MetricsCollector(
            str(self.config_file),
            "custom",
            custom_from=custom_from,
            custom_to=custom_to
        )

        self.assertEqual(collector.date_from, "2026-01-01T00:00:00+00:00")
        self.assertEqual(collector.date_to, "2026-01-31T23:59:59+00:00")

    def test_custom_range_missing_dates(self):
        """Test custom range without dates raises error."""
        with self.assertRaises(ValueError):
            MetricsCollector(str(self.config_file), "custom")


class TestGitMetricsCollection(unittest.TestCase):
    """Test git metrics collection."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.artifacts_dir = Path(self.temp_dir.name) / "artifacts"
        self.artifacts_dir.mkdir()

        self.config_file = Path(self.temp_dir.name) / "config.yaml"
        with open(self.config_file, 'w') as f:
            f.write("""
repos:
  - name: TestRepo
    path: .
    language: python
""")

    def tearDown(self):
        """Clean up."""
        self.temp_dir.cleanup()

    def test_commit_count_returns_tuple(self):
        """Test that _count_commits returns (dict, list) tuple."""
        collector = MetricsCollector(str(self.config_file), "last_30_days")

        # Mock subprocess to return test data
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="hash1\n2026-01-31T00:00:00+00:00\nauthor1\n"
            )

            result, commands = collector._count_commits(Path("."))

            self.assertIsInstance(result, dict)
            self.assertIsInstance(commands, list)
            self.assertIn("count", result)
            self.assertGreater(len(commands), 0)

    def test_diff_stats_parsing(self):
        """Test git diff stats parsing."""
        collector = MetricsCollector(str(self.config_file), "last_30_days")

        # Mock subprocess
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="10 files changed, 250 insertions(+), 100 deletions(-)\n"
            )

            result, commands = collector._collect_diff_stats(Path("."))

            self.assertEqual(result["loc_added"], 250)
            self.assertEqual(result["loc_deleted"], 100)
            self.assertEqual(result["files_changed"], 10)

    def test_diff_stats_no_commits(self):
        """Test diff stats when no commits exist."""
        collector = MetricsCollector(str(self.config_file), "last_30_days")

        # Mock subprocess to fail (no commits)
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stderr="")

            result, commands = collector._collect_diff_stats(Path("."))

            self.assertEqual(result["loc_added"], 0)
            self.assertEqual(result["loc_deleted"], 0)
            self.assertEqual(result["files_changed"], 0)


class TestEvidenceTracking(unittest.TestCase):
    """Test evidence tracking and metadata."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_file = Path(self.temp_dir.name) / "config.yaml"

        with open(self.config_file, 'w') as f:
            f.write("""
repos:
  - name: TestRepo
    path: .
    language: python
""")

    def tearDown(self):
        """Clean up."""
        self.temp_dir.cleanup()

    def test_evidence_completeness_required_fields(self):
        """Test that evidence has all required fields."""
        collector = MetricsCollector(str(self.config_file), "last_30_days")

        # Add test evidence
        collector.evidence_map["test_metric"] = {
            "metric_id": "test_metric",
            "repo": "TestRepo",
            "range": {"from": collector.date_from, "to": collector.date_to},
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "commands": ["test command"],
            "raw_file": str(Path(self.temp_dir.name) / "test.json")
        }

        # Should not raise (all fields present)
        try:
            collector._validate_evidence_completeness()
        except RuntimeError:
            self.fail("Evidence completeness check raised unexpectedly")

    def test_evidence_missing_fields(self):
        """Test that missing evidence fields are caught."""
        collector = MetricsCollector(str(self.config_file), "last_30_days")
        collector.metrics = {"test": "value"}

        # Add incomplete evidence
        collector.evidence_map["test_metric"] = {
            "metric_id": "test_metric"
            # Missing other required fields
        }

        with self.assertRaises(RuntimeError):
            collector._validate_evidence_completeness()


class TestJUnitParsing(unittest.TestCase):
    """Test JUnit XML parsing."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_file = Path(self.temp_dir.name) / "config.yaml"

        with open(self.config_file, 'w') as f:
            f.write("""
repos:
  - name: TestRepo
    path: .
    language: python
""")

    def tearDown(self):
        """Clean up."""
        self.temp_dir.cleanup()

    def test_junit_parsing(self):
        """Test parsing JUnit XML."""
        collector = MetricsCollector(str(self.config_file), "last_30_days")

        # Create test JUnit file
        junit_file = Path(self.temp_dir.name) / "test.xml"
        junit_content = """<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="test_suite" tests="10" failures="2" skipped="1">
    <testcase name="test1"/>
    <testcase name="test2"/>
    <testcase name="test3"><failure/></testcase>
    <testcase name="test4"><failure/></testcase>
    <testcase name="test5"><skipped/></testcase>
  </testsuite>
</testsuites>
"""
        with open(junit_file, 'w') as f:
            f.write(junit_content)

        result, commands = collector._parse_junit_reports([junit_file])

        self.assertEqual(result["total"], 5)
        self.assertEqual(result["failed"], 2)
        self.assertEqual(result["skipped"], 1)
        # Passed = 5 - 2 - 1 = 2
        self.assertEqual(result["passed"], 2)


class TestDocsCoverage(unittest.TestCase):
    """Test documentation coverage scanning."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_file = Path(self.temp_dir.name) / "config.yaml"
        self.repo_dir = Path(self.temp_dir.name) / "repo"
        self.repo_dir.mkdir()

        with open(self.config_file, 'w') as f:
            f.write(f"""
repos:
  - name: TestRepo
    path: {self.repo_dir}
    language: python
""")

    def tearDown(self):
        """Clean up."""
        self.temp_dir.cleanup()

    def test_python_docstring_detection(self):
        """Test Python docstring detection."""
        # Create test Python file
        py_file = self.repo_dir / "test.py"
        py_content = '''
def documented_func():
    """This function is documented."""
    pass

def undocumented_func():
    pass

class DocumentedClass:
    """This class is documented."""
    pass

class UndocumentedClass:
    pass
'''
        with open(py_file, 'w') as f:
            f.write(py_content)

        collector = MetricsCollector(str(self.config_file), "last_30_days")
        result = collector._scan_python_docs(self.repo_dir)

        self.assertEqual(result["total"], 4)  # 2 functions + 2 classes
        self.assertEqual(result["documented"], 2)
        self.assertEqual(result["files_scanned"], 1)


class TestManifestGeneration(unittest.TestCase):
    """Test manifest generation."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_file = Path(self.temp_dir.name) / "config.yaml"

        with open(self.config_file, 'w') as f:
            f.write("""
repos:
  - name: TestRepo
    path: .
    language: python
""")

    def tearDown(self):
        """Clean up."""
        self.temp_dir.cleanup()

    def test_manifest_structure(self):
        """Test manifest has required structure."""
        collector = MetricsCollector(str(self.config_file), "last_30_days")

        capabilities = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "repos": {},
            "computable_metrics": {},
            "na_metrics": {}
        }

        collector._write_manifest(capabilities)

        manifest_file = collector.artifacts_dir / "manifest.json"
        self.assertTrue(manifest_file.exists())

        with open(manifest_file, 'r') as f:
            manifest = json.load(f)

        self.assertIn("run_timestamp", manifest)
        self.assertIn("time_range", manifest)
        self.assertIn("date_from", manifest)
        self.assertIn("date_to", manifest)
        self.assertIn("evidence_map", manifest)
        self.assertIn("quality_gates", manifest)


if __name__ == "__main__":
    unittest.main()
