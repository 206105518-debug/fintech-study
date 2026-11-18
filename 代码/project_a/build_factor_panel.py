"""构造 12-1 动量面板并合并未来收益。"""

import pandas as pd

from build_monthly_returns import build_monthly_returns
from build_trade_calendar import build_monthly_calendar, load_daily
from config import OUTPUT_DIR


def build_momentum(daily):
    """使用完整历史月末价格计算标准 12-1 动量。"""
    history=daily.copy()
    history["month"]=history["日期"].dt.to_period("M")

    month_ends=(
        history.groupby("month")["日期"]
        .max()
        .reset_index(name="month_end_date")
    )

    month_end_prices=(
        month_ends.merge(
            history[["日期","股票代码","收盘"]],
            left_on="month_end_date",
            right_on="日期",
            how="inner",
        ).drop(columns=["日期"])
    )

    price_wide=month_end_prices.pivot(index="month", columns="股票代码", values="收盘")

    expected_months = pd.period_range(price_wide.index.min(), price_wide.index.max(), freq="M")
    assert price_wide.index.equals(expected_months)

    momentum_wide = price_wide.shift(1) / price_wide.shift(12) - 1

    return (
        momentum_wide
        .stack()                    # 宽表 → 长表
        .rename("momentum_12_1")    # 值列命名
        .reset_index()              # (month, 股票) 变回列
        .dropna(subset=["momentum_12_1"])  # 去 NaN（前 12 月算不出）
    )


def build_factor_panel():
    """返回同时具备有效动量和未来收益的观测。"""
    daily = load_daily()
    calendar = build_monthly_calendar(daily)
    momentum = build_momentum(daily)
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
    assert panel["momentum_12_1"].notna().all()
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

    output_path = OUTPUT_DIR / "momentum_12_1_panel.csv"
    panel.to_csv(output_path, index=False, encoding="utf-8-sig")
    print("已保存：", output_path)


if __name__ == "__main__":
    main()
