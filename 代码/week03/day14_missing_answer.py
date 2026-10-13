# day14_missing_answer.py ｜ 参考答案
# 先自己做，卡住 30 分钟以上再来看。

from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent
csv_path = BASE.parent / "week01" / "hs300_sample.csv"
df = pd.read_csv(csv_path, encoding="utf-8", dtype={"代码": str})


# ---------- 题 1  缺失体检 ----------
print("每列缺失个数：")
print(df.isna().sum())

print("\n每列缺失比例（%）：")
print((df.isna().mean() * 100).round(2))

print("\n哪几列有缺失：")
print(df.isna().any())
print()


# ---------- 题 2  定位缺失的行 ----------
print("市盈率缺失的行：")
print(df[df["市盈率"].isna()][["代码", "名称", "市盈率"]])

has_missing = df[df.isna().any(axis=1)]
print(f"\n任意一列缺失的行（共 {len(has_missing)} 行）：")
print(has_missing[["代码", "名称", "涨跌幅", "市盈率", "成交额"]])
print()


# ---------- 题 3  dropna ----------
print(f"原始行数：{len(df)}")
print(f"dropna() 之后：{len(df.dropna())} 行（任何一列缺就删）")
print(f"dropna(subset=['市盈率']) 之后：{len(df.dropna(subset=['市盈率']))} 行")
print(f"dropna(how='all') 之后：{len(df.dropna(how='all'))} 行")
print()


# ---------- 题 4  fillna ----------
col = df["市盈率"]
print("原始市盈率：")
print(list(col))
print(f"\n填 0：        {list(col.fillna(0))}")
print(f"填均值：      {list(col.fillna(col.mean()).round(2))}")
print(f"填中位数：    {list(col.fillna(col.median()).round(2))}")
print(f"用上一个值填：{list(col.ffill())}")
print(f"用下一个值填：{list(col.bfill())}")
print()


# ---------- 题 5  缺失不是 0 ----------
right = df["市盈率"].mean()
wrong = df["市盈率"].fillna(0).mean()
print(f"跳过缺失算均值（正确）：{right:.2f}")
print(f"填 0 之后算均值（错误）：{wrong:.2f}")
print(f"差了 {right - wrong:.2f} —— 凭空把整体估值拉低了")
print()


# ---------- 题 6  参考判断 ----------
print("参考判断：")
print("a) 停牌导致的涨跌幅缺失：可以当 0 收益处理，但要在报告里写明这是假设")
print("b) 亏损导致的市盈率缺失：不能填、也不能直接算均值；应单独标记为亏损")
print("c) 数据没采到：优先补采；补不了就整行排除，不要把空当成 0")
print()


# ---------- 主菜  缺失体检报告 ----------
def missing_report(df, only_missing=True):
    """返回一张缺失体检表：列名 / 缺失个数 / 缺失比例(%)。

    only_missing=True 时只看有缺失的列 —— 一眼看出哪列最脏。
    """
    report = pd.DataFrame({
        "列名": df.columns,
        "缺失个数": df.isna().sum().values,
        "缺失比例(%)": (df.isna().mean() * 100).round(2).values,
    })
    if only_missing:
        report = report[report["缺失个数"] > 0]
    return report.sort_values("缺失比例(%)", ascending=False).reset_index(drop=True)


print("=== 缺失体检报告（只看有缺失的列）===")
print(missing_report(df))

print("\n=== 全量列 ===")
print(missing_report(df, only_missing=False))
