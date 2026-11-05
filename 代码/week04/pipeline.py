"""沪深300数据管道入口。

运行方式：
    cd 代码/week04
    python3 pipeline.py

完整运行、强制刷新和失败重试分别由 main() 与 parse_args() 控制。
"""

import argparse
import time

from pipeline_config import CONFIG, data_dir
from pipeline_daily import fetch_daily_all
from pipeline_market import (
    fetch_valuation_all,
    load_constituents,
    load_financial,
    load_industry,
)
from pipeline_quality import quality_report
from pipeline_retry import retry_failed_daily
from pipeline_state import (
    can_skip,
    log,
    save,
    save_failures,
    write_manifest,
)
from pipeline_transform import clean_daily, merge_valuation


def parse_args():
    """解析 --force 和 --retry-failed 命令行参数。"""
    parser = argparse.ArgumentParser(description="沪深300数据管道")
    parser.add_argument(
        "--force",
        action="store_true",
        help="忽略已有结果，强制重新拉取",
    )
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="只重试 failed_daily.csv 中失败的股票",
    )
    return parser.parse_args()


# 主流程：按顺序执行取数、清洗、落盘和质量检查
def main(force=False, retry_failed=False):
    """执行完整数据管道，或只重试失败股票。"""
    if retry_failed:
        retry_failed_daily()
        return

    if not force and can_skip():
        log("参数一致且结果齐全，跳过本次运行")
        log("本次运行完成")
        return

    log("=" * 60)
    log(
        f"参数：start={CONFIG['start']} "
        f"end={CONFIG['end']} "
        f"max_stocks={CONFIG['max_stocks']} "
        f"force={force}"
    )

    log("加载名单")
    constituents = load_constituents()
    if constituents is None:
        log("名单加载失败，停止运行")
        return

    log("补充行业")
    constituents = load_industry(constituents)
    constituents.to_csv(
        data_dir / "constituents_with_industry.csv",
        index=False,
        encoding="utf-8-sig",
    )

    if CONFIG["max_stocks"]:
        constituents = constituents.head(CONFIG["max_stocks"])
    log(f"名单共 {len(constituents)} 只")

    log("拉取日线")
    started_at = time.time()
    daily, failed_daily = fetch_daily_all(
        constituents["代码"].tolist(),
        force=force,
    )
    save_failures(failed_daily, "daily")

    if daily.empty:
        log("日线全部失败，停止运行")
        return

    log(
        f"日线 {len(daily)} 行，失败 {len(failed_daily)} 只，"
        f"耗时 {time.time() - started_at:.1f} 秒"
    )

    log("拉取估值")
    started_at = time.time()
    valuation, failed_valuation = fetch_valuation_all(
        constituents["代码"].tolist()
    )
    save_failures(failed_valuation, "valuation")
    log(
        f"估值成功 {len(valuation)} 只，失败 {len(failed_valuation)} 只，"
        f"耗时 {time.time() - started_at:.1f} 秒"
    )

    log("合并名单与估值")
    valuation_table = merge_valuation(constituents, valuation)

    log("清洗日线")
    daily = clean_daily(daily)

    log("保存日线与估值")
    save(daily, "daily")
    save(valuation_table, "valuation")

    log("读取财务")
    financial = load_financial()

    log("生成质量报告")
    tables = {
        "名单": constituents,
        "日线": daily,
        "估值": valuation_table,
    }
    if financial is not None:
        save(financial, "financial")
        tables["财务"] = financial

    report = quality_report(tables)
    report.to_csv(
        data_dir / "data_quality_report.csv",
        index=False,
        encoding="utf-8-sig",
    )
    print(report.to_string(index=False))

    write_manifest()
    log("本次运行完成")


if __name__ == "__main__":
    args = parse_args()
    main(force=args.force, retry_failed=args.retry_failed)