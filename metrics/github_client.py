"""GitHub API client for collecting deployment and PR metrics."""

import os
import time
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class GitHubClient:
    """GitHub API client with rate limiting, caching, and graceful degradation."""

    def __init__(self, token: Optional[str] = None, base_url: str = "https://api.github.com"):
        """Initialize GitHub API client.

        Args:
            token: GitHub personal access token (falls back to GITHUB_TOKEN env var)
            base_url: GitHub API base URL
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.base_url = base_url.rstrip("/")

        # Setup caching
        self.cache_dir = Path(".cache/github")
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        self.cache_enabled = os.getenv("GITHUB_ENABLE_CACHING", "true").lower() == "true"
        self.cache_ttl_hours = 1  # Default 1 hour TTL

        # Rate limiting
        self.max_requests_per_hour = int(os.getenv("GITHUB_MAX_REQUESTS_PER_HOUR", "4500"))
        self.request_times = []

        # Session setup with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        if self.token:
            self.session.headers.update({
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            })
        else:
            print("⚠️  Warning: No GitHub token provided. Using public API (limited to 60 requests/hour)")

    def _get_cache_key(self, endpoint: str, params: Dict[str, Any]) -> str:
        """Generate cache key from endpoint and parameters."""
        key = f"{endpoint}_{json.dumps(params, sort_keys=True)}"
        return hashlib.sha256(key.encode()).hexdigest()

    def _get_cached(self, cache_key: str, max_age_hours: int = 1) -> Optional[Any]:
        """Retrieve cached response if available and not expired."""
        if not self.cache_enabled:
            return None

        cache_file = self.cache_dir / f"{cache_key}.json"
        if not cache_file.exists():
            return None

        age_seconds = time.time() - cache_file.stat().st_mtime
        if age_seconds > max_age_hours * 3600:
            return None  # Cache expired

        try:
            with open(cache_file) as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error reading cache: {e}")
            return None

    def _save_cache(self, cache_key: str, data: Any) -> None:
        """Save data to cache."""
        if not self.cache_enabled:
            return

        try:
            cache_file = self.cache_dir / f"{cache_key}.json"
            with open(cache_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"⚠️  Error saving cache: {e}")

    def _check_rate_limit(self) -> None:
        """Check and enforce rate limiting."""
        now = time.time()
        # Remove requests older than 1 hour
        self.request_times = [t for t in self.request_times if now - t < 3600]

        if len(self.request_times) >= self.max_requests_per_hour:
            # Calculate sleep time
            oldest_request = self.request_times[0]
            sleep_time = 3600 - (now - oldest_request)
            if sleep_time > 0:
                print(f"⚠️  Rate limit approaching ({len(self.request_times)}/{self.max_requests_per_hour}). Sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)
                self.request_times = []

        self.request_times.append(now)

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request to GitHub API with caching."""
        params = params or {}

        # Try cache first
        cache_key = self._get_cache_key(endpoint, params)
        cached = self._get_cached(cache_key, max_age_hours=self.cache_ttl_hours)
        if cached is not None:
            return cached

        # Check rate limit
        self._check_rate_limit()

        # Make request
        url = f"{self.base_url}{endpoint}"
        try:
            resp = self.session.get(url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            # Cache successful response
            self._save_cache(cache_key, data)
            return data

        except requests.exceptions.RequestException as e:
            print(f"❌ GitHub API error: {e}")
            # Return empty list/dict on error
            return {} if "list" not in endpoint else []

    def _paginate(self, endpoint: str, params: Optional[Dict[str, Any]] = None, per_page: int = 100) -> List[Dict[str, Any]]:
        """Paginate through GitHub API results."""
        params = params or {}
        results = []
        page = 1

        while True:
            params.update({"per_page": per_page, "page": page})
            batch = self._get(endpoint, params)

            if not isinstance(batch, list):
                # Single object returned, not paginated
                return [batch] if batch else []

            if not batch:
                break

            results.extend(batch)

            if len(batch) < per_page:
                break

            page += 1

        return results

    def get_releases(self, owner: str, repo: str, since: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get repository releases (deployments).

        Args:
            owner: GitHub repository owner
            repo: GitHub repository name
            since: Optional datetime to filter releases after this time

        Returns:
            List of release dictionaries
        """
        endpoint = f"/repos/{owner}/{repo}/releases"
        releases = self._paginate(endpoint, params={"per_page": 100})

        # Filter by date if provided
        if since:
            releases = [
                r for r in releases
                if r.get("published_at") and datetime.fromisoformat(r["published_at"].replace("Z", "+00:00")) >= since
            ]

        return releases

    def get_pull_requests(self, owner: str, repo: str, since: Optional[datetime] = None,
                         state: str = "closed") -> List[Dict[str, Any]]:
        """Get merged pull requests (for lead time and cycle time).

        Args:
            owner: GitHub repository owner
            repo: GitHub repository name
            since: Optional datetime to filter PRs after this time
            state: PR state filter (closed, merged, all) - defaults to closed

        Returns:
            List of PR dictionaries with merged_at and created_at
        """
        endpoint = f"/repos/{owner}/{repo}/pulls"
        prs = self._paginate(endpoint, params={
            "state": state,
            "sort": "updated",
            "direction": "desc",
            "per_page": 100
        })

        # Filter only merged PRs and by date if provided
        merged_prs = []
        for pr in prs:
            if not pr.get("merged_at"):
                continue

            merged_at = datetime.fromisoformat(pr["merged_at"].replace("Z", "+00:00"))
            if since and merged_at < since:
                continue

            merged_prs.append(pr)

        return merged_prs

    def search_commits(self, owner: str, repo: str, query: str, since: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Search commits by message (for failure/revert detection).

        Args:
            owner: GitHub repository owner
            repo: GitHub repository name
            query: Search query (e.g., "revert", "rollback")
            since: Optional datetime to filter commits after this time

        Returns:
            List of matching commit dictionaries
        """
        endpoint = f"/repos/{owner}/{repo}/commits"

        # Build search parameters
        params = {"q": query}
        if since:
            params["since"] = since.isoformat()

        try:
            # Use search endpoint
            search_endpoint = f"/search/commits"
            search_query = f"repo:{owner}/{repo} {query}"
            if since:
                search_query += f" committer-date:>={since.isoformat()}"

            results = self._get(search_endpoint, params={"q": search_query, "per_page": 100})
            return results.get("items", []) if isinstance(results, dict) else []

        except Exception as e:
            print(f"⚠️  Error searching commits: {e}")
            # Fallback to listing commits (less efficient but works)
            commits = self._paginate(endpoint, params=params, per_page=100)

            # Filter by keyword manually
            keyword_commits = [
                c for c in commits
                if query.lower() in c.get("commit", {}).get("message", "").lower()
            ]
            return keyword_commits

    def get_commit(self, owner: str, repo: str, sha: str) -> Dict[str, Any]:
        """Get a specific commit.

        Args:
            owner: GitHub repository owner
            repo: GitHub repository name
            sha: Commit SHA

        Returns:
            Commit dictionary
        """
        endpoint = f"/repos/{owner}/{repo}/commits/{sha}"
        return self._get(endpoint)

    def get_deployment_status(self, owner: str, repo: str, deployment_id: int) -> Dict[str, Any]:
        """Get deployment status (success/failure).

        Args:
            owner: GitHub repository owner
            repo: GitHub repository name
            deployment_id: Deployment ID

        Returns:
            Deployment status dictionary
        """
        endpoint = f"/repos/{owner}/{repo}/deployments/{deployment_id}/statuses"
        statuses = self._paginate(endpoint, per_page=100)

        # Return the most recent status
        return statuses[0] if statuses else {}


def get_github_client() -> Optional[GitHubClient]:
    """Factory function to get authenticated GitHub client."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("⚠️  GITHUB_TOKEN not set. GitHub API features will be limited.")
        return GitHubClient()  # Returns unauthenticated client
    return GitHubClient(token=token)


if __name__ == "__main__":
    # Test the client
    client = get_github_client()

    print("Testing GitHub API client...")
    print(f"Token available: {bool(client.token)}")
    print(f"Cache enabled: {client.cache_enabled}")
    print(f"Rate limit: {client.max_requests_per_hour} requests/hour")

    # Test with public repo
    try:
        releases = client.get_releases("torvalds", "linux")
        print(f"✅ Can fetch releases: found {len(releases)} releases")
    except Exception as e:
        print(f"❌ Error fetching releases: {e}")

    print("GitHub client ready!")
