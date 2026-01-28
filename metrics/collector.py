import datetime as dt
import os
import subprocess
from collections import Counter
from typing import Dict, Any

from .gitlab import GitLabClient
from .metrics_calc import calculate_repo_metrics, parse_lcov
from .utils import ensure_dir


class Collector:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def _gitlab_client(self):
        project_cfg = self.config.get("project", {})
        token_env = project_cfg.get("token_env", "GITLAB_TOKEN")
        token = os.getenv(token_env)
        if not token:
            raise RuntimeError(f"Missing GitLab token in env var: {token_env}")
        return GitLabClient(project_cfg.get("gitlab_url"), token)

    def _clone_repo(self, clone_url: str, repo_path: str, shallow: bool, depth: int):
        if os.path.exists(os.path.join(repo_path, ".git")):
            return
        ensure_dir(os.path.dirname(repo_path))
        cmd = ["git", "clone", clone_url, repo_path]
        if shallow:
            cmd.extend(["--depth", str(depth)])
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def collect(self) -> Dict[str, Any]:
        project_cfg = self.config.get("project", {})
        collection_cfg = self.config.get("collection", {})
        retention_cfg = self.config.get("retention", {})
        epics_cfg = self.config.get("epics", {})

        client = self._gitlab_client()
        project_id = project_cfg.get("project_id")
        since_days = int(collection_cfg.get("since_days", 365))
        since = dt.date.today() - dt.timedelta(days=since_days)

        project = client.get_project(project_id)
        commits = client.list_commits(project_id, since)

        daily_commits: Counter[str] = Counter()
        epic_commits: Counter[str] = Counter()
        epic_rules = epics_cfg.get("rules", [])

        for commit in commits:
            date = commit.get("created_at", "")[:10]
            if date:
                daily_commits[date] += 1
            message = commit.get("title", "") + " " + commit.get("message", "")
            for rule in epic_rules:
                key = rule.get("key")
                pattern = rule.get("pattern")
                if not key or not pattern:
                    continue
                if re_search(pattern, message):
                    epic_commits[key] += 1

        repo_path = collection_cfg.get("repo_path")
        include_paths = collection_cfg.get("include_paths", ["."])
        exclude_paths = collection_cfg.get("exclude_paths", [".git"])
        exclude_extensions = collection_cfg.get("exclude_extensions", [])
        shallow = bool(collection_cfg.get("shallow_clone", True))
        depth = int(collection_cfg.get("clone_depth", 50))

        repo_metrics = None
        coverage = None

        if repo_path:
            clone_url = project_cfg.get("repo_url") or project.get("http_url_to_repo")
            token_env = project_cfg.get("token_env", "GITLAB_TOKEN")
            token = os.getenv(token_env)
            if token and clone_url and clone_url.startswith("http"):
                parts = clone_url.split("//", 1)
                clone_url = f"{parts[0]}//oauth2:{token}@{parts[1]}"
            if clone_url:
                self._clone_repo(clone_url, repo_path, shallow, depth)
                repo_metrics = calculate_repo_metrics(
                    repo_path, include_paths, exclude_paths, exclude_extensions
                )
                coverage_path = os.path.join(repo_path, "coverage", "lcov.info")
                fallback_path = os.path.join(repo_path, "lcov.info")
                coverage = parse_lcov(coverage_path) or parse_lcov(fallback_path)

        return {
            "project": {
                "name": project.get("name"),
                "web_url": project.get("web_url"),
                "default_branch": project.get("default_branch"),
            },
            "snapshot_date": dt.date.today().isoformat(),
            "daily_commits": dict(daily_commits),
            "epic_commits": dict(epic_commits),
            "repo_metrics": repo_metrics,
            "coverage": coverage,
            "retention_days": int(retention_cfg.get("days", 365)),
        }


def re_search(pattern: str, text: str) -> bool:
    try:
        import re

        return re.search(pattern, text, re.IGNORECASE) is not None
    except re.error:
        return False
