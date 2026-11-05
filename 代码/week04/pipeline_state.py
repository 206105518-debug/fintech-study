"""管道运行状态与本地元数据管理。"""

import json
from datetime import datetime

import pandas as pd

from pipeline_config import (
    ADJUST,
    CONFIG,
    DAILY_COVERAGE_FILE,
    LOG_FILE,
    MANIFEST_FILE,
    REQUIRED_OUTPUTS,
    data_dir,
)


def log(msg):
    """同时输出到终端和当天的日志文件。"""
    line = f"[{datetime.now():%H:%M:%S}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def can_skip():
    """上次成功参数相同、结果文件齐全时返回 True。"""
    if not MANIFEST_FILE.exists():
        return False

    if not all(path.exists() for path in REQUIRED_OUTPUTS):
        return False

    try:
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except (OSError, json.JSONDecodeError):
        return False

    return (
        manifest.get("status") == "success"
        and manifest.get("start") == CONFIG["start"]
        and manifest.get("end") == CONFIG["end"]
        and manifest.get("max_stocks") == CONFIG["max_stocks"]
    )


def write_manifest():
    """全部步骤成功后，记录本次运行参数。"""
    manifest = {
        "status": "success",
        "start": CONFIG["start"],
        "end": CONFIG["end"],
        "max_stocks": CONFIG["max_stocks"],
        "completed_at": datetime.now().isoformat(timespec="seconds"),
    }
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def load_daily_coverage():
    """读取每只股票已经覆盖的请求日期范围。"""
    if not DAILY_COVERAGE_FILE.exists():
        return {}

    try:
        with open(DAILY_COVERAGE_FILE, "r", encoding="utf-8") as f:
            coverage = json.load(f)
    except (OSError, json.JSONDecodeError):
        log("daily_coverage.json 损坏，将重新建立")
        return {}

    return coverage if isinstance(coverage, dict) else {}


def save_daily_coverage(coverage):
    """保存日线日期覆盖清单。"""
    with open(DAILY_COVERAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(coverage, f, ensure_ascii=False, indent=2)


def bootstrap_daily_coverage(existing):
    """旧版本没有覆盖清单时，根据上次成功运行记录初始化。"""
    coverage = load_daily_coverage()
    if coverage or existing.empty or not MANIFEST_FILE.exists():
        return coverage

    try:
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except (OSError, json.JSONDecodeError):
        return coverage

    if manifest.get("status") != "success":
        return coverage

    for code in existing["股票代码"].astype(str).str.zfill(6).unique():
        coverage[code] = {
            "start": manifest["start"],
            "end": manifest["end"],
            "adjust": ADJUST,
        }

    save_daily_coverage(coverage)
    log(f"已从运行清单建立 {len(coverage)} 只股票的日线覆盖记录")
    return coverage


def save_failures(failures, name):
    """保存失败清单；没有失败时保留表头。"""
    df = pd.DataFrame(failures, columns=["代码", "原因"])
    path = data_dir / f"failed_{name}.csv"
    df.to_csv(path, index=False, encoding="utf-8-sig")
    log(f"{name}失败清单已保存：{len(df)}只")


def save(df, name):
    """把清洗后的表保存到 data/clean_<name>.csv。"""
    path = data_dir / f"clean_{name}.csv"
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"已存 {path}：{df.shape[0]} 行 × {df.shape[1]} 列")