# day13_pandas_filter_answer.py ｜ 参考答案
# 先自己做，卡住 30 分钟以上再来看。

from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent
csv_path = BASE.parent / "week01" / "hs300_sample.csv"
df = pd.read_csv(csv_path, encoding="utf-8", dtype={"代码": str})


# ---------- 题 1  多条件筛选 ----------
print(f"上涨的：{len(df[df['涨跌幅'] > 0])} 只")

cheap_and_up = df[(df["市盈率"] < 30) & (df["涨跌幅"] > 0)]
print(f"市盈率<30 且上涨的：{len(cheap_and_up)} 只")

expensive_or_falling = df[(df["市盈率"] > 50) | (df["涨跌幅"] < -2)]
print(f"高估值或大跌的：{len(expensive_or_falling)} 只")

not_moutai = df[~(df["名称"] == "贵州茅台")]
print(f"排除茅台后：{len(not_moutai)} 只")

picked_names = df[df["名称"].isin(["贵州茅台", "比亚迪", "五粮液"])]
print(f"只留三只指定的：{len(picked_names)} 只")
print()


# ---------- 题 2  loc 与 iloc ----------
print("loc[3]（标签 3）：")
print(df.loc[3].to_dict())

print("\nloc[0:2] 含右端，行数：", len(df.loc[0:2]))
print("iloc[0:2] 不含右端，行数：", len(df.iloc[0:2]))

print("\n取一个格子：df.loc[0, '名称'] =", df.loc[0, "名称"])
print("取一个格子：df.iloc[0, 1] =", df.iloc[0, 1])

df2 = df.set_index("代码")
print("\n按代码取一行：")
print(df2.loc["600519"][["名称", "收盘价", "涨跌幅"]])
print()


# ---------- 题 3  排序与取前几名 ----------
print("按涨跌幅从高到低（前 3 行）：")
print(df.sort_values("涨跌幅", ascending=False).head(3)[["名称", "涨跌幅"]])

print("\n成交额最大的 3 只：")
print(df.nlargest(3, "成交额")[["名称", "成交额"]])

print("\n市盈率最小的 3 只：")
print(df.nsmallest(3, "市盈率")[["名称", "市盈率"]])
print()


# ---------- 题 4  新增列与赋值 ----------
df["是否上涨"] = df["涨跌幅"] > 0
print("新增「是否上涨」列之后：")
print(df[["名称", "涨跌幅", "是否上涨"]].head(3))

# 坑示范：切出来的副本改了，原表不动
sub = df[df["涨跌幅"] > 0]
sub["标记"] = 1
print(f"\n副本里加了「标记」列，原表有没有？{'标记' in df.columns}")

# 正确写法：要改原表就用 loc
df.loc[df["市盈率"] > 30, "估值标签"] = "高估值"
df.loc[df["市盈率"] <= 30, "估值标签"] = "低估值"
print("\n用 loc 给原表加「估值标签」之后：")
print(df[["名称", "市盈率", "估值标签"]])
print()


# ---------- 题 5  综合练习 ----------
screen_result = df[(df["市盈率"] < 30) & (df["涨跌幅"] > 0) & (df["成交额"] > 20)]
screen_result = screen_result[["代码", "名称", "收盘价", "涨跌幅", "市盈率"]]
screen_result = screen_result.sort_values("市盈率")
print("选股结果：")
print(screen_result)

screen_result.to_csv("picked2.csv", index=False, encoding="utf-8-sig")
print("已保存 picked2.csv")
print()


# ---------- 主菜  把筛选封装成函数 ----------
def screen(df, max_pe=30, min_change=0.0, min_amount=0.0):
    """按市盈率、涨跌幅、成交额三个条件筛选，返回按市盈率升序排好的表。

    为什么给默认值：常用的那套条件直接调用就行，想试别的只改一个参数。
    """
    result = df[(df["市盈率"] < max_pe)
                & (df["涨跌幅"] > min_change)
                & (df["成交额"] > min_amount)]
    result = result.sort_values("市盈率")
    print(f"条件：市盈率<{max_pe}、涨跌幅>{min_change}、成交额>{min_amount} → 筛出 {len(result)} 只")
    return result


print("=== 主菜：同一份数据，三组条件 ===")
print(screen(df)[["名称", "市盈率", "涨跌幅"]])
print()
print(screen(df, max_pe=10)[["名称", "市盈率", "涨跌幅"]])
print()
print(screen(df, min_change=-2, min_amount=15)[["名称", "市盈率", "涨跌幅", "成交额"]])
