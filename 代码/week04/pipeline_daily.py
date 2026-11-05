"""日线批量下载、日期增量判断与合并。"""

import time

import pandas as pd

from fetchers import fetch_daily
from pipeline_config import ADJUST, CONFIG, data_dir
from pipeline_state import (
    bootstrap_daily_coverage,
    save_daily_coverage,
)
from pipeline_transform import (
    clean_daily,
    filter_daily_range,
    missing_periods,
)


def daily_periods_to_fetch(code, coverage, has_current=True):
    """根据覆盖清单决定单只股票要请求的日期段。"""
    target_start = CONFIG["start"]
    target_end = CONFIG["end"]

    if not has_current:
        return [(target_start, target_end)]

    old = coverage.get(code)
    if old is None or old.get("adjust") != ADJUST:
        return [(target_start, target_end)]

    covered = (
        old.get("start", "99999999") <= target_start
        and old.get("end", "00000000") >= target_end
    )
    if covered:
        return []

    return missing_periods(
        old["start"],
        old["end"],
        target_start,
        target_end,
    )


def fetch_daily_incremental(code, current, coverage):
    """补齐单只股票缺失的日期段。

    返回 (数据, 是否成功, 新覆盖范围, 是否访问接口)。
    """
    periods = daily_periods_to_fetch(
        code,
        coverage,
        has_current=not current.empty,
    )
    old = coverage.get(code)
    new_coverage = {
        "start": CONFIG["start"],
        "end": CONFIG["end"],
        "adjust": ADJUST,
    }

    if not periods:
        return filter_daily_range(current), True, new_coverage, False

    parts = [] if current.empty else [current]

    for start, end in periods:
        print(f"{code} 增量拉取 {start}-{end}")
        data = fetch_daily(code, start, end, adjust=ADJUST)
        if data is None or data.empty:
            return filter_daily_range(current), False, old, True
        parts.append(data)

    merged = pd.concat(parts, ignore_index=True)
    merged = clean_daily(merged)
    return filter_daily_range(merged), True, new_coverage, True


def fetch_daily_all(codes, force=False):
    """批量更新日线，返回合并后的日线和失败清单。"""
    daily_path = data_dir / "clean_daily.csv"
    old_daily = (
        pd.read_csv(daily_path, dtype={"股票代码": str})
        if daily_path.exists()
        else pd.DataFrame()
    )

    coverage = {} if force else bootstrap_daily_coverage(old_daily)
    results = []
    failures = []

    for i, code in enumerate(codes, start=1):
        current = (
            old_daily[
                old_daily["股票代码"].astype(str).str.zfill(6) == code
            ].copy()
            if not old_daily.empty
            else pd.DataFrame()
        )
        requested = False

        try:
            data, ok, new_coverage, requested = fetch_daily_incremental(
                code,
                current,
                coverage,
            )

            if ok:
                results.append(data)
                coverage[code] = new_coverage
                action = "接口更新" if requested else "缓存命中"
                print(f"{i}/{len(codes)} {code} {len(data)}行（{action}）")
            else:
                failures.append({
                    "代码": code,
                    "原因": "拉取或增量更新失败",
                })
                if not data.empty:
                    results.append(data)
                print(f"{i}/{len(codes)} {code} 失败，保留旧数据")

        except Exception as exc:
            failures.append({"代码": code, "原因": str(exc)})
            if not current.empty:
                results.append(filter_daily_range(current))
            print(f"{i}/{len(codes)} {code} 异常：{type(exc).__name__}")

        if requested:
            time.sleep(CONFIG["sleep_sec"])

    save_daily_coverage(coverage)

    if not results:
        return pd.DataFrame(), failures

    combined = pd.concat(results, ignore_index=True)
    combined = clean_daily(combined)
    combined = filter_daily_range(combined)
    return combined, failures