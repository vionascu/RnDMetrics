import yaml
from typing import Any, Dict


def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def get_config_value(cfg: Dict[str, Any], *keys, default=None):
    current = cfg
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current
