"""无网络请求的数据转换与清洗函数。"""

import pandas as pd

from pipeline_config import CONFIG


def shift_date(date_text, days):
    """把 YYYYMMDD 日期向前或向后移动指定天数。"""
    return (
        pd.Timestamp(date_text) + pd.Timedelta(days=days)
    ).strftime("%Y%m%d")


def missing_periods(old_start, old_end, target_start, target_end):
    """返回需要补拉的日期段列表。"""
    periods = []

    if target_start < old_start:
        head_end = min(shift_date(old_start, -1), target_end)
        periods.append((target_start, head_end))

    if target_end > old_end:
        tail_start = max(shift_date(old_end, 1), target_start)
        periods.append((tail_start, target_end))

    return periods


def filter_daily_range(df):
    """只保留当前配置要求的日期范围。"""
    if df.empty:
        return df

    dates = pd.to_datetime(df["日期"])
    mask = (
        (dates >= pd.Timestamp(CONFIG["start"]))
        & (dates <= pd.Timestamp(CONFIG["end"]))
    )
    return df.loc[mask].copy()


def clean_daily(df):
    """统一日线字段类型、排序并按股票代码和日期去重。"""
    df["股票代码"] = df["股票代码"].astype(str).str.zfill(6)
    df["日期"] = pd.to_datetime(df["日期"])

    numeric_columns = [
        "开盘", "最高", "最低", "收盘",
        "成交量", "成交额", "流通股本", "换手率",
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.sort_values(["股票代码", "日期"])
    return df.drop_duplicates(subset=["股票代码", "日期"])


def merge_valuation(constituents, valuation):
    """以名单为准左连接估值表，并输出市值覆盖率。"""
    merged = pd.merge(constituents, valuation, on="代码", how="left")
    coverage = merged["总市值"].notna().mean() * 100
    print(f"覆盖率{coverage:.2f}%")
    return merged