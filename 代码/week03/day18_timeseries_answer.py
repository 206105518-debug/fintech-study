# day18_timeseries_answer.py ｜ 参考答案
# 先自己做，卡住 30 分钟以上再来看。

import numpy as np
import pandas as pd

np.random.seed(42)
dates = pd.date_range("2025-01-01", periods=250, freq="B")
daily_ret = np.random.normal(0.0003, 0.015, 250)
price = 100 * (1 + daily_ret).cumprod()
df = pd.DataFrame({"日期": dates, "收盘价": price})


# ---------- 题 1  日期类型 ----------
print("原始类型：", df["日期"].dtype)
as_str = df["日期"].astype(str)
print("转成字符串：", as_str.dtype, "示例：", as_str.iloc[0])
back = pd.to_datetime(as_str)
print("再转回来：", back.dtype)
print()


# ---------- 题 2  日期索引 ----------
df = df.set_index("日期")
print("三月行数：", len(df.loc["2025-03"]))
print(df.loc["2025-03-03":"2025-03-07"][["收盘价"]].round(2))
print()


# ---------- 题 3  按月聚合 ----------
monthly = df.resample("ME")["收盘价"].mean().round(2)
print("月度平均收盘价：")
print(monthly)
print()


# ---------- 题 4  20 日滚动均线 ----------
df["20日均线"] = df["收盘价"].rolling(20).mean()
print("前 22 行（前 19 个均线是 NaN）：")
print(df[["收盘价", "20日均线"]].head(22).round(2))
print()


# ---------- 题 5  日收益率 ----------
df["日收益率"] = df["收盘价"].pct_change()
print("日收益率第一行：", df["日收益率"].iloc[0])
print(f"最大单日涨幅：{df['日收益率'].max() * 100:.2f}%")
print(f"最大单日跌幅：{df['日收益率'].min() * 100:.2f}%")
print()


# ---------- 主菜  三张脸 ----------
print("=== 1) 月度平均（按时间聚合）===")
print(monthly.head(3))

print("\n=== 2) 20 日滚动均线（按时间滚动，最后 3 个）===")
print(df["20日均线"].dropna().tail(3).round(2))

print("\n=== 3) 日收益率的均值与标准差（相邻两期相减）===")
print(f"日均收益率：{df['日收益率'].mean() * 100:.3f}%")
print(f"日波动率：  {df['日收益率'].std() * 100:.3f}%")

print("""
三类操作的区别：
  resample    按时间聚合：把一个月的行压成一行（降维）
  rolling     按时间滚动：每行都算前 N 天的统计量（行数不变）
  pct_change  相邻两期相减：把价格变成收益率（行数不变，首行 NaN）
这三类覆盖了时间序列 90% 的日常需求。
""")
