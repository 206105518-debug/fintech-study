"""用少量股票验证历史 PE/PB 的时间对齐。"""

import pandas as pd

from build_trade_calendar import build_monthly_calendar, load_daily

import akshare as ak

TEST_CODES = ["600519", "000001", "002353"]
START_DATE = "2025-01-01"
END_DATE = "2025-10-17"

def fetch_indicator(code, indicator):
    """获取一只股票的一个历史估值指标。"""
    data = ak.stock_zh_valuation_baidu(
        symbol=code, indicator=indicator, period="近三年")
    data["date"] = pd.to_datetime(data["date"])
    return data.rename(columns={"value": indicator})

def main():
    """输出测试股票在月末信号日的 PE 和 PB。"""
    daily = load_daily()
    calendar = build_monthly_calendar(daily)
    signal_dates = calendar[["month", "signal_date"]]

    panels = []

    for code in TEST_CODES:
        pe = fetch_indicator(code, "市盈率(TTM)")
        pb = fetch_indicator(code, "市净率")

        valuation = pe.merge(
            pb,
            on="date",
            how="inner",
        )
        valuation["股票代码"] = code

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

        print(f"\n===== {code} =====")
        print("估值历史行数：", len(valuation))
        print("月末命中数：", len(sample))
        print(sample.to_string(index=False))

        panels.append(sample)

    result = pd.concat(panels, ignore_index=True)
    print("\n合并后：", result.shape)
    print("主键重复数：", result.duplicated(
        ["month", "股票代码"]
    ).sum())


if __name__ == "__main__":
    main()