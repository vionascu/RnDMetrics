#!/usr/bin/env python3
"""
Setup script that reads projects.json and clones/configures projects for analysis.
Creates config/repos.yaml from the projects specified in projects.json.
"""

import json
import subprocess
import sys
from pathlib import Path

def setup_projects():
    """Read projects.json and setup repositories."""

    root = Path(__file__).parent.parent
    projects_file = root / "projects.json"
    config_file = root / "config" / "repos.yaml"
    projects_dir = root / ".."  # Parent directory where projects are cloned

    # Load projects
    if not projects_file.exists():
        print(f"❌ projects.json not found: {projects_file}")
        print("   Create projects.json with list of GitHub project URLs")
        return False

    with open(projects_file) as f:
        data = json.load(f)

    projects = data.get("projects", [])
    if not projects:
        print("❌ No projects defined in projects.json")
        return False

    print(f"📋 Setting up {len(projects)} project(s) from projects.json")
    print()

    # Ensure config directory
    config_file.parent.mkdir(exist_ok=True)

    # Generate repos.yaml
    repos_yaml = "# Evidence-backed metrics system configuration\n"
    repos_yaml += "# Auto-generated from projects.json\n"
    repos_yaml += "# DO NOT EDIT - modify projects.json instead\n\n"
    repos_yaml += "repos:\n"

    for i, project in enumerate(projects, 1):
        url = project.get("url", "").strip()
        if not url.startswith("https://github.com/"):
            print(f"❌ Invalid GitHub URL: {url}")
            return False

        # Extract repo name from URL
        parts = url.rstrip("/").split("/")
        owner = parts[-2]
        repo_name = parts[-1]
        project_name = f"{owner}_{repo_name}"

        # Use custom local_dir if provided, otherwise use repo_name from URL
        local_dir = project.get("local_dir", repo_name)

        print(f"{i}. {project_name}")
        print(f"   URL: {url}")

        # Check if repo exists locally
        repo_path = projects_dir / local_dir
        if not repo_path.exists():
            print(f"   Cloning...")
            try:
                subprocess.run(
                    ["git", "clone", url, str(repo_path)],
                    capture_output=True,
                    timeout=60
                )
                print(f"   ✅ Cloned to {repo_path}")
            except Exception as e:
                print(f"   ❌ Clone failed: {e}")
                return False
        else:
            print(f"   ✅ Already exists at {repo_path}")

        # Add to repos.yaml
        language = project.get("language", "mixed")
        description = project.get("description", repo_name)

        repos_yaml += f"  - name: {project_name}\n"
        repos_yaml += f"    path: ../{local_dir}\n"
        repos_yaml += f"    github_url: \"{url}\"\n"
        repos_yaml += f"    default_branch: main\n"
        repos_yaml += f"    language: {language}\n"
        repos_yaml += f"    ci_artifacts_path: ../ci_artifacts/{project_name}\n"
        repos_yaml += f"    description: \"{description}\"\n\n"

        print()

    # Add default sections to repos.yaml
    repos_yaml += """# Time zone for all timestamps
timezone: UTC

# Documentation coverage definition
docs_coverage_strategy:
  default: "code_comments"

# AI-generated code tracking
ai_tracking:
  enabled: false
  signal_type: "commit_trailer"
  signal_value: "AI-Generated: true"
  note: "No explicit AI attribution policy found. Defaulting to N/A."

# Quality gates
quality_gates:
  coverage_min_percent: 0
  test_pass_rate_min_percent: 0
  enforce_evidence_completeness: true
  enforce_determinism: true
"""

    # Write config
    with open(config_file, 'w') as f:
        f.write(repos_yaml)

    print(f"✅ Generated config file: {config_file}")
    print()
    print("Ready to run: ./run_metrics.sh")
    return True

if __name__ == "__main__":
    success = setup_projects()
    sys.exit(0 if success else 1)
