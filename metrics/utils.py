import datetime as dt
import os
from pathlib import Path


def utc_now_iso():
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def today_date():
    return dt.date.today().isoformat()


def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def safe_join(base: str, *parts: str) -> str:
    return str(Path(base).joinpath(*parts))


def env_required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def normalize_path(path: str) -> str:
    return str(Path(path).resolve())
