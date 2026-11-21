"""下载沪深 300 的历史 PE/PB，并对齐月末信号日。"""

import time

import akshare as ak
import pandas as pd

from build_trade_calendar import build_monthly_calendar, load_daily
from config import OUTPUT_DIR, SOURCE_DATA_DIR

SLEEP_SECONDS = 0.2
START_DATE = "2025-01-01"
END_DATE = "2025-10-17"

def fetch_indicator(code, indicator, retries=3):
    """获取一个历史估值指标，失败时最多重试 3 次。"""
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            data = ak.stock_zh_valuation_baidu(
                symbol=code,
                indicator=indicator,
                period="近三年",
            )
            data["date"] = pd.to_datetime(data["date"])
            return data.rename(columns={"value": indicator})
        except Exception as exc:
            last_error = exc
            print(
                f"{code} {indicator} 第 {attempt} 次失败："
                f"{type(exc).__name__}: {exc}"
            )
            if attempt < retries:
                time.sleep(1)

    raise RuntimeError(str(last_error))

def fetch_stock_valuation(code, signal_dates):
    """获取一只股票并匹配月末信号日。"""
    pe = fetch_indicator(code, "市盈率(TTM)")
    pb = fetch_indicator(code, "市净率")

    valuation = pe.merge(
        pb,
        on="date",
        how="inner",
    )

    valuation = valuation[
        (valuation["date"] >= pd.Timestamp(START_DATE))
        & (valuation["date"] <= pd.Timestamp(END_DATE))
    ]

    sample = signal_dates.merge(
        valuation,
        left_on="signal_date",
        right_on="date",
        how="inner",
    )
    sample["股票代码"] = code

    return sample.drop(columns=["date"])

def fetch_all_valuation(codes):
    """批量下载历史估值并记录失败股票。"""
    daily = load_daily()
    calendar = build_monthly_calendar(daily)
    signal_dates = calendar[["month", "signal_date"]]

    frames = []
    failures = []
    total = len(codes)

    for i, code in enumerate(codes, start=1):
        try:
            sample = fetch_stock_valuation(code, signal_dates)
            if sample.empty:
                failures.append({
                    "代码": code,
                    "原因": "没有月末估值数据",
                })
            else:
                frames.append(sample)
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

    if not frames:
        return pd.DataFrame(), failures

    result = pd.concat(frames, ignore_index=True)
    result = result.sort_values(["month", "股票代码"])

    assert not result.duplicated(
        ["month", "股票代码"]
    ).any()

    return result.reset_index(drop=True), failures

def main():
    """下载全量历史估值并保存。"""
    constituents = pd.read_csv(
        SOURCE_DATA_DIR / "hs300_constituents.csv",
        dtype={"代码": str},
    )
    codes = constituents["代码"].tolist()

    print("股票数：", len(codes))

    valuation, failures = fetch_all_valuation(codes)

    output_path = OUTPUT_DIR / "historical_valuation.csv"
    failed_path = OUTPUT_DIR / "historical_valuation_failed.csv"

    valuation.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
    )
    pd.DataFrame(
        failures,
        columns=["代码", "原因"],
    ).to_csv(
        failed_path,
        index=False,
        encoding="utf-8-sig",
    )

    print("\n下载完成：")
    print("总行数：", len(valuation))
    print("股票数：", valuation["股票代码"].nunique())
    print("月份数：", valuation["month"].nunique())
    print("失败股票数：", len(failures))
    print("估值文件：", output_path)
    print("失败清单：", failed_path)


if __name__ == "__main__":
    main()