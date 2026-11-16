"""构造 6-1 动量面板并合并未来收益。"""

import pandas as pd

from build_monthly_returns import build_monthly_returns
from build_trade_calendar import build_monthly_calendar, load_daily
from config import OUTPUT_DIR


def build_momentum(daily, calendar):
    """使用完整月末收盘价计算 6-1 动量。"""
    month_end_prices = (
        calendar[["month", "signal_date"]]
        .merge(
            daily[["日期", "股票代码", "收盘"]],
            left_on="signal_date",
            right_on="日期",
            how="inner",
        )
        .drop(columns=["日期"])
    )

    price_wide = month_end_prices.pivot(
        index="month",
        columns="股票代码",
        values="收盘",
    )

    expected_months = pd.period_range(
        price_wide.index.min(),
        price_wide.index.max(),
        freq="M",
    )
    assert price_wide.index.equals(expected_months)

    momentum_wide = price_wide.shift(1) / price_wide.shift(6) - 1
    return (
        momentum_wide.stack()
        .rename("momentum_6_1")
        .reset_index()
        .dropna(subset=["momentum_6_1"])
    )


def build_factor_panel():
    """返回同时具备有效动量和未来收益的观测。"""
    daily = load_daily()
    calendar = build_monthly_calendar(daily)
    momentum = build_momentum(daily, calendar)
    returns = build_monthly_returns(daily, calendar)

    panel = momentum.merge(
        returns[
            [
                "month",
                "股票代码",
                "signal_date",
                "entry_date",
                "exit_date",
                "future_return",
            ]
        ],
        on=["month", "股票代码"],
        how="inner",
    )

    assert not panel.duplicated(["month", "股票代码"]).any()
    assert panel["momentum_6_1"].notna().all()
    assert panel["future_return"].notna().all()
    assert (panel["signal_date"] < panel["entry_date"]).all()
    assert (panel["entry_date"] < panel["exit_date"]).all()
    return panel.sort_values(["month", "股票代码"]).reset_index(drop=True)


def main():
    """构造、校验并保存动量面板。"""
    panel = build_factor_panel()

    print("因子面板：", panel.shape)
    print("月份数：", panel["month"].nunique())
    print("主键重复数：", panel.duplicated(["month", "股票代码"]).sum())
    print(
        panel.groupby("month").size().rename("记录数").to_string()
    )

    output_path = OUTPUT_DIR / "momentum_panel.csv"
    panel.to_csv(output_path, index=False, encoding="utf-8-sig")
    print("已保存：", output_path)


if __name__ == "__main__":
    main()
