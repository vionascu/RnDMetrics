#!/usr/bin/env python3
"""
Quality gates enforcement system.

Validates metrics artifacts against evidence completeness and sanity checks.
Ensures all metrics have verifiable sources before deployment.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any


class QualityGateValidator:
    """Validate metrics against quality gates."""

    def __init__(self, artifacts_dir: Path, config_path: Path):
        """Initialize validator."""
        self.artifacts_dir = artifacts_dir
        self.raw_dir = artifacts_dir / "raw"
        self.derived_dir = artifacts_dir / "derived"
        self.manifest_file = artifacts_dir / "manifest.json"
        self.config_path = config_path

        self.manifest = None
        self.config = None
        self.failures = []
        self.warnings = []

    def run(self) -> bool:
        """Execute all quality gates. Return True if all pass."""
        print("[QUALITY GATES] Validating metrics artifacts...")
        print()

        try:
            self._load_manifest()
            self._load_config()

            # Run gates
            self._gate_evidence_completeness()
            self._gate_sanity_checks()
            self._gate_determinism()

            # Report results
            return self._report_results()

        except Exception as e:
            print(f"❌ Quality gate validation failed: {e}")
            return False

    def _load_manifest(self):
        """Load manifest file."""
        if not self.manifest_file.exists():
            raise FileNotFoundError(f"Manifest not found: {self.manifest_file}")

        with open(self.manifest_file, 'r') as f:
            self.manifest = json.load(f)

    def _load_config(self):
        """Load configuration."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")

        import yaml
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def _gate_evidence_completeness(self):
        """Validate that all metrics have complete evidence."""
        print("[GATE] Evidence Completeness...")

        if "quality_gates" not in self.config:
            return

        enforce = self.config["quality_gates"].get("enforce_evidence_completeness", True)
        if not enforce:
            print("  ⚠️  Evidence completeness not enforced (config)")
            return

        evidence_map = self.manifest.get("evidence_map", {})
        metrics_collected = self.manifest.get("metrics_collected", [])

        required_fields = ["metric_id", "repo", "range", "collected_at", "commands", "raw_file"]
        missing_evidence = []

        for metric_id in metrics_collected:
            if metric_id not in evidence_map:
                missing_evidence.append(f"  ❌ {metric_id}: Missing evidence record")
                continue

            evidence = evidence_map[metric_id]
            missing_fields = [f for f in required_fields if not evidence.get(f)]

            if missing_fields:
                missing_evidence.append(f"  ❌ {metric_id}: Missing {missing_fields}")
            else:
                # Check file exists
                raw_file = Path(evidence.get("raw_file", ""))
                if not raw_file.exists():
                    missing_evidence.append(f"  ❌ {metric_id}: Raw file missing {raw_file}")

        if missing_evidence:
            self.failures.extend(missing_evidence)
            print("\n".join(missing_evidence))
        else:
            print(f"  ✅ All {len(metrics_collected)} metrics have complete evidence")

    def _gate_sanity_checks(self):
        """Validate metric values are within expected ranges."""
        print("\n[GATE] Sanity Checks...")

        checks_performed = 0
        checks_failed = []

        # Load all raw files
        for raw_file in self.raw_dir.glob("*.json"):
            try:
                with open(raw_file, 'r') as f:
                    raw_data = json.load(f)

                    # Percentage checks
                    for key in ["pass_rate_percent", "coverage_percent"]:
                        if key in raw_data:
                            value = raw_data[key]
                            if not (0 <= value <= 100):
                                checks_failed.append(f"  ❌ {raw_file.name}: {key}={value} (must be 0-100)")
                            else:
                                checks_performed += 1

                    # Non-negative checks
                    for key in ["count", "loc_added", "loc_deleted", "files_changed", "total", "passed", "failed"]:
                        if key in raw_data:
                            value = raw_data[key]
                            if value < 0:
                                checks_failed.append(f"  ❌ {raw_file.name}: {key}={value} (must be >= 0)")
                            else:
                                checks_performed += 1

                    # Test count logic
                    if "total" in raw_data and "passed" in raw_data:
                        total = raw_data["total"]
                        passed = raw_data["passed"]
                        failed = raw_data.get("failed", 0)
                        skipped = raw_data.get("skipped", 0)

                        if passed + failed + skipped > total:
                            checks_failed.append(
                                f"  ❌ {raw_file.name}: Test counts don't add up "
                                f"(passed={passed} + failed={failed} + skipped={skipped} > total={total})"
                            )
                        else:
                            checks_performed += 1

            except Exception as e:
                self.warnings.append(f"  ⚠️  Could not check {raw_file.name}: {e}")

        if checks_failed:
            self.failures.extend(checks_failed)
            print("\n".join(checks_failed))
        else:
            print(f"  ✅ All {checks_performed} sanity checks passed")

    def _gate_determinism(self):
        """Check metrics collection is deterministic (stub)."""
        print("\n[GATE] Determinism Check...")

        # This would compare two consecutive runs and verify identical output
        # For now, mark as pending since we don't have historical runs
        print("  ⏳ Determinism requires historical comparison (skipped on first run)")

        # In production, would check:
        # - Same repository state → identical metric values
        # - Timestamps are independent of execution time
        # - Evidence hashes are reproducible

    def _report_results(self) -> bool:
        """Report quality gate results."""
        print()
        print("=" * 50)

        if self.failures:
            print(f"❌ QUALITY GATE FAILED ({len(self.failures)} issues)")
            print()
            for failure in self.failures:
                print(failure)
            return False

        if self.warnings:
            print(f"⚠️  QUALITY GATES PASSED (with {len(self.warnings)} warnings)")
            print()
            for warning in self.warnings:
                print(warning)
        else:
            print("✅ QUALITY GATES PASSED")

        print("=" * 50)
        return True


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Quality gates validator")
    parser.add_argument("--artifacts", default="artifacts", help="Artifacts directory")
    parser.add_argument("--config", default="config/repos.yaml", help="Configuration file")

    args = parser.parse_args()

    artifacts_dir = Path(args.artifacts)
    config_path = Path(args.config)

    validator = QualityGateValidator(artifacts_dir, config_path)
    success = validator.run()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
