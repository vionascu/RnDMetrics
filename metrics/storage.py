import sqlite3
from typing import Dict, Any

from .utils import ensure_dir, utc_now_iso


def init_db(db_path: str, schema_path: str):
    ensure_dir(db_path.rsplit("/", 1)[0])
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = f.read()
    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema)


def store_snapshot(db_path: str, data: Dict[str, Any]):
    snapshot_date = data["snapshot_date"]
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT OR IGNORE INTO snapshots(snapshot_date, created_at) VALUES (?, ?)",
            (snapshot_date, utc_now_iso()),
        )
        snapshot_id = conn.execute(
            "SELECT id FROM snapshots WHERE snapshot_date = ?",
            (snapshot_date,),
        ).fetchone()[0]

        for date, count in data["daily_commits"].items():
            conn.execute(
                "INSERT OR REPLACE INTO commit_counts(snapshot_id, date, count) VALUES (?, ?, ?)",
                (snapshot_id, date, count),
            )

        repo_metrics = data.get("repo_metrics")
        if repo_metrics:
            conn.execute(
                "INSERT OR REPLACE INTO loc_totals(snapshot_id, total, code, comment, blank) VALUES (?, ?, ?, ?, ?)",
                (snapshot_id, repo_metrics["total_loc"], None, None, None),
            )
            conn.execute(
                "INSERT OR REPLACE INTO test_totals(snapshot_id, count) VALUES (?, ?)",
                (snapshot_id, repo_metrics["test_count"]),
            )
            for (ext, count) in repo_metrics["file_types"].items():
                conn.execute(
                    "INSERT OR REPLACE INTO file_types(snapshot_id, extension, files, loc) VALUES (?, ?, ?, ?)",
                    (snapshot_id, ext, count, None),
                )
            for path, loc, ext in repo_metrics["source_files"]:
                conn.execute(
                    "INSERT OR REPLACE INTO source_files(snapshot_id, path, loc, extension) VALUES (?, ?, ?, ?)",
                    (snapshot_id, path, loc, ext),
                )

        for key, count in data.get("epic_commits", {}).items():
            conn.execute(
                "INSERT OR REPLACE INTO epic_stats(snapshot_id, epic_key, commits, loc) VALUES (?, ?, ?, ?)",
                (snapshot_id, key, count, None),
            )

        coverage = data.get("coverage")
        if coverage:
            conn.execute(
                "INSERT OR REPLACE INTO coverage_totals(snapshot_id, line_rate, branch_rate) VALUES (?, ?, ?)",
                (snapshot_id, coverage.get("line_rate"), coverage.get("branch_rate")),
            )


def purge_old(db_path: str, retention_days: int):
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "DELETE FROM snapshots WHERE snapshot_date < date('now', ?) ",
            (f"-{retention_days} days",),
        )
