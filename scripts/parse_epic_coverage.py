#!/usr/bin/env python3
"""
Parse test files to extract epic and user story coverage metrics.

Analyzes test structure to determine:
- Number of tests per epic
- Number of tests per user story
- Overall epic/US coverage percentages
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any


class EpicCoverageParser:
    """Parse test files to extract epic and user story coverage."""

    def __init__(self, root_dir: Path = None):
        """Initialize with repository root."""
        if root_dir is None:
            root_dir = Path(__file__).parent.parent
        self.root_dir = root_dir
        self.projects_root = root_dir.parent

    def parse_trailwaze_coverage(self) -> Dict[str, Any]:
        """Parse Trailwaze test file to extract epic/US coverage."""
        test_file = self.projects_root / "trailwaze" / "apps" / "mobile" / "__tests__" / "mvp-epics.test.js"

        if not test_file.exists():
            return {}

        with open(test_file, 'r') as f:
            content = f.read()

        # Simple approach: count describe and it blocks
        # Pattern: describe('Epic N: Title', () => {
        epic_pattern = r"describe\('(Epic \d+:[^']+)',\s*\(\)\s*=>"
        epics = []

        # Find all epic titles
        for epic_match in re.finditer(epic_pattern, content):
            epic_title = epic_match.group(1)

            # Extract epic number and name
            epic_num_match = re.match(r'Epic (\d+):\s*(.*)', epic_title)
            if not epic_num_match:
                continue

            epic_num = epic_num_match.group(1)
            epic_name = epic_num_match.group(2).strip()

            # Find position of this epic and next epic
            current_pos = epic_match.start()
            next_epic_match = re.search(epic_pattern, content[current_pos + 1:])
            end_pos = (current_pos + 1 + next_epic_match.start()) if next_epic_match else len(content)

            epic_section = content[current_pos:end_pos]

            # Find user stories in this section
            us_pattern = r"describe\('(US\d+\.\d+[^']*)',\s*\(\)\s*=>"
            user_stories = []

            for us_match in re.finditer(us_pattern, epic_section):
                us_title = us_match.group(1)

                # Find position of this US and next US
                us_pos = us_match.start()
                next_us_match = re.search(us_pattern, epic_section[us_pos + 1:])
                us_end_pos = (us_pos + 1 + next_us_match.start()) if next_us_match else len(epic_section)

                us_section = epic_section[us_pos:us_end_pos]

                # Count tests in this user story (it() or test())
                test_count = len(re.findall(r"\bit\(|\btest\(", us_section))

                user_stories.append({
                    "id": us_title.split(' ')[0],
                    "title": us_title,
                    "test_count": test_count
                })

            # Total tests for this epic
            total_epic_tests = sum(us["test_count"] for us in user_stories)

            epics.append({
                "epic_id": f"epic-{epic_num}",
                "epic_number": epic_num,
                "epic_title": epic_name,
                "total_tests": total_epic_tests,
                "user_stories": user_stories,
                "us_count": len(user_stories)
            })

        return {
            "project": "vionascu_trailwaze",
            "source_file": str(test_file),
            "collection_method": "Jest test file parsing",
            "epics": epics,
            "total_epics": len(epics),
            "total_user_stories": sum(e["us_count"] for e in epics),
            "total_tests": sum(e["total_tests"] for e in epics)
        }

    def parse_trail_equip_coverage(self) -> Dict[str, Any]:
        """Parse Trail-Equip test files to extract epic/US coverage."""
        repo_path = self.projects_root / "TrailEquip"

        if not repo_path.exists():
            return {}

        # Find all test files
        test_files = list(repo_path.rglob("*Test.java")) + list(repo_path.rglob("*IT.java"))

        if not test_files:
            return {}

        # Read MVP_EPICS.md to get epic and US structure
        mvp_file = repo_path / "docs" / "MVP_EPICS.md"
        if not mvp_file.exists():
            return {}

        with open(mvp_file, 'r') as f:
            mvp_content = f.read()

        # Extract epics and user stories from MVP_EPICS.md
        # Build a map of epic number -> user stories
        epics_map = {}

        # Parse user stories first: #### US N.N - Title
        us_pattern = r"#### US([\d.]+) - (.+)"
        for us_match in re.finditer(us_pattern, mvp_content):
            us_id = us_match.group(1)
            us_title = us_match.group(2).strip()
            epic_num = us_id.split('.')[0]  # Extract epic number from US1.1 -> 1

            if epic_num not in epics_map:
                epics_map[epic_num] = {"user_stories": []}

            # Count tests for this US
            test_count = sum(1 for f in test_files if us_id.replace(".", "") in f.read_text(errors='ignore'))

            epics_map[epic_num]["user_stories"].append({
                "id": f"US{us_id}",
                "title": us_title,
                "test_count": test_count
            })

        # Now parse epics: ### EPIC N: Title (only unique ones)
        epic_pattern = r"### EPIC\s+(\d+):\s*([^\n]+)"
        epics = []
        seen_epics = set()

        for epic_match in re.finditer(epic_pattern, mvp_content):
            epic_num = epic_match.group(1)
            epic_title = epic_match.group(2).strip()

            if epic_num not in seen_epics:
                user_stories = epics_map.get(epic_num, {}).get("user_stories", [])
                total_epic_tests = sum(us["test_count"] for us in user_stories)

                epics.append({
                    "epic_id": f"epic-{epic_num}",
                    "epic_number": epic_num,
                    "epic_title": epic_title,
                    "user_stories": user_stories,
                    "us_count": len(user_stories),
                    "total_tests": total_epic_tests
                })
                seen_epics.add(epic_num)

        return {
            "project": "vionascu_trail-equip",
            "source_file": str(mvp_file),
            "collection_method": "MVP_EPICS.md + test file analysis",
            "epics": epics,
            "total_epics": len(epics),
            "total_user_stories": sum(e["us_count"] for e in epics),
            "total_tests": len(test_files),
            "test_files_found": len(test_files)
        }

    def run(self) -> bool:
        """Parse all projects and generate coverage metrics."""
        print("[EPIC COVERAGE] Parsing test files for epic/US breakdown...")
        print()

        coverage_data = {}

        # Parse Trailwaze
        print("📊 Trailwaze...")
        trailwaze_coverage = self.parse_trailwaze_coverage()
        if trailwaze_coverage:
            coverage_data["vionascu_trailwaze"] = trailwaze_coverage
            print(f"   ✅ {trailwaze_coverage['total_epics']} epics")
            print(f"   ✅ {trailwaze_coverage['total_user_stories']} user stories")
            print(f"   ✅ {trailwaze_coverage['total_tests']} tests")

        # Parse Trail-Equip
        print("📊 Trail-Equip...")
        trail_equip_coverage = self.parse_trail_equip_coverage()
        if trail_equip_coverage:
            coverage_data["vionascu_trail-equip"] = trail_equip_coverage
            print(f"   ✅ {trail_equip_coverage['total_epics']} epics")
            print(f"   ✅ {trail_equip_coverage['total_user_stories']} user stories")
            print(f"   ✅ {trail_equip_coverage['total_tests']} tests")

        print()

        # Write coverage data
        output_file = self.root_dir / "artifacts" / "raw" / "epic_coverage.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(coverage_data, f, indent=2)

        print(f"✅ Epic coverage data written to: {output_file}")
        return True


def main():
    """Main entry point."""
    try:
        parser = EpicCoverageParser()
        success = parser.run()
        return 0 if success else 1
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
