# day23_clean_answer.py ｜ 参考答案
# 全部在本地文件上跑，不需要联网。

from pathlib import Path

import pandas as pd

BASE = Path(__file__).parent
data_dir = BASE / "data"

KEYS = {"名单": ["代码"], "日线": ["股票代码", "日期"], "估值": ["代码"]}


# ---------- 题 1  读进来 ----------
名单 = pd.read_csv(data_dir / "hs300_constituents.csv", dtype={"代码": str})
日线 = pd.read_csv(data_dir / "daily_batch.csv", dtype={"股票代码": str})
估值 = pd.read_csv(data_dir / "valuation_10.csv", dtype={"代码": str})

for 名, 表 in [("名单", 名单), ("日线", 日线), ("估值", 估值)]:
    print(f"[{名}] shape={表.shape}")
    print(f"  列：{list(表.columns)}")
    print(f"  类型：{dict(表.dtypes.astype(str))}")
print()


# ---------- 题 2  统一字段 ----------
名单["代码"] = 名单["代码"].astype(str).str.zfill(6)
日线["股票代码"] = 日线["股票代码"].astype(str).str.zfill(6)
日线["日期"] = pd.to_datetime(日线["日期"])
估值["代码"] = 估值["代码"].astype(str).str.zfill(6)

for col in ["总市值", "市盈率TTM", "市净率"]:
    估值[col] = pd.to_numeric(估值[col], errors="coerce")
for col in ["开盘", "最高", "最低", "收盘", "成交量", "成交额", "换手率"]:
    日线[col] = pd.to_numeric(日线[col], errors="coerce")

print("统一之后：")
print("  名单代码类型：", 名单["代码"].dtype)
print("  日线日期类型：", 日线["日期"].dtype)
print("  估值数值列：", [c for c in ["总市值", "市盈率TTM", "市净率"]])
print()


# ---------- 题 3  查重 ----------
for 名, 表 in [("名单", 名单), ("日线", 日线), ("估值", 估值)]:
    重复 = 表.duplicated(subset=KEYS[名]).sum()
    print(f"[{名}] 主键重复：{重复}")
print()


# ---------- 题 4  缺失体检 ----------
for 名, 表 in [("名单", 名单), ("日线", 日线), ("估值", 估值)]:
    缺失 = 表.isna().sum()
    有缺失 = 缺失[缺失 > 0]
    print(f"[{名}] 有缺失的列：")
    print("  ", 有缺失.to_dict() if len(有缺失) else "无")
print()


# ---------- 题 5  跨表一致性 ----------
日线只数 = 日线["股票代码"].nunique()
估值只数 = 估值["代码"].nunique()
print(f"名单 {len(名单)} 只；日线覆盖 {日线只数} 只（{日线只数/len(名单)*100:.1f}%）；"
      f"估值覆盖 {估值只数} 只（{估值只数/len(名单)*100:.1f}%）")
print(f"日线日期范围：{日线['日期'].min().date()} ~ {日线['日期'].max().date()}")
print("每只行数：")
print(日线.groupby("股票代码").size().to_string())
print(f"成交量为 0 的天数：{(日线['成交量'] == 0).sum()}")
print()


# ---------- 主菜  clean_all ----------
def clean_all():
    """读三张原始表、清洗、落盘，并返回质量报告。"""
    名单 = pd.read_csv(data_dir / "hs300_constituents.csv", dtype={"代码": str})
    日线 = pd.read_csv(data_dir / "daily_batch.csv", dtype={"股票代码": str})
    估值 = pd.read_csv(data_dir / "valuation_10.csv", dtype={"代码": str})

    名单["代码"] = 名单["代码"].astype(str).str.zfill(6)
    日线["股票代码"] = 日线["股票代码"].astype(str).str.zfill(6)
    日线["日期"] = pd.to_datetime(日线["日期"])
    估值["代码"] = 估值["代码"].astype(str).str.zfill(6)
    for c in ["总市值", "市盈率TTM", "市净率"]:
        估值[c] = pd.to_numeric(估值[c], errors="coerce")
    for c in ["开盘", "最高", "最低", "收盘", "成交量", "成交额", "换手率"]:
        日线[c] = pd.to_numeric(日线[c], errors="coerce")

    名单.to_csv(data_dir / "clean_constituents.csv", index=False, encoding="utf-8-sig")
    日线.to_csv(data_dir / "clean_daily.csv", index=False, encoding="utf-8-sig")
    估值.to_csv(data_dir / "clean_valuation.csv", index=False, encoding="utf-8-sig")

    报告 = []
    for 名, 表 in [("名单", 名单), ("日线", 日线), ("估值", 估值)]:
        缺失列数 = int((表.isna().sum() > 0).sum())
        报告.append({
            "表名": 名,
            "行数": len(表),
            "列数": 表.shape[1],
            "主键重复数": int(表.duplicated(subset=KEYS[名]).sum()),
            "有缺失的列数": 缺失列数,
        })
    return pd.DataFrame(报告)


报告 = clean_all()
报告.to_csv(data_dir / "data_quality_report.csv", index=False, encoding="utf-8-sig")
print("=== 数据质量报告 ===")
print(报告.to_string(index=False))
