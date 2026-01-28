import argparse
import os
import shutil

from .collector import Collector
from .config import load_config, get_config_value
from .exporter import export_json
from .storage import init_db, store_snapshot, purge_old
from .utils import ensure_dir


def build_parser():
    parser = argparse.ArgumentParser(prog="metrics")
    parser.add_argument("--config", default="config.yml")

    sub = parser.add_subparsers(dest="command", required=True)

    for name in ["init", "collect", "export", "build-dashboard", "run"]:
        sub_parser = sub.add_parser(name)
        sub_parser.add_argument("--config", default="config.yml")

    return parser


def cmd_init(cfg):
    db_path = get_config_value(cfg, "storage", "db_path", default="data/metrics.db")
    schema_path = get_config_value(cfg, "storage", "schema_path", default="sql/schema.sql")
    init_db(db_path, schema_path)


def cmd_collect(cfg):
    db_path = get_config_value(cfg, "storage", "db_path", default="data/metrics.db")
    schema_path = get_config_value(cfg, "storage", "schema_path", default="sql/schema.sql")
    init_db(db_path, schema_path)

    collector = Collector(cfg)
    data = collector.collect()
    store_snapshot(db_path, data)
    purge_old(db_path, data.get("retention_days", 365))


def cmd_export(cfg):
    db_path = get_config_value(cfg, "storage", "db_path", default="data/metrics.db")
    output_dir = get_config_value(cfg, "export", "output_dir", default="output")
    export_json(db_path, output_dir)


def cmd_build_dashboard(cfg):
    public_dir = get_config_value(cfg, "export", "public_dir", default="public")
    ensure_dir(public_dir)
    ui_dir = "ui"
    for name in os.listdir(ui_dir):
        src = os.path.join(ui_dir, name)
        dst = os.path.join(public_dir, name)
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    output_dir = get_config_value(cfg, "export", "output_dir", default="output")
    data_dir = os.path.join(public_dir, "data")
    ensure_dir(data_dir)
    for name in ["latest.json", "history.json"]:
        src = os.path.join(output_dir, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(data_dir, name))


def cmd_run(cfg):
    cmd_collect(cfg)
    cmd_export(cfg)
    cmd_build_dashboard(cfg)


def main():
    parser = build_parser()
    args = parser.parse_args()
    cfg = load_config(args.config)

    if args.command == "init":
        cmd_init(cfg)
    elif args.command == "collect":
        cmd_collect(cfg)
    elif args.command == "export":
        cmd_export(cfg)
    elif args.command == "build-dashboard":
        cmd_build_dashboard(cfg)
    elif args.command == "run":
        cmd_run(cfg)


if __name__ == "__main__":
    main()
