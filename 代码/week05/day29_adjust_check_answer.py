# day29_adjust_check_answer.py ｜ 参考答案

import sys
from pathlib import Path

import akshare as ak
import pandas as pd

BASE = Path(__file__).parent
data_dir = BASE.parent / "week04" / "data"
sys.path.append(str(BASE.parent / "week04"))
from fetchers import to_sina_symbol   # noqa: E402


# ---------- 实验 1  复权 ----------
frames = {}
for adj, label in [("qfq", "前复权"), ("hfq", "后复权"), ("", "不复权")]:
    d = ak.stock_zh_a_daily(
        symbol="sh600519", start_date="20240101", end_date="20251231", adjust=adj)
    d = d[["date", "close"]].rename(columns={"close": label})
    frames[label] = d

df = frames["前复权"].merge(frames["后复权"], on="date").merge(frames["不复权"], on="date")
df["ret_不复权"] = df["不复权"].pct_change()
df["ret_前复权"] = df["前复权"].pct_change()
df["差异"] = (df["ret_不复权"] - df["ret_前复权"]).abs()

print("=== 实验 1：复权差异最大的 5 天 ===")
print(df.nlargest(5, "差异")[["date", "不复权", "前复权", "ret_不复权", "ret_前复权", "差异"]].round(4).to_string(index=False))
print()


# ---------- 实验 2  单位 ----------
one = ak.stock_zh_a_daily(
    symbol="sh600519", start_date="20250101", end_date="20250228", adjust="qfq")
one["自己算的换手率"] = one["volume"] / one["outstanding_share"]
print("=== 实验 2：成交量单位 ===")
print(one[["date", "volume", "outstanding_share", "自己算的换手率", "turnover"]].head(5).to_string(index=False))
print("两者接近 → volume 单位是「股」\n")


# ---------- 实验 3  披露日 ----------
fin = pd.read_csv(data_dir / "financial_all.csv", dtype={"股票代码": str})
fin["公告日"] = pd.to_datetime(fin["公告日期"], format="%Y%m%d")
fin["滞后天数"] = (fin["公告日"] - fin["报告期"].pipe(pd.to_datetime)).dt.days

print("=== 实验 3：公告日期滞后天数 ===")
print(fin["滞后天数"].describe().round(1).to_string())
print()
by_year = fin.assign(年份=pd.to_datetime(fin["报告期"]).dt.year).groupby("年份")["滞后天数"].median()
print("按报告年份看中位数：")
print(by_year.to_string())
print("\n合规年报应 ≤ 120 天；中位数远超 → 历史公告日期被污染")
