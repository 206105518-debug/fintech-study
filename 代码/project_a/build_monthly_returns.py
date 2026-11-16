"""根据信号日、建仓日和平仓日构造月度持有期收益。"""

import pandas as pd

from build_trade_calendar import build_monthly_calendar, load_daily
from config import OUTPUT_DIR


def build_monthly_returns(daily=None, calendar=None):
    """返回每只股票在每个完整持有期的收益。"""
    if daily is None:
        daily = load_daily()
    if calendar is None:
        calendar = build_monthly_calendar(daily)

    valid_calendar = calendar.dropna(subset=["entry_date", "exit_date"]).copy()

    entry_prices = daily[
        ["日期", "股票代码", "开盘"]
    ].rename(columns={
        "日期": "entry_date",
        "开盘": "entry_open",
    })

    exit_prices = daily[
        ["日期", "股票代码", "开盘"]
    ].rename(columns={
        "日期": "exit_date",
        "开盘": "exit_open",
    })

    entry = valid_calendar.merge(
        entry_prices,
        on="entry_date",
        how="inner",
    )

    exit_ = entry[
        ["month", "exit_date", "股票代码"]
    ].merge(
        exit_prices,
        on=["exit_date", "股票代码"],
        how="inner",
    )

    returns = entry.merge(
        exit_[["month", "股票代码", "exit_open"]],
        on=["month", "股票代码"],
        how="inner",
    )

    returns["future_return"] = (
        returns["exit_open"] / returns["entry_open"] - 1
    )

    assert not returns.duplicated(["month", "股票代码"]).any()
    assert returns["future_return"].notna().all()

    return returns.sort_values(["month", "股票代码"]).reset_index(drop=True)


def main():
    """运行收益构造并保存结果。"""
    returns = build_monthly_returns()

    print("总行数：", len(returns))
    print("月份数量：", returns["month"].nunique())
    print("股票数量：", returns["股票代码"].nunique())
    print("主键重复数：", returns.duplicated(["month", "股票代码"]).sum())

    print("\n每月记录数：")
    print(returns.groupby("month").size().to_string())

    print("\n收益范围：")
    print(returns["future_return"].describe())

    output_path = OUTPUT_DIR / "monthly_returns.csv"
    returns.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
    )
    print("\n已保存：", output_path)


if __name__ == "__main__":
    main()
