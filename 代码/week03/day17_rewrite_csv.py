# day17_rewrite_csv.py ｜ 2026.10.17 周六：用 pandas 重写 day08 的 CSV 统计脚本
#
# 运行方式：
#   cd 金融科技学习/代码/week03
#   python3 day17_rewrite_csv.py
#
# 今天的任务：
#   把 9 月 22 日你用 csv 模块手写的那份脚本（代码/week01/day08_csv_stats.py）
#   用 pandas 重写一遍。**同样的输入、同样的输出，看代码短了多少。**
#
#   重写完把两个文件都打开放在一起看：
#     手写版：自己拆行拆列、自己判断空字符串、自己写数值列名单
#     pandas 版：read_csv 一行进来，剩下的都是「声明要什么」
#   这就是数据岗第一工具为什么是 pandas。

from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent
csv_path = BASE.parent / "week01" / "hs300_sample.csv"


# ==========================================================
# 题 1  读进来（和 day12 一样的开头）
#   用 pd.read_csv 读，别忘了 dtype={"代码": str} 保住前导零。
#   动手：读进来打印一次，确认代码列显示的是 000858 而不是 858
# ==========================================================

# TODO 1
df=pd.read_csv(csv_path, encoding="utf-8", dtype={"代码":str})
print(df)
print()
# ==========================================================
# 题 2  行数
#   手写版：读一遍 reader 再数数，或者循环累加
#   pandas 版：读进来之后 df.shape 就够了
#   动手：打印「数据行数」和「列数」
#   自查：12 行、6 列
# ==========================================================

# TODO 2
print(df.shape)
print()
# ==========================================================
# 题 3  每列缺失（个数 + 比例）
#   手写版：双层循环 + 判断 value == "" + 字典累加，大概十几行
#   pandas 版：
#     df.isna().sum()                个数
#     (df.isna().mean() * 100).round(2)   比例
#   动手：两张都打印出来
#   自查：涨跌幅 3（25%）、市盈率 2（16.67%）、成交额 1（8.33%）
# ==========================================================

# TODO 3
缺失=df.isna().sum()
比例=(df.isna().mean()*100).round(2)
print(缺失)
print(比例)
print()
# ==========================================================
# 题 4  数值列均值（这里有个新工具）
#   手写版：你当时手写了一张名单 ["收盘价", "涨跌幅", "市盈率", "成交额"]。
#   pandas 版可以直接问它「哪些列是数值列」：
#     df.select_dtypes(include="number").columns
#   然后对这些列求值：
#     df.select_dtypes(include="number").mean()
#   动手：两步都跑一遍
#   想一想：为什么这次可以放心用「自动判断」，而 day08 里不行？
#          （提示：day08 那次的坑是「代码」列被当成数字。
#            这次你在 read_csv 时指定了 dtype，代码列已经是文本，
#            剩下的数值列就都是真数值了。）
#   自查：收盘价 209.83、涨跌幅 0.28、市盈率 22.38、成交额 26.43
# ==========================================================

# TODO 4
数值列=df.select_dtypes(include="number").columns
print(数值列)
均值=(df.select_dtypes(include="number").mean()).round(2)
print(均值)
print()

# ==========================================================
# 题 5  打印成和 day08 一样的表
#   格式要求（和那天一样）：
#     列名       缺失      均值
#     代码          0
#     收盘价        0   209.83
#   动手：复用你那天写过的对齐写法（f-string 的 :<8 :>8 :>12.2f）
#   提示：遍历列名可以用 df.columns
# ==========================================================

# TODO 5
print(f"{'列名':<8}{'缺失':>8}{'均值':>12}")
for col in df.columns:
    missing=df[col].isna().sum()
    if col in 数值列:
        print(f"{col:<8}{missing:>8}{df[col].mean():>12.2f}")
    else:
        print(f"{col:<8}{missing:>8}")
print()

# ==========================================================
# 主菜  封装成 analyze_csv_pandas(path)
#   要求：返回一个字典，结构和 day08 的 analyze_csv 尽量一致：
#     {"行数": ..., "缺失": {列名: 个数}, "均值": {列名: 均值}}
#   文件不存在时用 try/except 兜住，返回 None（和那天一样）。
#   写完做两件事：
#     1) 调用它，把结果打印成表
#     2) 传一个不存在的文件名，确认不崩
#
#   然后做今天最重要的一个对比：
#     打开 代码/week01/day08_csv_stats.py，数一数它有多少行代码、
#     用了几个 for 循环；再数一数这个文件。
#     把两个数字写在下面：
#       手写版：______ 行，______ 个 for 循环
#       pandas 版：______ 行，______ 个 for 循环
#   一句话总结这个差别（自己写）：
#
# ==========================================================

# TODO 主菜
#卡住：怎么返回字典
def analyze_csv_pandas(path):
    try:
        df=pd.read_csv(path, encoding="utf-8", dtype={"代码":str})
    except FileNotFoundError:
        print("没有此文件")
        return None

    缺失=df.isna().sum().to_dict()

    均值=(df.select_dtypes(include="number").mean()).round(2).to_dict()

    return {
    "行数":len(df), 
    "缺失":缺失, 
    "均值":均值,
}

r1 = analyze_csv_pandas(csv_path)
r2 = analyze_csv_pandas(BASE.parent / "week01" / "没有这个文件.csv")

print(r1)
print(r2)

# ==========================================================
# 收尾
#   1) 这一段的 pandas 到此主线走完，周日做时间序列收尾
#   2) 下一段（10.19 起）：akshare 取真实数据，搭沪深300数据管道
#   3) 提交推送
# ==========================================================
