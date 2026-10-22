# day22_valuation_answer.py ｜ 按题目顺序的参考答案
#
# 用法：做到第几题就看第几题，看完关掉自己敲。
# 不要整段复制运行——那样练不到手。

import time
from pathlib import Path

import akshare as ak
import pandas as pd

BASE = Path(__file__).parent
data_dir = BASE / "data"

INDICATORS = {
    "总市值": "总市值",
    "市盈率(TTM)": "市盈率TTM",
    "市净率": "市净率",
}


# ==========================================================
# 题 1  取 10 只股票
#   从昨天批量拉的数据里，取不重复的前 10 个代码。
# ==========================================================

日线 = pd.read_csv(data_dir / "daily_batch.csv", dtype={"股票代码": str})
codes = 日线["股票代码"].unique()[:10].tolist()
print(codes)


# ==========================================================
# 题 2  单只股票：一次拿三个指标
#   要点：
#     1) 先按 date 排序，再取最后一行——不要假设接口返回是正序
#     2) 三个指标拼成一个字典
#     3) 每个指标之间 sleep，别连着猛发
# ==========================================================

row = {"代码": "600519"}
for ind, col in INDICATORS.items():
    d = ak.stock_zh_valuation_baidu(
        symbol="600519", indicator=ind, period="近一年"
    )
    d = d.sort_values("date")
    row[col] = float(d["value"].iloc[-1])
    time.sleep(0.2)

print(row)
# 自查：总市值约 16482（亿元）、市盈率TTM 约 20.24、市净率 约 6.56


# ==========================================================
# 题 3  循环 10 只，收集结果
#   把题 2 那段搬进循环；每只包 try/except，
#   失败的记进「失败清单」，成功的 append 进列表。
# ==========================================================

估值列表 = []
失败 = []

for i, code in enumerate(codes, start=1):
    try:
        row = {"代码": code}
        for ind, col in INDICATORS.items():
            d = ak.stock_zh_valuation_baidu(
                symbol=code, indicator=ind, period="近一年"
            )
            d = d.sort_values("date")
            row[col] = float(d["value"].iloc[-1])
            time.sleep(0.2)
        估值列表.append(row)
        print(f"{i}/{len(codes)} {code} 成功")
    except Exception as e:
        失败.append({"代码": code, "原因": f"{type(e).__name__}: {e}"})
        print(f"{i}/{len(codes)} {code} 失败")


# ==========================================================
# 题 4  合并与覆盖率
#   估值表转 DataFrame，再和名单 merge，以名单为准。
# ==========================================================

估值表 = pd.DataFrame(估值列表)
名单 = pd.read_csv(data_dir / "hs300_constituents.csv", dtype={"代码": str})

合并 = pd.merge(名单[名单["代码"].isin(codes)], 估值表, on="代码", how="left")
覆盖 = 合并["总市值"].notna().sum()

print(f"名单 {len(合并)} 只，拿到总市值 {覆盖} 只，"
      f"覆盖率 {覆盖 / len(合并) * 100:.1f}%")
print(合并[["代码", "名称", "总市值", "市盈率TTM", "市净率"]])


# ==========================================================
# 题 5  存盘
# ==========================================================

out_path = data_dir / "valuation_10.csv"
合并.to_csv(out_path, index=False, encoding="utf-8-sig")

回读 = pd.read_csv(out_path, dtype={"代码": str})
print(f"已保存 {out_path}，读回 {回读.shape}")


# ==========================================================
# 主菜  封装
#   把题 2 的单只逻辑包成 fetch_valuation(code)，
#   把题 3 的循环包成 enrich_valuation(codes)。
#   注意：单个指标失败设 None，三个全失败才返回 None。
# ==========================================================

def fetch_valuation(code):
    row = {"代码": code}
    ok = 0
    for ind, col in INDICATORS.items():
        try:
            d = ak.stock_zh_valuation_baidu(
                symbol=code, indicator=ind, period="近一年"
            )
            d = d.sort_values("date")
            row[col] = float(d["value"].iloc[-1])
            ok += 1
        except Exception:
            row[col] = None
        time.sleep(0.2)
    return row if ok > 0 else None


def enrich_valuation(codes, sleep_sec=0.2):
    rows, failed = [], []
    for i, code in enumerate(codes, start=1):
        v = fetch_valuation(code)
        if v is None:
            failed.append({"代码": code, "原因": "三个指标均失败"})
            print(f"{i}/{len(codes)} {code} 失败")
        else:
            rows.append(v)
            print(f"{i}/{len(codes)} {code} 成功")
        time.sleep(sleep_sec)
    return pd.DataFrame(rows), failed
