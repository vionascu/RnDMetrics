import datetime as dt
import requests
from typing import Dict, List, Any, Optional


class GitLabClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"PRIVATE-TOKEN": token})

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None):
        url = f"{self.base_url}/api/v4{path}"
        resp = self.session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_project(self, project_id: str) -> Dict[str, Any]:
        return self._get(f"/projects/{project_id}")

    def list_commits(self, project_id: str, since: dt.date) -> List[Dict[str, Any]]:
        commits = []
        page = 1
        per_page = 100
        while True:
            batch = self._get(
                f"/projects/{project_id}/repository/commits",
                params={
                    "since": since.isoformat(),
                    "per_page": per_page,
                    "page": page,
                },
            )
            if not batch:
                break
            commits.extend(batch)
            if len(batch) < per_page:
                break
            page += 1
        return commits
