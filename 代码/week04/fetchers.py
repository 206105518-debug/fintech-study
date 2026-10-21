# fetchers.py ｜ 公共取数模块
#
# 为什么单独抽一个文件：
#   day20、day21 和以后的 pipeline 都要「拉一只股票」。
#   放一份在这里，谁要用就 import，不用复制粘贴。
#   这是你第一次写「可复用的模块」。

import time

import akshare as ak
import pandas as pd

RENAME_MAP = {
    "date": "日期", "open": "开盘", "high": "最高", "low": "最低",
    "close": "收盘", "volume": "成交量", "amount": "成交额",
    "outstanding_share": "流通股本", "turnover": "换手率",
}


def to_sina_symbol(code):
    """600519 → sh600519；000001 → sz000001。"""
    return ("sh" if code[:2] in ("60", "68") else "sz") + code


def fetch_daily(code, start, end, adjust="qfq", retries=3, sleep_sec=1.0):
    """拉单只股票日线并标准化。

    返回中文列名的 DataFrame（含「股票代码」）；失败返回 None。
    注意：新浪的 volume 单位是「股」，和东财的「手」差 100 倍。
    """
    symbol = to_sina_symbol(code)

    raw = None
    for attempt in range(1, retries + 1):
        try:
            raw = ak.stock_zh_a_daily(
                symbol=symbol, start_date=start, end_date=end, adjust=adjust
            )
            if raw is not None and len(raw) > 0:
                break
            print(f"  {code} 返回空数据（第 {attempt} 次）")
        except Exception as e:
            print(f"  {code} 第 {attempt} 次失败：{type(e).__name__}: {e}")
        time.sleep(sleep_sec)

    if raw is None or len(raw) == 0:
        return None

    df = raw.rename(columns=RENAME_MAP).copy()
    df["股票代码"] = code
    df["日期"] = pd.to_datetime(df["日期"])
    df = df.sort_values("日期").reset_index(drop=True)
    return df
