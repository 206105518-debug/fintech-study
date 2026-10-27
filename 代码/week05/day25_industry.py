# day25_industry.py ｜ 2026.10.27 周二：补申万一级行业
#
# 运行方式：
#   cd 金融科技学习/代码/week05
#   python3 day25_industry.py
#
# 数据链：
#   31 个申万一级行业 → 每个行业拉成分股 → 拼成「代码 → 行业」→ merge 进名单
#
# 为什么用申万：
#   券商研报、金工报告几乎都用申万分类。以后读研报看到「电力设备」，
#   能和自己的数据对上；用东财或新浪的行业名就对不上。

import time
from pathlib import Path

import akshare as ak
import pandas as pd

BASE = Path(__file__).parent
data_dir = BASE.parent / "week04" / "data"

def fetch_one_industry(code, name, retries=3):
    for attempt in range(1, retries + 1):
        try:
            cons = ak.index_component_sw(symbol=code)
            if len(cons) > 0:
                return cons
            print(f"  {name} 返回空（第 {attempt} 次）")
        except Exception as e:
            print(f"  {name} 第 {attempt} 次失败：{type(e).__name__}")
        time.sleep(1)
    return None

def fetch_industry_map(level="first"):
    base=ak.sw_index_first_info() if level=="first" else ak.sw_index_second_info()
    
    行业映射=[]
    失败行业=[]

    for i, (_, row) in enumerate(base.iterrows(), start=1):
        行业代码=row["行业代码"].split(".")[0]
        行业名称=row["行业名称"]
        try:
            cons = fetch_one_industry(行业代码, 行业名称)
            for _, c in cons.iterrows():
                行业映射.append({
                    "代码":str(c["证券代码"]).zfill(6),
                    "行业":行业名称,
                })
            print(f"{i}/{len(base)}{行业名称}{len(cons)}只")
        except Exception as e:
            失败行业.append({"行业":行业名称, "原因": f"{type(e).__name__}: {e}"})
            print(f"{i}/{len(base)}{行业名称}")
        time.sleep(0.3)
    df=pd.DataFrame(行业映射).drop_duplicates("代码")
    print(f"{level}共{len(df)}只，{df['行业'].nunique()}个行业，失败{len(失败行业)}个")
    return df

映射=fetch_industry_map(level="first")
print(映射["行业"].value_counts().head(10))

# ==========================================================
# 题 1  拿到 31 个一级行业
#   接口：ak.sw_index_first_info()
#   「行业代码」长这样：801010.SI，
#   但拉成分股时接口要 801010（不带 .SI），所以要切掉后缀。
#   动手：拉一次，打印行业代码和名称，确认是 31 行
# ==========================================================

# TODO 1
一级=ak.sw_index_first_info()
print(len(一级))
print(一级.head())


# ==========================================================
# 题 2  循环拉每个行业的成分股
#   cons = ak.index_component_sw(symbol=行业代码去掉.SI)
#   返回列：序号 / 证券代码 / 证券名称 / 最新权重 / 计入日期
#
#   把每一行拆成 {"代码": 证券代码补 6 位, "行业": 行业名称}
#   收集到一个列表里。
#
#   注意：
#     a) 每拉一个行业 sleep(0.3)，31 个行业也就 10 秒
#     b) 打印进度：「3/31 电力设备 128 只」
#     c) 某个行业失败，不影响其他行业
#   动手：先只拉前 3 个行业试试，通了再拉全部。
# ==========================================================

# TODO 2


# ==========================================================
# 题 3  检查这份映射干不干净
#   a) 一共多少行、多少个不重复代码
#   b) 有没有一只股票属于两个行业？
#      按代码 groupby 后看 size > 1 —— 申万一级是互斥的，
#      出现重复说明数据有问题
#   c) 每个行业多少只
#   动手：三项都打印
# ==========================================================

# TODO 3

# ==========================================================
# 题 4  合并进名单，算覆盖率
#   名单 300 只 left join 行业表（on="代码"）
#   覆盖率 = 行业列非空的股票数 / 300
#   没匹配上的股票单独打印出来
#   动手：合并、打印覆盖率、打印缺失的代码
# ==========================================================

# TODO 4
名单 = pd.read_csv(data_dir / "clean_constituents.csv", dtype={"代码": str})
if "行业" in 名单.columns:
    名单 = 名单.drop(columns=["行业"])
大表=pd.merge(名单, 映射, on="代码", how="left")
覆盖率=大表["行业"].notna().sum()/len(大表)
print(f"覆盖率为{覆盖率*100:.2f}%")

缺失=大表[大表["行业"].isna()]
print(缺失)


# ==========================================================
# 题 5  存盘
#   存两份：
#     data/industry_map.csv        代码 / 行业（全市场）
#     data/clean_constituents.csv  覆盖写，多一列「行业」
#   第二份用 merge 后的表，不要用原来的名单。
# ==========================================================

# TODO 5
映射.to_csv(data_dir / "industry_map.csv", index=False, encoding="utf-8-sig")
大表.to_csv(data_dir / "clean_constituents.csv", index=False, encoding="utf-8-sig")
print("已保存 industry_map.csv 与含行业的 clean_constituents.csv")

# ==========================================================
# 主菜  封装成 fetch_industry_map(level="first")
#   返回 DataFrame：代码 / 行业
#   要求：
#     1) level="first" 用一级，level="second" 用二级
#     2) 单个行业失败记录到失败清单，不影响整体
#     3) 返回前按代码去重，并打印「多少只、多少个行业、失败几个」
#   写完调用、存盘、打印行业分布前 10。
#
#   为什么留 level 参数：
#     一级 31 个、二级 131 个。以后做行业中性化，
#     样本少用一级、样本多用二级——可调，就不用改代码。
# ==========================================================

# TODO 主菜

# ==========================================================
# 收尾
#   1) 行业代码要切掉 .SI；一只股票只能属于一个一级行业
#   2) 明天（10.28）：把行业接进 pipeline，处理停牌缺口
#   3) 提交推送
# ==========================================================
