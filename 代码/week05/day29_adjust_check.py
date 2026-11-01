# day29_adjust_check.py ｜ 2026.11.1 周日：口径三件事，用数据自己证明
#
# 运行方式：
#   cd 金融科技学习/代码/week05
#   python3 day29_adjust_check.py
#
# 为什么做这个：
#   复权、单位、披露日，这三件事你答得含糊。光看答案是记不住的，
#   **用数据跑出一个反例，才会真的记住。**
#   今天三个实验，每个 20 分钟，跑完你就会讲得清清楚楚。

import sys
from pathlib import Path

import akshare as ak
import pandas as pd

BASE = Path(__file__).parent
data_dir = BASE.parent / "week04" / "data"
sys.path.append(str(BASE.parent / "week04"))
from fetchers import to_sina_symbol   # noqa: E402


# ==========================================================
# 实验 1  复权：同一只股票，三种价格，找出「除权日」
#   步骤：
#     1) 用 ak.stock_zh_a_daily 拉 600519 的 2024-2025 数据三次，
#        adjust 分别传 "qfq"、"hfq"、""（空字符串 = 不复权）
#     2) 每份只保留 date 和 close，按 date 合并成一张表
#     3) 分别算三份的日收益率（pct_change）
#     4) 找「不复权收益率」和「前复权收益率」差得最多的几天
#   你会看到：除权日那天，不复权显示 -X%，前复权接近 0 —— 那就是分红送股造成的假跌。
#   动手：打印差值最大的 5 天，以及那几天三种收盘价
# ==========================================================

# TODO 实验 1
前复权=ak.stock_zh_a_daily(symbol="sh600519", start_date="20240101", end_date="20251231", adjust="qfq")
后复权=ak.stock_zh_a_daily(symbol="sh600519", start_date="20240101", end_date="20251231", adjust="hfq")
不复权=ak.stock_zh_a_daily(symbol="sh600519", start_date="20240101", end_date="20251231", adjust="")

q = 前复权[["date", "close"]].rename(columns={"close": "前复权"})
h = 后复权[["date", "close"]].rename(columns={"close": "后复权"})
r = 不复权[["date", "close"]].rename(columns={"close": "不复权"})

合并=q.merge(h, on="date", how="inner").merge(r, on="date", how="inner")
合并["date"]=pd.to_datetime(合并["date"])
合并=合并.sort_values("date").reset_index(drop=True)

合并["ret_前"] = 合并["前复权"].pct_change()
合并["ret_后"] = 合并["后复权"].pct_change()
合并["ret_不"] = 合并["不复权"].pct_change()

合并["差值"]=(合并["ret_不"]-合并["ret_前"] ).abs() #.abs()取绝对值

最大=合并.nlargest(5,"差值")
print(最大[["date", "不复权", "前复权", "后复权", "ret_不", "ret_前", "差值"]].round(4).to_string(index=False))


# ==========================================================
# 实验 2  单位：成交量到底是「股」还是「手」
#   已知：换手率 = 成交量 ÷ 流通股本（新浪的 turnover 与 outstanding_share 同源）
#   步骤：
#     1) 拉一份 qfq 数据（已经包含 volume、outstanding_share、turnover）
#     2) 自己算：volume / outstanding_share
#     3) 和 turnover 对比
#   如果两者接近 → volume 的单位是「股」；
#   如果差 100 倍 → 是「手」。
#   动手：打印前 5 行的「自己算的换手率」和「接口给的换手率」
# ==========================================================

# TODO 实验 2
one=ak.stock_zh_a_daily(symbol="sh600519", start_date="20240101", end_date="20251231", adjust="qfq")
one["自己算的换手率"]=one["volume"]/one["outstanding_share"]
print("=== 实验 2：成交量单位 ===")
print(one[["date", "volume", "outstanding_share", "自己算的换手率", "turnover"]].head(5).to_string(index=False))
print("两者接近 → volume 单位是「股」\n")

# ==========================================================
# 实验 3  披露日：公告日期到底晚了多久
#   用本地 data/financial_all.csv（已经有了），不需要联网。
#   步骤：
#     1) 读 financial_all.csv
#     2) 公告日期是 8 位字符串，转成日期
#     3) 算「公告日期 - 报告期」的天数
#     4) 看这列的描述统计：中位数多少天？最大多少天？
#   合规的年报应该 ≤ 120 天（4/30 前）。
#   如果中位数是 300 多天，就证明了「历史公告日期被污染」。
#   动手：打印 describe()，再按报告年份分组看中位数
# ==========================================================

# TODO 实验 3
fin=pd.read_csv( data_dir/"financial_all.csv", encoding="utf-8", dtype={"代码":str})
fin["公告日期"]=pd.to_datetime(fin["公告日期"], format="%Y%m%d")
fin["报告期"]=pd.to_datetime(fin["报告期"])
fin["滞后天数"] = (fin["公告日期"] - fin["报告期"]).dt.days

print("=== 实验 3：公告日期滞后天数 ===")
print(fin["滞后天数"].describe().round(1).to_string())
print()


# ==========================================================
# 收尾
#   1) 三个实验跑完，用一句话分别写下结论
#   2) 把结论补进 规划/易错点清单.md
#   3) 提交推送
# ==========================================================
