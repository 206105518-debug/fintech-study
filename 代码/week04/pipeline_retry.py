"""只重试日线失败股票并更新相关结果。"""

import time

import pandas as pd

from pipeline_config import CONFIG, data_dir
from pipeline_daily import fetch_daily_incremental
from pipeline_quality import refresh_quality_report
from pipeline_state import (
    bootstrap_daily_coverage,
    log,
    save,
    save_daily_coverage,
    save_failures,
    write_manifest,
)
from pipeline_transform import clean_daily


def retry_failed_daily():
    """只重试 failed_daily.csv 中的股票，并合并回现有日线。"""
    failed_path = data_dir / "failed_daily.csv"
    daily_path = data_dir / "clean_daily.csv"

    if not failed_path.exists():
        log("没有 failed_daily.csv，无需重试")
        return

    if not daily_path.exists():
        log("clean_daily.csv 不存在，请先完整运行一次")
        return

    failed = pd.read_csv(failed_path, dtype={"代码": str})
    if failed.empty:
        log("失败清单为空，无需重试")
        return

    old_daily = pd.read_csv(daily_path, dtype={"股票代码": str})
    coverage = bootstrap_daily_coverage(old_daily)
    successful = []
    remaining_failed = []
    codes = failed["代码"].astype(str).str.zfill(6).drop_duplicates()

    for i, code in enumerate(codes, start=1):
        log(f"重试 {i}/{len(codes)}：{code}")
        current = old_daily[
            old_daily["股票代码"].astype(str).str.zfill(6) == code
        ].copy()

        data, ok, new_coverage, requested = fetch_daily_incremental(
            code,
            current,
            coverage,
        )

        if not ok:
            remaining_failed.append({
                "代码": code,
                "原因": "重试后仍未取到数据",
            })
            log(f"{code} 重试失败")
        else:
            successful.append(data)
            coverage[code] = new_coverage
            log(f"{code} 重试成功：{len(data)} 行")

        if requested:
            time.sleep(CONFIG["sleep_sec"])

    if successful:
        new_daily = pd.concat(successful, ignore_index=True)
        successful_codes = new_daily["股票代码"].unique()

        old_daily = old_daily[
            ~old_daily["股票代码"].isin(successful_codes)
        ]
        merged = pd.concat([old_daily, new_daily], ignore_index=True)
        merged = clean_daily(merged)

        save(merged, "daily")
        save_daily_coverage(coverage)

        if refresh_quality_report():
            write_manifest()
        log(f"重试完成：成功 {len(successful)} 只")
    else:
        log("本次没有股票重试成功")

    save_failures(remaining_failed, "daily")