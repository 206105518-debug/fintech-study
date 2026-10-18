# day17_rewrite_csv_answer.py ｜ 参考答案

from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent
csv_path = BASE.parent / "week01" / "hs300_sample.csv"


# ---------- 题 1  读进来 ----------
df = pd.read_csv(csv_path, encoding="utf-8", dtype={"代码": str})
print(df)
print()


# ---------- 题 2  行数与列数 ----------
print(f"数据行数：{df.shape[0]}，列数：{df.shape[1]}")
print()


# ---------- 题 3  每列缺失 ----------
print("每列缺失个数：")
print(df.isna().sum())
print("\n每列缺失比例（%）：")
print((df.isna().mean() * 100).round(2))
print()


# ---------- 题 4  数值列均值 ----------
数值列 = df.select_dtypes(include="number").columns
print(f"自动识别出的数值列：{list(数值列)}")
print("\n数值列均值：")
print(df[数值列].mean().round(2))
print()


# ---------- 题 5  打印成表 ----------
print(f"{'列名':<10}{'缺失':>8}{'均值':>12}")
for col in df.columns:
    missing = df[col].isna().sum()
    if col in 数值列:
        print(f"{col:<10}{missing:>8}{df[col].mean():>12.2f}")
    else:
        print(f"{col:<10}{missing:>8}")
print()


# ---------- 主菜  封装成函数 ----------
def analyze_csv_pandas(path):
    """用 pandas 做 CSV 统计，返回结构：
    {"行数": int, "缺失": {列名: 个数}, "均值": {列名: 均值}}
    文件不存在时返回 None。
    """
    try:
        df = pd.read_csv(path, encoding="utf-8", dtype={"代码": str})
    except FileNotFoundError:
        print(f"读不到文件：{path}")
        return None

    numeric = df.select_dtypes(include="number")
    return {
        "行数": len(df),
        "缺失": df.isna().sum().to_dict(),
        "均值": numeric.mean().round(2).to_dict(),
    }


print("=== 和 day08 同结构的返回值 ===")
print(analyze_csv_pandas(csv_path))
print("\n=== 文件不存在时 ===")
print(analyze_csv_pandas("没有这个文件.csv"))

print("""
=== 两个版本对比 ===
手写版（week01/day08_csv_stats.py）：总行 279，去掉注释和空行后 109 行，17 个 for 循环
pandas 版（本文件）：总行 82，去掉注释和空行后 55 行，1 个 for 循环（只用来打印表）

差别不在行数，在于**你要操心的事情少了**：
  手写版要自己拆行、自己判断空字符串、自己维护数值列名单、自己处理类型转换；
  pandas 版这些都由库负责，你只负责描述「我要什么」。
""")
