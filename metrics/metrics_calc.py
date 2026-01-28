import os
import re
from collections import Counter
from typing import Dict, List, Tuple, Optional


TEST_PATTERNS = [
    re.compile(r"test_.*\.py$"),
    re.compile(r".*_test\.py$"),
    re.compile(r".*\.spec\.(js|ts)$"),
    re.compile(r".*\.test\.(js|ts)$"),
    re.compile(r".*Test\.java$"),
]


def is_test_file(path: str) -> bool:
    name = os.path.basename(path)
    return any(p.search(name) for p in TEST_PATTERNS)


def file_extension(path: str) -> str:
    base = os.path.basename(path)
    if "." not in base:
        return ""
    return base.split(".")[-1].lower()


def count_lines(path: str) -> int:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except OSError:
        return 0


def scan_repo(root: str, include_paths: List[str], exclude_paths: List[str]):
    files: List[str] = []
    for inc in include_paths:
        base = os.path.join(root, inc)
        for dirpath, dirnames, filenames in os.walk(base):
            rel = os.path.relpath(dirpath, root)
            if any(part in exclude_paths for part in rel.split(os.sep)):
                dirnames[:] = []
                continue
            for name in filenames:
                rel_file = os.path.relpath(os.path.join(dirpath, name), root)
                if any(part in exclude_paths for part in rel_file.split(os.sep)):
                    continue
                files.append(rel_file)
    return files


def calculate_repo_metrics(
    root: str,
    include_paths: List[str],
    exclude_paths: List[str],
    exclude_extensions: Optional[List[str]] = None,
):
    files = scan_repo(root, include_paths, exclude_paths)
    file_types = Counter()
    source_files: List[Tuple[str, int, str]] = []
    total_loc = 0
    test_count = 0
    excluded = {ext.lower().lstrip(".") for ext in (exclude_extensions or [])}

    for rel_path in files:
        abs_path = os.path.join(root, rel_path)
        ext = file_extension(rel_path)
        if ext in excluded:
            continue
        loc = count_lines(abs_path)
        file_types[(ext or "(none)")] += 1
        source_files.append((rel_path, loc, ext))
        total_loc += loc
        if is_test_file(rel_path):
            test_count += 1

    return {
        "total_loc": total_loc,
        "test_count": test_count,
        "file_types": file_types,
        "source_files": source_files,
    }


def parse_lcov(path: str):
    if not os.path.exists(path):
        return None
    lf = lh = brf = brh = 0
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.startswith("LF:"):
                    lf += int(line.split(":", 1)[1].strip())
                elif line.startswith("LH:"):
                    lh += int(line.split(":", 1)[1].strip())
                elif line.startswith("BRF:"):
                    brf += int(line.split(":", 1)[1].strip())
                elif line.startswith("BRH:"):
                    brh += int(line.split(":", 1)[1].strip())
    except OSError:
        return None

    line_rate = (lh / lf) if lf else None
    branch_rate = (brh / brf) if brf else None
    return {"line_rate": line_rate, "branch_rate": branch_rate}
