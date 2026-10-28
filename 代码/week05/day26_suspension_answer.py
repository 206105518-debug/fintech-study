# day26_suspension_answer.py ｜ 参考答案

from pathlib import Path

import pandas as pd

BASE = Path(__file__).parent
data_dir = BASE.parent / "week04" / "data"

日线 = pd.read_csv(data_dir / "clean_daily.csv", dtype={"股票代码": str})
日线["日期"] = pd.to_datetime(日线["日期"])


# ---------- 题 1  谁的天数不够 ----------
sizes = 日线.groupby("股票代码").size()
缺少 = sizes[sizes != 190].sort_values()
print("交易日不足 190 的股票：")
print(缺少.to_string())
print()


# ---------- 题 2  统一交易日历 ----------
calendar = pd.DatetimeIndex(sorted(日线["日期"].unique()))
print(f"统一交易日历：{len(calendar)} 天，"
      f"{calendar.min().date()} ~ {calendar.max().date()}")
print()


# ---------- 题 3  一只股票 reindex ----------
one = 日线[日线["股票代码"] == "600930"].set_index("日期")
aligned = one.reindex(calendar)
print(f"600930：原来 {len(one)} 行，补齐后 {len(aligned)} 行，"
      f"其中空行 {aligned['收盘'].isna().sum()} 行")
print(aligned.loc[aligned["收盘"].isna()].head(3))
print()


# ---------- 题 4  两种处理对收益率的影响 ----------
代码 = "301269"
one = 日线[日线["股票代码"] == 代码].set_index("日期").reindex(calendar)

不填 = one["收盘"].copy()
前填 = one["收盘"].ffill()

ret_none = 不填.pct_change()
ret_ffill = 前填.pct_change()

print(f"{代码}：")
print(f"  不填充：有效收益率 {ret_none.notna().sum()} 个")
print(f"  前值填：有效收益率 {ret_ffill.notna().sum()} 个（多出来的是 0 收益日）")
print(f"  不填充的区间收益：{不填.dropna().iloc[-1] / 不填.dropna().iloc[0] - 1:.4f}")
print(f"  前值填的区间收益：{前填.dropna().iloc[-1] / 前填.dropna().iloc[0] - 1:.4f}")
print(f"  不填充的日收益标准差：{ret_none.std():.5f}")
print(f"  前值填的日收益标准差：{ret_ffill.std():.5f}   ← 被 0 收益日摊薄")
print(f"  前值填多出来的 0 收益日：{(ret_ffill == 0).sum() - (ret_none == 0).sum()} 个")
print()


# ---------- 题 5  align_to_calendar ----------
def align_to_calendar(df, calendar):
    """把长表补齐到统一日历，并标记停牌日。"""
    out = []
    for code, g in df.groupby("股票代码"):
        g = g.set_index("日期").reindex(calendar)
        g["股票代码"] = code
        g["是否停牌"] = g["收盘"].isna()
        g = g.reset_index().rename(columns={"index": "日期"})
        out.append(g)
    return pd.concat(out, ignore_index=True)


前5 = 日线[日线["股票代码"].isin(sizes.index[:5])]
补齐5 = align_to_calendar(前5, calendar)
print(f"前 5 只补齐后：{len(补齐5)} 行（应为 5 × {len(calendar)} = {5 * len(calendar)}）")
print()


# ---------- 主菜  只补有缺口的股票 ----------
有缺口 = sizes[sizes < 190].index
补齐 = align_to_calendar(日线[日线["股票代码"].isin(有缺口)], calendar)
补齐["日期"] = pd.to_datetime(补齐["日期"])

停牌统计 = 补齐.groupby("股票代码")["是否停牌"].sum().sort_values(ascending=False)
print("停牌天数最多的前 5 只：")
print(停牌统计.head(5).to_string())
print(f"\n总停牌天数（仅这 {len(有缺口)} 只）：{int(停牌统计.sum())}")

out_path = data_dir / "aligned_daily.csv"
补齐.to_csv(out_path, index=False, encoding="utf-8-sig")
print(f"已保存 {out_path}：{补齐.shape[0]} 行 × {补齐.shape[1]} 列")
