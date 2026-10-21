# day20_daily_hist_answer.py ｜ 参考答案
# 需要联网；接口报错把原文发我。

import time
from pathlib import Path

import akshare as ak
import pandas as pd

BASE = Path(__file__).parent
data_dir = BASE / "data"
data_dir.mkdir(exist_ok=True)


# ---------- 题 1  拉一只 ----------
df = ak.stock_zh_a_hist(
    symbol="600519", period="daily",
    start_date="20250101", end_date="20251017", adjust="qfq",
)
print(f"形状：{df.shape}")
print(f"列名：{list(df.columns)}")
print(df.head())
print(df.tail())
print()


# ---------- 题 2  类型与范围 ----------
print(df.dtypes)
print(f"日期范围：{df['日期'].min()} ~ {df['日期'].max()}")
print(f"行数：{len(df)}")
print()


# ---------- 题 3  清洗 ----------
df["日期"] = pd.to_datetime(df["日期"])
df = df.sort_values("日期").reset_index(drop=True)
if "股票代码" in df.columns:
    df["股票代码"] = df["股票代码"].astype(str).str.zfill(6)
print(df.dtypes)
print(df.head(3))
print()


# ---------- 题 4  存盘 ----------
path = data_dir / "daily_600519.csv"
df.to_csv(path, index=False, encoding="utf-8-sig")
回读 = pd.read_csv(path, dtype={"股票代码": str})
print(f"存盘：{path}")
print(f"读回：{回读.shape}，代码示例 {回读['股票代码'].iloc[0] if '股票代码' in 回读.columns else '无此列'}")
print()


# ---------- 题 5  三个体检指标 ----------
区间涨跌 = df["收盘"].iloc[-1] / df["收盘"].iloc[0] - 1
停牌天数 = (df["成交量"] == 0).sum()
print(f"区间涨跌幅：{区间涨跌 * 100:.2f}%")
print(f"成交量为 0 的天数：{停牌天数}")
print("缺失值：")
print(df.isna().sum())
print()


# ---------- 主菜  fetch_daily ----------
def fetch_daily(code, start, end, adjust="qfq", retries=3):
    """拉单只股票日线，失败自动重试；全部失败返回 None。"""
    for attempt in range(1, retries + 1):
        try:
            data = ak.stock_zh_a_hist(
                symbol=code, period="daily",
                start_date=start, end_date=end, adjust=adjust,
            )
            if data is None or len(data) == 0:
                print(f"{code} 返回空数据（第 {attempt} 次）")
                time.sleep(1)
                continue

            data["日期"] = pd.to_datetime(data["日期"])
            data = data.sort_values("日期").reset_index(drop=True)
            if "股票代码" in data.columns:
                data["股票代码"] = data["股票代码"].astype(str).str.zfill(6)
            return data
        except Exception as e:
            print(f"{code} 第 {attempt} 次失败：{type(e).__name__}: {e}")
            time.sleep(1)

    print(f"{code} 连续 {retries} 次失败，今天先跳过")
    return None


for code, name in [("600519", "贵州茅台"), ("000001", "平安银行")]:
    data = fetch_daily(code, "20250101", "20251017")
    if data is not None:
        out = data_dir / f"daily_{code}.csv"
        data.to_csv(out, index=False, encoding="utf-8-sig")
        print(f"{name}（{code}）：{len(data)} 行，已存 {out.name}")
    else:
        print(f"{name}（{code}）：没拉到")
