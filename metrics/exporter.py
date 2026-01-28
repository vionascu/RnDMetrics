import json
import sqlite3
from typing import Dict, Any

from .utils import ensure_dir


def export_json(db_path: str, output_dir: str):
    ensure_dir(output_dir)
    latest = build_latest(db_path)
    history = build_history(db_path)

    with open(f"{output_dir}/latest.json", "w", encoding="utf-8") as f:
        json.dump(latest, f, indent=2)
    with open(f"{output_dir}/history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def build_latest(db_path: str) -> Dict[str, Any]:
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT id, snapshot_date FROM snapshots ORDER BY snapshot_date DESC LIMIT 1"
        ).fetchone()
        if not row:
            return {}
        snapshot_id, snapshot_date = row

        loc = conn.execute(
            "SELECT total FROM loc_totals WHERE snapshot_id = ?",
            (snapshot_id,),
        ).fetchone()
        tests = conn.execute(
            "SELECT count FROM test_totals WHERE snapshot_id = ?",
            (snapshot_id,),
        ).fetchone()

        file_types = conn.execute(
            "SELECT extension, files FROM file_types WHERE snapshot_id = ? ORDER BY files DESC LIMIT 12",
            (snapshot_id,),
        ).fetchall()

        epics = conn.execute(
            "SELECT epic_key, commits FROM epic_stats WHERE snapshot_id = ? ORDER BY commits DESC",
            (snapshot_id,),
        ).fetchall()

        source_files = conn.execute(
            "SELECT path, loc, extension FROM source_files WHERE snapshot_id = ? ORDER BY loc DESC LIMIT 20",
            (snapshot_id,),
        ).fetchall()

        coverage = conn.execute(
            "SELECT line_rate, branch_rate FROM coverage_totals WHERE snapshot_id = ?",
            (snapshot_id,),
        ).fetchone()

        return {
            "snapshot_date": snapshot_date,
            "loc_total": loc[0] if loc else None,
            "test_files": tests[0] if tests else None,
            "file_types": [{"extension": ext, "files": files} for ext, files in file_types],
            "epics": [{"key": key, "commits": commits} for key, commits in epics],
            "source_files": [
                {"path": path, "loc": loc, "extension": ext}
                for path, loc, ext in source_files
            ],
            "coverage": {
                "line_rate": coverage[0],
                "branch_rate": coverage[1],
            }
            if coverage
            else None,
        }


def build_history(db_path: str) -> Dict[str, Any]:
    with sqlite3.connect(db_path) as conn:
        snapshots = conn.execute(
            "SELECT id, snapshot_date FROM snapshots ORDER BY snapshot_date ASC"
        ).fetchall()
        dates = [row[1] for row in snapshots]

        commits_by_date: Dict[str, int] = {}
        for snapshot_id, _ in snapshots:
            commit_sum = conn.execute(
                "SELECT SUM(count) FROM commit_counts WHERE snapshot_id = ?",
                (snapshot_id,),
            ).fetchone()[0]
            commits_by_date[snapshot_id] = commit_sum or 0

        loc_by_date: Dict[str, int] = {}
        for snapshot_id, _ in snapshots:
            loc = conn.execute(
                "SELECT total FROM loc_totals WHERE snapshot_id = ?",
                (snapshot_id,),
            ).fetchone()
            loc_by_date[snapshot_id] = loc[0] if loc and loc[0] is not None else 0

        tests_by_date: Dict[str, int] = {}
        for snapshot_id, _ in snapshots:
            tests = conn.execute(
                "SELECT count FROM test_totals WHERE snapshot_id = ?",
                (snapshot_id,),
            ).fetchone()
            tests_by_date[snapshot_id] = tests[0] if tests and tests[0] is not None else 0

        return {
            "dates": dates,
            "commits": [commits_by_date[sid] for sid, _ in snapshots],
            "loc": [loc_by_date[sid] for sid, _ in snapshots],
            "tests": [tests_by_date[sid] for sid, _ in snapshots],
        }
