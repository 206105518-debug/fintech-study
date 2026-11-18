"""构建每月信号日、建仓日和平仓日。"""

import pandas as pd

from config import (
    HISTORICAL_DAILY_PATH,
    SIGNAL_END,
    SIGNAL_START,
)


def load_daily():
    """读取基础日线数据并解析日期。"""
    daily = pd.read_csv(
        HISTORICAL_DAILY_PATH,
        dtype={"股票代码": str},
    )
    daily["日期"] = pd.to_datetime(daily["日期"])
    return daily


def build_monthly_calendar(daily):
    """返回每个完整月份的月末信号、建仓日和平仓日。"""
    data = daily.copy()
    data["日期"] = pd.to_datetime(data["日期"])

    trading_days = pd.Series(
        data["日期"].drop_duplicates().sort_values(),
        name="trade_date",
    )

    calendar_df = pd.DataFrame({"trade_date": trading_days})
    calendar_df["month"] = calendar_df["trade_date"].dt.to_period("M")

    monthly_ends = (
        calendar_df.groupby("month")["trade_date"]
        .max()
        .reset_index(name="signal_date")
    )

    monthly_ends = monthly_ends[
        (monthly_ends["signal_date"] >= pd.Timestamp(SIGNAL_START))
        & (monthly_ends["signal_date"] <= pd.Timestamp(SIGNAL_END))
    ].copy()

    # 当前数据截止 2025-10-17，因此 10 月不是完整月份。
    last_signal = monthly_ends.iloc[-1]["signal_date"]
    month_calendar_end = last_signal + pd.offsets.MonthEnd(0)
    if (month_calendar_end - last_signal).days > 5:
        monthly_ends = monthly_ends.iloc[:-1].copy()

    next_trading_day = dict(
        zip(trading_days.iloc[:-1], trading_days.iloc[1:])
    )
    monthly_ends["entry_date"] = monthly_ends["signal_date"].map(
        next_trading_day
    )
    monthly_ends["exit_date"] = monthly_ends["entry_date"].shift(-1)

    assert monthly_ends["month"].is_unique
    assert monthly_ends["signal_date"].is_unique
    assert monthly_ends["entry_date"].notna().all()

    return monthly_ends


def main():
    """打印月度交易日历。"""
    daily = load_daily()
    monthly_ends = build_monthly_calendar(daily)

    print(monthly_ends.to_string(index=False))

    valid_returns = monthly_ends.dropna(subset=["exit_date"])
    print("\n可计算完整持有期收益的月份：")
    print(
        valid_returns[
            ["month", "signal_date", "entry_date", "exit_date"]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
