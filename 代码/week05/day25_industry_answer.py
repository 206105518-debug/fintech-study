# day25_industry_answer.py ｜ 参考答案

import time
from pathlib import Path

import akshare as ak
import pandas as pd

BASE = Path(__file__).parent
data_dir = BASE.parent / "week04" / "data"


# ---------- 题 1  一级行业列表 ----------
一级 = ak.sw_index_first_info()
print(f"一级行业 {len(一级)} 个")
print(一级[["行业代码", "行业名称", "成份个数"]].head())
print()


# ---------- 题 2  拉成分股 ----------
行业映射 = []
失败行业 = []

for i, (_, row) in enumerate(一级.iterrows(), start=1):
    行业代码 = row["行业代码"].split(".")[0]
    行业名称 = row["行业名称"]
    try:
        cons = ak.index_component_sw(symbol=行业代码)
        for _, c in cons.iterrows():
            行业映射.append({
                "代码": str(c["证券代码"]).zfill(6),
                "行业": 行业名称,
            })
        print(f"{i}/{len(一级)} {行业名称} {len(cons)} 只")
    except Exception as e:
        失败行业.append({"行业": 行业名称, "原因": f"{type(e).__name__}: {e}"})
        print(f"{i}/{len(一级)} {行业名称} 失败")
    time.sleep(0.3)

行业表 = pd.DataFrame(行业映射)
print(f"\n共 {len(行业表)} 行，{行业表['代码'].nunique()} 个不重复代码")
print()


# ---------- 题 3  检查 ----------
重复 = 行业表.groupby("代码").size()
重复 = 重复[重复 > 1]
print(f"属于多个行业的代码：{len(重复)} 个")
if len(重复):
    print(行业表[行业表["代码"].isin(重复.index)].sort_values("代码").head(10))

print("\n行业分布（前 10）：")
print(行业表["行业"].value_counts().head(10))
print()


# ---------- 题 4  合并进名单 ----------
名单 = pd.read_csv(data_dir / "clean_constituents.csv", dtype={"代码": str})
合并 = pd.merge(名单, 行业表.drop_duplicates("代码"), on="代码", how="left")
覆盖 = 合并["行业"].notna().sum()
print(f"名单 {len(合并)} 只，匹配到行业 {覆盖} 只，覆盖率 {覆盖 / len(合并) * 100:.2f}%")

缺的 = 合并[合并["行业"].isna()]
if len(缺的):
    print("没匹配上的：")
    print(缺的[["代码", "名称", "交易所"]])
print()


# ---------- 题 5  存盘 ----------
行业表.drop_duplicates("代码").to_csv(
    data_dir / "industry_map.csv", index=False, encoding="utf-8-sig")
合并.to_csv(data_dir / "clean_constituents.csv", index=False, encoding="utf-8-sig")
print("已保存 industry_map.csv 与含行业的 clean_constituents.csv")
print()


# ---------- 主菜  fetch_industry_map ----------
def fetch_industry_map(level="first"):
    """拉申万行业映射，返回 代码 / 行业。"""
    base = ak.sw_index_first_info() if level == "first" else ak.sw_index_second_info()
    rows, failed = [], []
    for _, row in base.iterrows():
        code = row["行业代码"].split(".")[0]
        try:
            cons = ak.index_component_sw(symbol=code)
            for _, c in cons.iterrows():
                rows.append({"代码": str(c["证券代码"]).zfill(6), "行业": row["行业名称"]})
        except Exception as e:
            failed.append({"行业": row["行业名称"], "原因": str(e)})
        time.sleep(0.3)
    df = pd.DataFrame(rows).drop_duplicates("代码")
    print(f"{level}：{len(df)} 只股票、{df['行业'].nunique()} 个行业、失败 {len(failed)} 个行业")
    return df


映射 = fetch_industry_map("first")
print(映射["行业"].value_counts().head(10))
