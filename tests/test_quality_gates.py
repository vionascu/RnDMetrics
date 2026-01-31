#!/usr/bin/env python3
"""
Unit tests for quality gates validation.
Tests that metrics are validated against quality requirements.
"""

import json
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timezone

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from quality_gate import QualityGateValidator


class TestEvidenceCompletenessGate(unittest.TestCase):
    """Test evidence completeness validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.artifacts_dir = Path(self.temp_dir.name) / "artifacts"
        self.raw_dir = self.artifacts_dir / "raw"
        self.derived_dir = self.artifacts_dir / "derived"
        self.artifacts_dir.mkdir()
        self.raw_dir.mkdir()
        self.derived_dir.mkdir()

        self.config_file = Path(self.temp_dir.name) / "config.yaml"
        self._write_config()

    def tearDown(self):
        """Clean up."""
        self.temp_dir.cleanup()

    def _write_config(self):
        """Write test config."""
        config = """
repos:
  - name: TestRepo
    path: .
    language: python

quality_gates:
  enforce_evidence_completeness: true
  enforce_determinism: false
"""
        with open(self.config_file, 'w') as f:
            f.write(config)

    def _write_manifest(self, evidence_map):
        """Write manifest with given evidence map."""
        manifest = {
            "run_timestamp": datetime.now(timezone.utc).isoformat(),
            "time_range": "last_30_days",
            "date_from": "2026-01-01T00:00:00+00:00",
            "date_to": "2026-01-31T00:00:00+00:00",
            "metrics_collected": list(evidence_map.keys()),
            "evidence_map": evidence_map,
            "quality_gates": {}
        }

        manifest_file = self.artifacts_dir / "manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f)

    def test_complete_evidence_passes(self):
        """Test complete evidence passes gate."""
        # Create raw file
        raw_file = self.raw_dir / "TestRepo_commits_count.json"
        with open(raw_file, 'w') as f:
            json.dump({"count": 10}, f)

        # Create evidence
        evidence_map = {
            "TestRepo/commits.count": {
                "metric_id": "TestRepo/commits.count",
                "repo": "TestRepo",
                "range": {"from": "2026-01-01T00:00:00+00:00", "to": "2026-01-31T00:00:00+00:00"},
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "commands": ["git log --count"],
                "raw_file": str(raw_file)
            }
        }

        self._write_manifest(evidence_map)

        validator = QualityGateValidator(self.artifacts_dir, self.config_file)
        result = validator.run()

        self.assertTrue(result)

    def test_missing_evidence_fails(self):
        """Test missing evidence record fails gate."""
        # Create manifest with evidence reference but no actual evidence
        evidence_map = {
            "TestRepo/commits.count": {
                "metric_id": "TestRepo/commits.count"
                # Missing required fields
            }
        }

        self._write_manifest(evidence_map)

        validator = QualityGateValidator(self.artifacts_dir, self.config_file)
        result = validator.run()

        self.assertFalse(result)

    def test_missing_raw_file_fails(self):
        """Test missing raw data file fails gate."""
        evidence_map = {
            "TestRepo/commits.count": {
                "metric_id": "TestRepo/commits.count",
                "repo": "TestRepo",
                "range": {"from": "2026-01-01T00:00:00+00:00", "to": "2026-01-31T00:00:00+00:00"},
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "commands": ["git log"],
                "raw_file": str(self.raw_dir / "nonexistent.json")
            }
        }

        self._write_manifest(evidence_map)

        validator = QualityGateValidator(self.artifacts_dir, self.config_file)
        result = validator.run()

        self.assertFalse(result)


class TestSanityChecksGate(unittest.TestCase):
    """Test sanity check validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.artifacts_dir = Path(self.temp_dir.name) / "artifacts"
        self.raw_dir = self.artifacts_dir / "raw"
        self.derived_dir = self.artifacts_dir / "derived"
        self.artifacts_dir.mkdir()
        self.raw_dir.mkdir()
        self.derived_dir.mkdir()

        self.config_file = Path(self.temp_dir.name) / "config.yaml"
        self._write_config()

    def tearDown(self):
        """Clean up."""
        self.temp_dir.cleanup()

    def _write_config(self):
        """Write test config."""
        config = """
repos:
  - name: TestRepo
    path: .
    language: python

quality_gates:
  enforce_evidence_completeness: false
  enforce_determinism: false
"""
        with open(self.config_file, 'w') as f:
            f.write(config)

    def _write_manifest(self):
        """Write minimal manifest."""
        manifest = {
            "run_timestamp": datetime.now(timezone.utc).isoformat(),
            "time_range": "last_30_days",
            "date_from": "2026-01-01T00:00:00+00:00",
            "date_to": "2026-01-31T00:00:00+00:00",
            "metrics_collected": [],
            "evidence_map": {},
            "quality_gates": {}
        }

        manifest_file = self.artifacts_dir / "manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f)

    def test_valid_percentage_passes(self):
        """Test valid percentage values pass check."""
        raw_data = {"pass_rate_percent": 95, "coverage_percent": 80}

        raw_file = self.raw_dir / "TestRepo_tests_summary.json"
        with open(raw_file, 'w') as f:
            json.dump(raw_data, f)

        self._write_manifest()

        validator = QualityGateValidator(self.artifacts_dir, self.config_file)
        result = validator.run()

        self.assertTrue(result)

    def test_invalid_percentage_fails(self):
        """Test invalid percentage values fail check."""
        raw_data = {"pass_rate_percent": 150}  # Invalid: > 100

        raw_file = self.raw_dir / "TestRepo_tests_summary.json"
        with open(raw_file, 'w') as f:
            json.dump(raw_data, f)

        self._write_manifest()

        validator = QualityGateValidator(self.artifacts_dir, self.config_file)
        result = validator.run()

        self.assertFalse(result)

    def test_negative_count_fails(self):
        """Test negative count values fail check."""
        raw_data = {"count": -5}  # Invalid: negative

        raw_file = self.raw_dir / "TestRepo_commits_count.json"
        with open(raw_file, 'w') as f:
            json.dump(raw_data, f)

        self._write_manifest()

        validator = QualityGateValidator(self.artifacts_dir, self.config_file)
        result = validator.run()

        self.assertFalse(result)

    def test_test_count_logic_violation_fails(self):
        """Test test count logic violations fail check."""
        raw_data = {
            "total": 100,
            "passed": 70,
            "failed": 40,  # 70 + 40 > 100, invalid
            "skipped": 5
        }

        raw_file = self.raw_dir / "TestRepo_tests_summary.json"
        with open(raw_file, 'w') as f:
            json.dump(raw_data, f)

        self._write_manifest()

        validator = QualityGateValidator(self.artifacts_dir, self.config_file)
        result = validator.run()

        self.assertFalse(result)

    def test_test_count_logic_valid_passes(self):
        """Test valid test count logic passes check."""
        raw_data = {
            "total": 100,
            "passed": 90,
            "failed": 5,
            "skipped": 5  # 90 + 5 + 5 = 100, valid
        }

        raw_file = self.raw_dir / "TestRepo_tests_summary.json"
        with open(raw_file, 'w') as f:
            json.dump(raw_data, f)

        self._write_manifest()

        validator = QualityGateValidator(self.artifacts_dir, self.config_file)
        result = validator.run()

        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
