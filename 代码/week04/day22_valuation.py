# day22_valuation.py ｜ 2026.10.22 周四：给 10 只股票补估值（百度源）
#
# 运行方式：
#   cd 金融科技学习/代码/week04
#   python3 day22_valuation.py
#
# 为什么换数据源：
#   东方财富的两个接口（日线、全市场快照）在你的网络下都被拒了：
#   RemoteDisconnected: Remote end closed connection without response
#   这不是代码问题。实测百度估值接口是通的，今天就改用它。
#
#   这也是数据工作的常态：**数据源会挂，管道要能换源。**
#
# 百度接口的特点：
#   一次只给一只股票、一个指标，返回近一年每个交易日的历史序列。
#   所以我们只做 10 只，先把逻辑跑通；等东财恢复再上 300 只。

import time
from pathlib import Path

import akshare as ak
import pandas as pd

BASE = Path(__file__).parent
data_dir = BASE / "data"

# 指标名 → 表里的列名
INDICATORS = {
    "总市值": "总市值",          # 单位：亿元
    "市盈率(TTM)": "市盈率TTM",
    "市净率": "市净率",
}


# ==========================================================
# 题 1  取 10 只股票
#   读 data/daily_batch.csv，取出不重复的前 10 个代码。
#   提示：pd.read_csv(..., dtype={"股票代码": str})["股票代码"].unique()[:10]
# ==========================================================

# TODO 1
日线=pd.read_csv(data_dir/"daily_batch.csv", dtype={"股票代码": str})
codes=日线["股票代码"].unique()[:10].tolist()
print(codes)
print()
# ==========================================================
# 题 2  单只股票：一次拿三个指标
#   对每个指标调用：
#     ak.stock_zh_valuation_baidu(symbol=code, indicator=指标名, period="近一年")
#   返回 366 行、两列（date, value）。
#
#   要求：
#     a) 先按 date 排序，再取最后一行（最后一行才是最新的）
#     b) 把三个指标拼成一个字典：{"代码": code, "总市值": ..., "市盈率TTM": ..., "市净率": ...}
#     c) 每取完一个指标 time.sleep(0.2)，别连着猛发
#   动手：先用 600519 试一次，打印结果
#   自查：茅台的总市值约 1.6 万亿（16482 亿元）、市盈率 TTM 约 20、市净率约 6.5
# ==========================================================

# TODO 2

结果={"代码":600519}
for 指标名, 列名 in INDICATORS.items():
    数据=ak.stock_zh_valuation_baidu(symbol=600519, indicator=指标名, period="近一年")
    数据=数据.sort_values("date")
    最新值=float(数据["value"].iloc[-1])
    结果[列名]=最新值
    time.sleep(0.2)
print(结果)
print()
# ==========================================================
# 题 3  循环 10 只，收集结果
#   复用你昨天写过的模式：
#     成功的 append 进列表，失败的记进「失败清单」（代码 + 原因）
#     每只之间 sleep，打印进度
#   注意：这次每只股票要发 3 次请求，所以 10 只 = 30 次请求，
#        每次之间都要有间隔，不然容易被限流。
# ==========================================================

# TODO 3
估值列表=[]
失败=[]
for i,code in enumerate(codes,start=1):
    try:
        结果={"代码":code}
        for 指标名, 列名 in INDICATORS.items(): 
            数据=ak.stock_zh_valuation_baidu(symbol=code, indicator=指标名, period="近一年")
            数据=数据.sort_values("date")
            最新值=float(数据["value"].iloc[-1])
            结果[列名]=最新值
            time.sleep(0.2)
        估值列表.append(结果)
        print(f"{i}/{len(codes)} {code} 成功")
    except Exception as e:
        失败.append({"代码": code, "原因": f"{type(e).__name__}: {e}"}) #拼出可读的错误信息
        print(f"{i}/{len(codes)} {code} 失败")


# ==========================================================
# 题 4  合并与覆盖率
#   a) 把结果转成 DataFrame：pd.DataFrame(估值列表)
#   b) 和名单 merge（on="代码"，how="left"，以名单为准）
#   c) 算覆盖率：拿到总市值的股票数 / 10
#   思考：如果有 1 只没拿到，你会在后续分析里怎么处理它？
# ==========================================================

# TODO 4
估值表=pd.DataFrame(估值列表)
名单 = pd.read_csv(data_dir / "hs300_constituents.csv", dtype={"代码": str})
总表=pd.merge(名单[名单["代码"].isin(codes)], 估值表, on="代码", how="left")
总市值的股票数=总表["总市值"].notna().sum()
print(f"覆盖率{总市值的股票数/len(codes)*100:.2f}%")
print(总表)
print()

# ==========================================================
# 题 5  存盘
#   存成 data/valuation_10.csv，index=False、utf-8-sig
#   读回来确认：行数是 10 或更少、代码保持 6 位
# ==========================================================

# TODO 5
总表.to_csv(data_dir/"valuation_10.csv", index=False, encoding="utf-8-sig")
回读=pd.read_csv(data_dir/"valuation_10.csv", dtype={"代码":str})
print(回读.shape)
print()
# ==========================================================
# 主菜  封装成 fetch_valuation(code)
#   要求：
#     1) 三个指标循环取，每个之后 sleep
#     2) 单个指标失败时，那一项设为 None，其他指标照常取
#        （不要因为市盈率拿不到，连总市值也丢了）
#     3) 三个都失败，返回 None
#   然后写 enrich_valuation(codes) 循环调用它，
#   返回 (DataFrame, 失败清单)。
#
#   为什么「单项失败不影响其他项」很重要：
#   真实数据里经常是某几个字段缺失，而不是整条记录缺失。
#   你的管道要能拿到能拿的部分，并明确标出缺的部分。
# ==========================================================

# TODO 主菜
#卡住：参考答案
def fetch_valuation(code):
    row={"代码":code}
    ok=0
    for 指标名, 列名 in INDICATORS.items():
        try:
            数据 = ak.stock_zh_valuation_baidu(symbol=code, indicator=指标名, period="近一年")
            数据 = 数据.sort_values("date")
            row[列名] = float(数据["value"].iloc[-1])
            ok+=1
        except Exception as e:
            print(f"{code}{指标名}失败：{type(e).__name__}")
            row[列名]=None
        time.sleep(0.2)
    return row if ok>0 else None

def enrich_valuation(codes):
    rows,failed=[], []
    for i, code in enumerate(codes, start=1):
        v = fetch_valuation(code)
        if v is None:
            failed.append({"代码": code, "原因": "三个指标均失败"})
            print(f"{i}/{len(codes)} {code} 失败")
        else:
            rows.append(v)
            print(f"{i}/{len(codes)} {code} 成功")
        time.sleep(0.2)
    return pd.DataFrame(rows), failed



# ==========================================================
# 收尾
#   1) 记住：数据源会挂，换源比死磕高效；单项失败不等于整条失败
#   2) 明天（10.23）：统一字段、查重、缺失体检，落盘三个文件
#   3) 提交推送
# ==========================================================
