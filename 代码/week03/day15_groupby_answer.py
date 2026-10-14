# day15_groupby_answer.py ｜ 参考答案
# 先自己做，卡住 30 分钟以上再来看。

from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent
csv_path = BASE.parent / "week01" / "hs300_sample.csv"
df = pd.read_csv(csv_path, encoding="utf-8", dtype={"代码": str})

行业映射 = {
    "贵州茅台": "食品饮料", "五粮液": "食品饮料",
    "宁德时代": "电力设备", "隆基绿能": "电力设备",
    "比亚迪": "汽车",
    "招商银行": "银行", "平安银行": "银行",
    "中国平安": "非银金融", "中信证券": "非银金融", "东方财富": "非银金融",
    "紫金矿业": "有色金属",
    "恒瑞医药": "医药生物",
}
df["行业"] = df["名称"].map(行业映射)


# ---------- 题 1  按行业看平均 ----------
print("各行业平均（文本列被自动跳过）：")
print(df.groupby("行业").mean(numeric_only=True).round(2))
print()


# ---------- 题 2  agg ----------
print("市盈率：均值 / 最大 / 有效个数")
print(df.groupby("行业")["市盈率"].agg(["mean", "max", "count"]).round(2))

print("\n不同列用不同函数：")
print(df.groupby("行业").agg({
    "市盈率": "mean",
    "涨跌幅": ["mean", "std"],
    "成交额": "sum",
}).round(2))

print("\n自定义函数（组内极差）：")
print(df.groupby("行业")["市盈率"].agg(lambda s: s.max() - s.min()).round(2))
print()


# ---------- 题 3  分组后的三件事 ----------
print("每个行业几只：")
print(df.groupby("行业").size())

print("\n只看非银金融这一组：")
print(df.groupby("行业").get_group("非银金融")[["代码", "名称", "市盈率", "涨跌幅"]])

print("\n只留组内至少 2 行的行业：")
biger = df.groupby("行业").filter(lambda g: len(g) >= 2)
print(f"筛完剩 {len(biger)} 行，涉及行业：{sorted(biger['行业'].unique())}")
print()


# ---------- 题 4  分档 ----------
df["估值档"] = pd.cut(df["市盈率"], bins=[0, 15, 30, 100],
                      labels=["低估值", "中估值", "高估值"])
print("分档结果：")
print(df[["名称", "市盈率", "估值档"]])
print(f"\n有几只没分到档：{df['估值档'].isna().sum()} 只（市盈率缺失的那两只）")
print()


# ---------- 题 5  transform ----------
df["行业中位市盈率"] = df.groupby("行业")["市盈率"].transform("median")
df["相对行业溢价"] = (df["市盈率"] / df["行业中位市盈率"] - 1).round(3)
print("加回原表的两列：")
print(df[["名称", "行业", "市盈率", "行业中位市盈率", "相对行业溢价"]])
print()


# ---------- 主菜  分档汇总表 ----------
print("=== 分档汇总表 ===")
summary = df.groupby("估值档", observed=True)["涨跌幅"].agg(["count", "mean", "median"]).round(2)
summary.columns = ["只数", "平均涨跌幅", "中位涨跌幅"]
print(summary)

print("\n观察：低估值档平均涨跌幅 "
      f"{summary.loc['低估值', '平均涨跌幅']}%，"
      f"高估值档 {summary.loc['高估值', '平均涨跌幅']}%。")
print("样本只有 12 只股票，任何结论都不能当真——这一步练的是做法，不是结论。")
