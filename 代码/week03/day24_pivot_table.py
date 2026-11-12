from pathlib import Path

import pandas as pd

BASE = Path(__file__).parent
data_dir = BASE.parent / "week04" / "data"

daily = pd.read_csv(
    data_dir / "clean_daily.csv",
    dtype={"股票代码": str},
)
valuation = pd.read_csv(
    data_dir / "clean_valuation.csv",
    dtype={"代码": str},
)

daily["日期"] = pd.to_datetime(daily["日期"])
daily["月份"] = daily["日期"].dt.to_period("M")

industry = valuation[["代码", "行业"]]
merged = daily.merge(
    industry,
    left_on="股票代码",
    right_on="代码",
    how="left",
)
merged = merged.drop(columns=["代码"])

print("日线数据：", daily.shape)
print("估值数据：", valuation.shape)
print("合并后：", merged.shape)
print("行业缺失：", merged["行业"].isna().sum())
print("月份范围：", merged["月份"].min(), "到", merged["月份"].max())
print("行业数量：", merged["行业"].nunique())

turnover_pivot = merged.pivot_table(
    index="行业",
    columns="月份",
    values="换手率",
    aggfunc="mean",
)

print("\n行业 × 月份的平均换手率")
print("形状：", turnover_pivot.shape)
print("缺失单元格：", turnover_pivot.isna().sum().sum())
print(turnover_pivot.round(4).head())

stock_count_pivot = merged.pivot_table(
    index="行业",
    columns="月份",
    values="股票代码",
    aggfunc="nunique",
    fill_value=0,
    margins=True,
    margins_name="合计",
)

print("\n行业 × 月份的交易股票数")
print("形状：", stock_count_pivot.shape)
print(stock_count_pivot)

turnover_grouped = (
    merged.groupby(["行业", "月份"])["换手率"]
    .mean()
    .unstack()
)

print("\n使用 groupby + unstack 计算的平均换手率")
print(turnover_grouped.round(4).head())

same = turnover_pivot.round(10).equals(
    turnover_grouped.round(10)
)
print("\n两种结果是否一致：", same)