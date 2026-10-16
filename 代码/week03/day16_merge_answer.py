# day16_merge_answer.py ｜ 参考答案
# 先自己做，卡住 30 分钟以上再来看。

from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent
csv_path = BASE.parent / "week01" / "hs300_sample.csv"
行情表 = pd.read_csv(csv_path, encoding="utf-8", dtype={"代码": str})
名单表 = pd.DataFrame({
    "代码": ["600519", "300750", "600036", "601318", "000858", "999999"],
    "行业": ["食品饮料", "电力设备", "银行", "非银金融", "食品饮料", "未知"],
    "权重": [0.08, 0.06, 0.05, 0.04, 0.03, 0.01],
})


# ---------- 题 1  四种连接 ----------
print("=== 四种连接方式，各剩几行 ===")
for how in ["inner", "left", "right", "outer"]:
    merged = pd.merge(名单表, 行情表, on="代码", how=how)
    print(f"名单 join 行情，how={how:<5} → {len(merged)} 行")

print("\ninner 的结果（两边都有的 5 只）：")
print(pd.merge(名单表, 行情表, on="代码", how="inner")[["代码", "名称", "行业", "权重"]])
print()


# ---------- 题 2  左连接带来的缺失 ----------
left_merged = pd.merge(名单表, 行情表, on="代码", how="left")
no_quote = left_merged[left_merged["收盘价"].isna()]
print("以名单表为准左连接后，行情为空的：")
print(no_quote[["代码", "行业", "收盘价", "涨跌幅"]])
print("判断：999999 在行情表里不存在，要么代码写错，要么当天没有行情。\n")


# ---------- 题 3  连接键类型不一致 ----------
名单表错 = pd.DataFrame({"代码": [600519, 300750], "行业": ["食品饮料", "电力设备"]})
try:
    pd.merge(行情表.head(2), 名单表错, on="代码")
except ValueError as e:
    print("连接键类型不一致时的报错：")
    print(f"  ValueError: {e}")
print("修法：两边统一成字符串。\n")


# ---------- 题 4  列名重名 ----------
名单表带名称 = 名单表.assign(
    名称=["贵州茅台", "宁德时代", "招商银行", "中国平安", "五粮液", "不存在的股票"]
)
conflict = pd.merge(名单表带名称, 行情表, on="代码", how="left")
print("两表都有「名称」列时，默认后缀：")
print([c for c in conflict.columns if "名称" in c])

named = pd.merge(名单表带名称, 行情表, on="代码", how="left", suffixes=("_名单", "_行情"))
print("自定义后缀之后：")
print([c for c in named.columns if "名称" in c])
print()


# ---------- 题 5  concat 纵向拼接 ----------
上半 = 行情表.head(6)
下半 = 行情表.tail(6)
拼回来 = pd.concat([上半, 下半], ignore_index=True)
print(f"上半 {len(上半)} 行 + 下半 {len(下半)} 行 = 拼回来 {len(拼回来)} 行")
print(f"行号是否重新从 0 开始：{list(拼回来.index[:3])} ... {list(拼回来.index[-3:])}")
print()


# ---------- 主菜  合并 + 分组统计 ----------
完整表 = pd.merge(名单表, 行情表, on="代码", how="left")
完整表 = 完整表[["代码", "名称", "行业", "权重", "收盘价", "涨跌幅", "市盈率"]]
print("=== 合并后的完整表 ===")
print(完整表)

完整表["涨跌幅×权重"] = 完整表["涨跌幅"] * 完整表["权重"]
分组 = 完整表.groupby("行业", observed=True).agg(
    股票数=("代码", "count"),
    权重合计=("权重", "sum"),
    加权涨跌=("涨跌幅×权重", lambda s: s.sum(min_count=1)),   # 全 NaN 时返回 NaN，而不是 0
)
分组["加权平均涨跌幅"] = (分组["加权涨跌"] / 分组["权重合计"]).round(3)
print("\n=== 按行业加权平均涨跌幅 ===")
print(分组[["股票数", "权重合计", "加权平均涨跌幅"]])

print("\n注意 0.000 和 NaN 的区别：")
print("  未知、非银金融这两组的涨跌幅本来就是缺失的（中国平安停牌、999999 没有行情），")
print("  如果直接用 sum()，pandas 会把「全是 NaN」算成 0，看起来像零涨跌。")
print("  加上 min_count=1 之后，它们如实显示成 NaN —— 缺失就该是缺失。")

print("\n观察：未知行业那只是名单里多出来的股票，涨跌幅是 NaN，")
print("      它没参与任何行业的加权计算——数据不齐时，结果自然会缺。")
