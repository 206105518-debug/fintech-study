"""下载项目 A 需要的历史日线数据。"""

import time

import sys

from pathlib import Path

import pandas as pd

from config import BASE_DIR, OUTPUT_DIR, SOURCE_DATA_DIR

SLEEP_SECONDS = 0.3

# 复用 week04 的单只股票取数函数
sys.path.append(str(BASE_DIR.parent / "week04"))

from fetchers import fetch_daily


HISTORY_START = "20230101"
HISTORY_END = "20251017"


def load_constituents():
    """读取沪深 300 股票代码。"""
    return pd.read_csv(
        SOURCE_DATA_DIR / "hs300_constituents.csv",
        dtype={"代码": str},
    )

def fetch_all_history(codes):
    """批量下载历史日线，并记录失败股票。"""
    frames = []
    failures = []
    total = len(codes)

    for i, code in enumerate(codes, start=1):
        try:
            daily = fetch_daily(
                code,
                HISTORY_START,
                HISTORY_END,
            )

            if daily is None or daily.empty:
                failures.append({
                    "代码": code,
                    "原因": "接口返回空数据",
                })
            else:
                frames.append(daily)

        except Exception as exc:
            failures.append({
                "代码": code,
                "原因": str(exc),
            })

        if i % 20 == 0 or i == total:
            print(
                f"{i}/{total}，成功 {len(frames)}，"
                f"失败 {len(failures)}"
            )

        time.sleep(SLEEP_SECONDS)

    if not frames: #若一只都没成功（frames 空）→ 返回空 DataFrame + 失败清单
        return pd.DataFrame(), failures

    history = pd.concat(frames, ignore_index=True)
    history["股票代码"] = (
        history["股票代码"].astype(str).str.zfill(6)
    )
    history["日期"] = pd.to_datetime(history["日期"])
    history = history.sort_values(["股票代码", "日期"])
    history = history.drop_duplicates(
        ["股票代码", "日期"]
    )

    return history.reset_index(drop=True), failures


def save_results(history, failures):
    """保存历史日线、失败清单和覆盖统计。"""
    daily_path = OUTPUT_DIR / "historical_daily.csv"
    failed_path = OUTPUT_DIR / "historical_daily_failed.csv"
    summary_path = OUTPUT_DIR / "historical_daily_summary.csv"

    history.to_csv(
        daily_path,
        index=False,
        encoding="utf-8-sig",
    )

    failure_df = pd.DataFrame(
        failures,
        columns=["代码", "原因"],
    )
    failure_df.to_csv(
        failed_path,
        index=False,
        encoding="utf-8-sig",
    )

    summary = pd.DataFrame({
        "指标": [
            "开始日期",
            "结束日期",
            "总行数",
            "股票数",
            "成功股票数",
            "失败股票数",
        ],
        "值": [
            history["日期"].min().date(),
            history["日期"].max().date(),
            len(history),
            history["股票代码"].nunique(),
            history["股票代码"].nunique(),
            len(failures),
        ],
    })
    summary.to_csv(
        summary_path,
        index=False,
        encoding="utf-8-sig",
    )

    print("历史日线：", daily_path)
    print("失败清单：", failed_path)
    print("覆盖统计：", summary_path)


def main():
    """下载全部沪深 300 股票的历史日线。"""
    constituents = load_constituents()
    codes = constituents["代码"].tolist()

    print("股票总数：", len(codes))
    print("请求区间：", HISTORY_START, "到", HISTORY_END)

    history, failures = fetch_all_history(codes)

    if history.empty:
        print("全部股票下载失败")
        return

    save_results(history, failures)

    print("\n下载完成：")
    print("总行数：", len(history))
    print("股票数：", history["股票代码"].nunique())
    print("失败股票数：", len(failures))
    print(
        "日期范围：",
        history["日期"].min().date(),
        "到",
        history["日期"].max().date(),
    )


if __name__ == "__main__":
    main()