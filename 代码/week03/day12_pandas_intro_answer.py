# day12_pandas_intro_answer.py ｜ 参考答案
# 先自己做，卡住 30 分钟以上再来看。

from pathlib import Path
import pandas as pd


# ---------- 题 1  读进来 ----------
BASE = Path(__file__).parent
csv_path = BASE.parent / "week01" / "hs300_sample.csv"
df = pd.read_csv(csv_path, encoding="utf-8", dtype={"代码": str})
# dtype={"代码": str} 是关键：不写这一句，000858 会被读成 858，前导零丢掉。
# 只要一列是「编号」（股票代码、身份证号、订单号），都要这样指定成文本。
print(df)
print()


# ---------- 题 2  六个命令建立第一印象 ----------
print("前 5 行：")
print(df.head())

print(f"\n形状（行, 列）：{df.shape}")
print(f"列名：{list(df.columns)}")

print("\n每列类型：")
print(df.dtypes)

print("\ninfo：")
df.info()

print("\ndescribe：")
print(df.describe())
print()


# ---------- 题 3  选一列 vs 选多列 ----------
one_col = df["收盘价"]                        # Series：一列
multi_col = df[["代码", "名称", "收盘价"]]     # DataFrame：一张表

print("选一列（Series）：")
print(one_col.head())
print(f"类型是 {type(one_col).__name__}")

print("\n选多列（DataFrame）：")
print(multi_col.head())
print(f"类型是 {type(multi_col).__name__}")
print()


# ---------- 题 4  筛选与排序 ----------
up = df[df["涨跌幅"] > 0]
print(f"上涨的股票有 {len(up)} 只")

picked = df[(df["市盈率"] < 30) & (df["涨跌幅"] > 0)]
picked = picked.sort_values("收盘价", ascending=False)
print("\n市盈率低于 30 且上涨的股票，按收盘价排序：")
print(picked[["代码", "名称", "收盘价", "涨跌幅", "市盈率"]])

print("\n成交额最大的 3 只：")
print(df.nlargest(3, "成交额")[["代码", "名称", "成交额"]])
print()


# ---------- 题 5  存出去 ----------
picked.to_csv("picked.csv", index=False, encoding="utf-8-sig")
print("已保存 picked.csv")
print()


# ---------- 主菜  数据初诊报告 ----------
print("=== 数据初诊报告 ===")
print(f"行数 {df.shape[0]}，列数 {df.shape[1]}")

print("\n列名与类型：")
print(df.dtypes)

print("\n每列缺失个数：")
print(df.isna().sum())

print("\n数值列平均值：")
print(df.mean(numeric_only=True).round(2))

print(f"\n上涨的股票：{(df['涨跌幅'] > 0).sum()} 只")

# 对比 day08：同样的统计，那边用了八十多行，
# 还要自己处理缺失、自己区分哪些列是数值列。
