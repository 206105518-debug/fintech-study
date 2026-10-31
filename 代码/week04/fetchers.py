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


def available_date(report_date):
    """报告期 → 数据可用日（监管披露截止日的次日）。

    A 股披露截止：年报 4/30、一季报 4/30、半年报 8/31、三季报 10/31。
    用它做 point-in-time，比相信数据源给的「公告日期」可靠。
    """
    m = report_date.month
    if m == 12:
        return pd.Timestamp(report_date.year + 1, 5, 1)
    if m == 3:
        return pd.Timestamp(report_date.year, 5, 1)
    if m == 6:
        return pd.Timestamp(report_date.year, 9, 1)
    return pd.Timestamp(report_date.year, 11, 1)


def fetch_financial(code, start_year="2020"):
    """拉单只股票的财务指标（年报口径），失败返回 None。

    返回列：报告期 / 净资产收益率(%) / 主营业务收入增长率(%) / 公告日期 / 可用日 / 股票代码
    注意：银行、券商的「主营业务收入增长率」通常为空——口径不适用。
    """
    try:
        财务 = ak.stock_financial_analysis_indicator(symbol=code, start_year=start_year)
        利润 = ak.stock_financial_report_sina(
            stock=to_sina_symbol(code), symbol="利润表")
    except Exception:
        return None

    try:
        财务["报告期"] = pd.to_datetime(财务["日期"]).dt.normalize()
        利润["报告期"] = pd.to_datetime(利润["报告日"], format="%Y%m%d")

        合并 = pd.merge(
            财务[["报告期", "净资产收益率(%)", "主营业务收入增长率(%)"]],
            利润[["报告期", "公告日期"]],
            on="报告期", how="inner",
        )
        合并["可用日"] = 合并["报告期"].apply(available_date)
        合并["股票代码"] = code
        return 合并[合并["报告期"].dt.month == 12].reset_index(drop=True)
    except Exception:
        return None
