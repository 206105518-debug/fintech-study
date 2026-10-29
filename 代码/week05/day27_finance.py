# day27_finance.py ｜ 2026.10.29 周四：补财务字段（ROE / 营收增速 / 公告日）
#
# 运行方式：
#   cd 金融科技学习/代码/week05
#   python3 day27_finance.py
#
# 今天的数据链：
#   财务指标（ROE、营收增长率） + 公告日期 → 按报告期合并 → 能防前视偏差的财务表
#
# 为什么必须有「公告日期」：
#   2026 年一季报的报告期是 2026-03-31，但 4 月 25 日才公布。
#   如果你在 4 月 1 日就用这份数据选股，就是用了未来信息——回测收益虚高，实盘必崩。

import time
from pathlib import Path

import akshare as ak
import pandas as pd

BASE = Path(__file__).parent
data_dir = BASE.parent / "week04" / "data"


# ==========================================================
# 题 1  拉一只股票的财务指标
#   接口：ak.stock_financial_analysis_indicator(symbol="600519", start_year="2024")
#   返回 10 行 × 86 列（按季度）。
#   只挑三列：
#     "日期"、"净资产收益率(%)"、"主营业务收入增长率(%)"
#   动手：拉一次，只保留这三列，打印出来
#   自查：日期应该是 2024-03-31、2024-06-30 这样的季末
# ==========================================================

# TODO 1
财务=ak.stock_financial_analysis_indicator(symbol="600519", start_year="2020")
print(财务.shape)
print(财务.columns)
财务["日期"]=pd.to_datetime(财务["日期"])
print(财务["日期"])
print(财务["净资产收益率(%)"])
print(财务["主营业务收入增长率(%)"])

# ==========================================================
# 题 2  拉公告日期
#   接口：ak.stock_financial_report_sina(stock="sh600519", symbol="利润表")
#   返回 100 多行 × 80 多列，只要两列：
#     "报告日"（字符串，如 "20260331"）
#     "公告日期"（字符串，如 "20260425"）
#   动手：拉一次，只保留这两列，打印前 5 行
#   注意：报告日是 8 位字符串，要和题 1 的日期对齐，得先转成时间类型。
# ==========================================================

# TODO 2
利润=ak.stock_financial_report_sina(stock="sh600519", symbol="利润表")
print(利润.shape)
print(利润[["报告日","公告日期"]].head(5))

# ==========================================================
# 题 3  按报告期合并
#   两边都有「报告期」，但格式不同：
#     题 1：datetime.date（2024-03-31）
#     题 2：字符串（20240331）
#   先把两边都转成同一种格式（建议都转成 Timestamp/日期）：
#     pd.to_datetime(列)
#   然后 merge（on="报告期"，how="inner"），得到：
#     报告期 / ROE / 营收增速 / 公告日期
#   动手：合并，打印前 5 行
#   自查：公告日期应该都比报告期晚 1 个月以上
# ==========================================================

# TODO 3
财务["报告期"]=pd.to_datetime(财务["日期"]).dt.normalize()
利润["报告期"]=pd.to_datetime(利润["报告日"], format="%Y%m%d")
合并=pd.merge(财务[["报告期","净资产收益率(%)","主营业务收入增长率(%)"]], 利润[["报告期","公告日期"]], on="报告期", how="inner")
print(合并.head(5))

#         报告期  净资产收益率(%)  主营业务收入增长率(%)      公告日期
#0 2024-03-31      10.04       18.1127  20250430
#1 2024-06-30      19.08       17.7575  20250813
#2 2024-09-30      25.59       16.9537  20251030
#3 2024-12-31      36.99       15.7120  20260417
#4 2025-03-31      10.39       10.5415  20260425 数据有问题

def 可用日(报告期):
    m = 报告期.month
    if m == 12: return pd.Timestamp(报告期.year + 1, 5, 1)   # 年报截止 4/30，次日可用
    if m == 3:  return pd.Timestamp(报告期.year, 5, 1)        # 一季报截止 4/30
    if m == 6:  return pd.Timestamp(报告期.year, 9, 1)        # 半年报截止 8/31
    return pd.Timestamp(报告期.year, 11, 1)                    # 三季报截止 10/31            
合并["可用日"] = 合并["报告期"].apply(可用日)

年报 = 合并[合并["报告期"].dt.month == 12].reset_index(drop=True)
print(年报[["报告期", "净资产收益率(%)", "主营业务收入增长率(%)", "可用日"]])
# ==========================================================
# 题 4  前视偏差自检
#   检查：有没有「公告日期早于报告期」的行？
#   正常应该是 0 —— 报表不可能在期末之前公布。
#   动手：用一个布尔列筛出来，打印条数
#   如果出现非 0，说明合并键配错了（比如把「报告日」和「公告日期」串了）。
# ==========================================================

# TODO 4


# ==========================================================
# 题 5  批量 10 只
#   从 data/constituents_with_industry.csv 取前 10 个代码，
#   对每只重复题 1-3：
#     - 每只 2 次请求，加 sleep(0.3)
#     - 打印进度
#     - 加一列「股票代码」
#   最后 concat 成一张表，存 data/financial_10.csv
#   动手：跑完打印总行数、每只多少期财报
# ==========================================================

# TODO 5


# ==========================================================
# 主菜  封装成 fetch_financial(code)
#   def fetch_financial(code):
#       返回该股票的财务表：报告期 / ROE / 营收增速 / 公告日期
#       任一步失败返回 None（调用处记失败清单）
#   注意代码格式：
#     财务指标接口用 "600519"
#     利润表接口用 "sh600519"（带前缀）
#   写完用它对 10 只跑一遍，统计成功/失败。
#
#   这个函数以后会被 pipeline 调用，所以：
#     - 不要在函数里存盘（存盘是调用方的事）
#     - 不要在函数里 print 太多（进度由调用方打印）
# ==========================================================

# TODO 主菜

def fetch_financial(code):
    前缀 = "sh" if code[:2] in ("60", "68") else "sz"
    try:
        财务=ak.stock_financial_analysis_indicator(symbol=code, start_year="2020")
        利润=ak.stock_financial_report_sina(stock=前缀+code, symbol="利润表")
    except Exception as e:
        print(f"{code}拉取失败：{type(e).__name__}")
        return None

    财务["报告期"]=pd.to_datetime(财务["日期"]).dt.normalize()
    利润["报告期"]=pd.to_datetime(利润["报告日"], format="%Y%m%d")

    合并=pd.merge(
        财务[["报告期","净资产收益率(%)","主营业务收入增长率(%)"]],
        利润[["报告期","公告日期"]], 
        on="报告期", 
        how="inner",
    )

    合并["可用日"] = 合并["报告期"].apply(可用日)
    合并["股票代码"]=code

    return (合并[合并["报告期"].dt.month == 12].reset_index(drop=True))

成分=pd.read_csv(data_dir/"constituents_with_industry.csv", encoding="utf-8", dtype={"代码":str})
前10=成分["代码"].head(10).tolist()
成功=[]
失败=[]
for i,code in enumerate(前10,start=1):
    df=fetch_financial(code)
    if df is not None:
        成功.append(df)
        print(f"{i}/{len(前10)} {code}成功")
    else:
        失败.append(code)
        print(f"{i}/{len(前10)} {code}拉取失败")
    time.sleep(0.3)

年报=pd.concat(成功, ignore_index=True) if 成功 else pd.DataFrame()
print(f"\n成功{len(成功)}只，失败{len(失败)}只")
print(年报.shape)

if len(年报):  #判断 年报 这个 DataFrame 是不是「空的」 if 数字: 在 Python 里：0 是假（False），非 0 是真（True
    年报.to_csv(data_dir / "financial_10.csv", index=False, encoding="utf-8-sig")
    print(f"已保存：{len(年报)} 行")


# ==========================================================
# 收尾
#   1) 记住：财务数据要按「公告日期」使用，不是报告期
#   2) 周六（10.31）：全量 300 只 + 接进 pipeline
#   3) 提交推送
# ==========================================================
