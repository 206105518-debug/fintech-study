# day21_batch_fetch_answer.py ｜ 参考答案

import time
from pathlib import Path

import pandas as pd

from fetchers import fetch_daily

BASE = Path(__file__).parent
data_dir = BASE / "data"
START, END = "20250101", "20251017"


# ---------- 题 1  取前 10 只 ----------
名单 = pd.read_csv(data_dir / "hs300_constituents.csv", dtype={"代码": str})
前10 = 名单.head(10)
print(前10[["代码", "名称"]])
codes = 前10["代码"].tolist()
print()


# ---------- 主菜  fetch_many ----------
def fetch_many(codes, start, end, sleep_sec=0.3):
    """批量拉取，返回 (成功的大表, 失败清单)。"""
    成功 = []
    失败 = []
    总数 = len(codes)

    for i, code in enumerate(codes, start=1):
        try:
            data = fetch_daily(code, start, end)
            if data is None:
                失败.append({"代码": code, "原因": "拉取失败（重试后仍为空）"})
                print(f"{i}/{总数} {code} 失败")
            else:
                成功.append(data)
                print(f"{i}/{总数} {code} {len(data)} 行")
        except Exception as e:
            失败.append({"代码": code, "原因": f"{type(e).__name__}: {e}"})
            print(f"{i}/{总数} {code} 异常：{type(e).__name__}")

        time.sleep(sleep_sec)

    大表 = pd.concat(成功, ignore_index=True) if 成功 else pd.DataFrame()
    return 大表, 失败


大表, 失败 = fetch_many(codes, START, END)
print()


# ---------- 题 4  检查 ----------
print(f"总行数：{len(大表)}")
if len(大表) > 0:
    print("\n每只股票的行数：")
    print(大表.groupby("股票代码").size())
    print(f"\n重复的（股票代码+日期）：{大表.duplicated(subset=['股票代码', '日期']).sum()}")


# ---------- 题 5  存盘 + 报告 ----------
if len(大表) > 0:
    out_path = data_dir / "daily_batch.csv"
    大表.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"\n已保存：{out_path}")

print("\n=== 总结 ===")
print(f"成功 {len(codes) - len(失败)} 只，失败 {len(失败)} 只，共 {len(大表)} 行")
if 失败:
    print("失败清单：")
    for item in 失败:
        print(f"  {item['代码']}：{item['原因']}")
