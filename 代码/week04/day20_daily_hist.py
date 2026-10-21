# day20_daily_hist.py ｜ 2026.10.20 周二：第一次拉单只股票的日线
#
# 运行方式：
#   cd 金融科技学习/代码/week04
#   python3 day20_daily_hist.py
#
# 今天只做一件事：把一只股票的日线拉下来，看清它的每一个字段。
#   为什么只拉一只：批量出错时，你要能分清是接口问题、代码问题、还是某只股票的问题。
#   先看清一只，明天才谈批量。

from pathlib import Path
import akshare as ak
import pandas as pd

BASE = Path(__file__).parent
data_dir = BASE / "data"
data_dir.mkdir(exist_ok=True)


# ==========================================================
# 题 1  第一只：贵州茅台 600519
#   接口：ak.stock_zh_a_hist(
#           symbol="600519", period="daily",
#           start_date="20250101", end_date="20251017", adjust="qfq")
#   四个参数的含义：
#     symbol      6 位股票代码，不带后缀
#     period      日频固定写 "daily"
#     start/end   日期写成 8 位字符串 YYYYMMDD
#     adjust      复权方式，见下面
#
#   ⚠️ 复权是什么（这个概念比代码重要）：
#     股票分红送股那天，股价会「跳空下跌」，但你的持仓并没有亏。
#     不复权的价格会把这种除权造成的缺口当成真实下跌，算出来的收益率是错的。
#     "qfq" 前复权：以最新价为基准往前调整，**回测标准用法**
#     "hfq" 后复权：以上市首日为基准往后调整
#     ""    不复权：原始成交价，只适合看当天真实价格
#
#   动手：拉一次，打印 shape、columns、head、tail
#   自查：应该有 11 个字段左右——日期、股票代码、开盘、收盘、最高、最低、
#        成交量、成交额、振幅、涨跌幅、涨跌额、换手率
# ==========================================================

# TODO 1
df = ak.stock_zh_a_daily(
    symbol="sh600519", 
    start_date="20250101", end_date="20251017", adjust="qfq")

print(df.shape)
print(df.columns)

#Index(['date', 'open', 'high', 'low', 'close', 'volume', 'amount',
#'outstanding_share', 'turnover'], dtype='str')

print(df.head())
print(df.tail())
print()


# ==========================================================
# 题 2  看清数据类型和日期范围
#   动手：打印三样
#     a) df.dtypes            —— 日期是 object 还是 datetime？代码是什么类型？
#     b) df["日期"].min() 和 max()   —— 数据覆盖哪一段
#     c) 行数             —— 2025 年至今大约 200 个交易日
#   思考：如果日期是字符串，后面能直接做 resample 吗？（不能）
# ==========================================================

# TODO 2
print(df.dtypes)

print(df["date"].min())
print(df["date"].max())
print(f"行数为{len(df)}") #190
print()



# ==========================================================
# 题 3  清洗成能用的表
#     1) 日期转成时间类型
#     2) 按日期从早到晚排序，行号重排
#     3) 股票代码补成 6 位（如果接口给的是数字）
#   动手：三步做完，再打印 dtypes 和 head 确认
#   提示：排序一定要做。接口返回的顺序不保证，而收益率、均线都依赖顺序。
# ==========================================================

# TODO 3
rename_map = {
    "date": "日期", "open": "开盘", "high": "最高", "low": "最低",
    "close": "收盘", "volume": "成交量", "amount": "成交额",
    "outstanding_share": "流通股本", "turnover": "换手率",
}
df = df.rename(columns=rename_map)
df["股票代码"] = "600519"          # 新浪接口不给代码，自己补上
df["日期"] = pd.to_datetime(df["日期"])
df = df.sort_values("日期").reset_index(drop=True)

print(df.dtypes)
print(df.head(5))
print()


# ==========================================================
# 题 4  存盘
#   存成 data/daily_600519.csv，index=False、utf-8-sig
#   动手：存完读回来，确认行数一致、代码还是 6 位
# ==========================================================

# TODO 4

df.to_csv(data_dir/"daily_600519.csv", index=False, encoding="utf-8-sig")
回读 = pd.read_csv(data_dir / "daily_600519.csv", dtype={"股票代码": str})
print(回读.shape, 回读["股票代码"].iloc[0])

# ==========================================================
# 题 5  三个体检指标（存完数据该看的三件事）
#     a) 区间涨跌幅 = 最后一天收盘价 / 第一天收盘价 - 1
#     b) 有没有停牌：成交量等于 0 的天数
#     c) 有没有缺失：df.isna().sum() 里有没有非零
#   动手：三个都打印出来
#   提醒：如果 a 的结果高得离谱（几百个百分点），大概率是复权没设对，
#        或者是数据源给的字段不是你以为的那样——先怀疑，再下结论。
# ==========================================================

# TODO 5

区间涨跌幅 = df["收盘"].iloc[-1] / df["收盘"].iloc[0] - 1
print(f"区间涨跌幅：{区间涨跌幅 * 100:.2f}%")
print()
停牌天数=(df["成交量"]==0).sum()
print(f"停牌天数为{停牌天数}")
print()
print(df.isna().sum())
print()

df.to_csv(data_dir/"daily_600519.csv", index=False, encoding="utf-8-sig")
# ==========================================================
# 主菜  封装成 fetch_daily()
#   要求：
#     def fetch_daily(code, start, end, adjust="qfq"):
#         返回清洗好的 DataFrame（日期为索引或列均可，但要转好类型）
#     1) 单次失败自动重试，最多 3 次，每次间隔 1 秒
#        （免费接口偶尔抽风，重试两次常常就好了）
#     2) 3 次都失败，打印一句人话并返回 None
#     3) 不要静默失败——失败的代码和原因要打印出来
#   写完用它拉两只股票（600519 茅台、000001 平安银行），各存一份 CSV。
#   为什么要重试：你没有能力让接口稳定，但你有能力让代码扛住不稳定。
# ==========================================================

# TODO 主菜
#卡住：参考答案
import time

def fetch_daily(code, start, end, adjust="qfq"):
    sina_symbol=("sh" if code[:2] in ("60", "68") else "sz") + code
    raw=None
    for attempt in range(1,4):
        try:
            
            raw = ak.stock_zh_a_daily(
                symbol=sina_symbol,              # sh600519 —— 新浪认这个
                start_date=start, end_date=end, adjust=adjust,
            )
            if raw is not None and len(raw)>0:
                break
            print(f"{code} 返回空数据（第 {attempt} 次）")
        except Exception as e:
            print(f"{code} 第 {attempt} 次失败：{type(e).__name__}: {e}")
        time.sleep(1)
    if raw is None or len(raw) == 0:
        print(f"{code} 连续 3 次失败，跳过")
        return None


    
    rename_map = {
        "date": "日期", "open": "开盘", "high": "最高", "low": "最低",
        "close": "收盘", "volume": "成交量", "amount": "成交额",
        "outstanding_share": "流通股本", "turnover": "换手率",
    }
    df = raw.rename(columns=rename_map)
    df["股票代码"] = code
    df["日期"] = pd.to_datetime(df["日期"])
    df = df.sort_values("日期").reset_index(drop=True)
    return df



for code, name in [("600519", "贵州茅台"), ("000001", "平安银行")]:
    data = fetch_daily(code, "20250101", "20251017")
    if data is not None:
        data.to_csv(data_dir / f"daily_{code}.csv", index=False, encoding="utf-8-sig")
        print(f"{name}({code}):{len(data)} 行已保存")
    else:
        print(f"{name}({code}):没拉到")   

# ==========================================================
# 收尾
#   1) 记住：回测一律用前复权（qfq）
#   2) 明天（10.21）：按名单批量拉 10 只，加限流与失败清单
#   3) 提交推送
# ==========================================================
