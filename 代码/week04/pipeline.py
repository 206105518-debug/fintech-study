# pipeline.py ｜ 数据管道第一版
#
# 运行方式：
#   cd 金融科技学习/代码/week04
#   python3 pipeline.py
#
# 这一版要做的事：
#   名单 → 日线 → 清洗 → 落盘
#   （估值和健壮性明天补）
#
# 为什么要有这个文件：
#   day19–day23 是分段练习，每段一个脚本。
#   真实工作里你要一条命令跑完全流程——这就是 pipeline 的意义。

import time
from datetime import datetime
from pathlib import Path

import pandas as pd

import akshare as ak

from fetchers import fetch_daily

BASE = Path(__file__).parent
data_dir = BASE / "data"
data_dir.mkdir(exist_ok=True)


# ==========================================================
# 配置区：所有可以调的东西集中在这里
# ==========================================================
CONFIG = {
    "start": "20250101",
    "end": "20251017",
    "max_stocks": 10,      # 先跑 10 只；明天/接口稳定后改成 None（全量 300）
    "sleep_sec": 0.3,
}


def log(msg):
    """统一日志格式，带时间戳。"""
    print(f"[{datetime.now():%H:%M:%S}] {msg}")


# ==========================================================
# ① 名单
#   读本地 data/hs300_constituents.csv。
#   如果文件不存在，再用 ak.index_stock_cons_csindex 拉一次并存盘。
#   提示：
#     - 代码列用 dtype={"代码": str}
#     - 按 CONFIG["max_stocks"] 截断（None 表示不截）
# ==========================================================

def load_constituents():
    # TODO ①
    try:
        名单 = pd.read_csv(data_dir/"hs300_constituents.csv", encoding="utf-8", dtype={"代码": str})
    except Exception:
        log("本地名单不存在，尝试从接口拉取")
        try:
            原始 = ak.index_stock_cons_csindex(symbol="000300")
            名单 = pd.DataFrame({
                "代码": 原始["成分券代码"].astype(str).str.zfill(6),
                "名称": 原始["成分券名称"],
                "交易所": 原始["交易所"],
            })
            名单.to_csv(data_dir/"hs300_constituents.csv", index=False, encoding="utf-8-sig")
        except Exception as e2:
            log(f"中证接口失败：{e2}")
            return None
    return 名单



# ==========================================================
# ② 日线
#   对每只代码调用 fetchers.fetch_daily
#   加 sleep、进度打印、失败清单
#   返回 (大表, 失败清单)
#   提示：这段逻辑你昨天在 day21 写过，直接搬过来整理成函数
# ==========================================================


# TODO ②
def fetch_daily_all(codes):
    成功=[]
    失败清单=[]
    for i,code in enumerate(codes,start=1):
        try:
            data=fetch_daily(code,CONFIG["start"],CONFIG["end"])
            if data is not None:
                成功.append(data)
                print(f"{i}/{len(codes)} {code} {len(data)}行")
            else:
                失败清单.append({"代码": code, "原因": "拉取失败（返回 None)"})
        except Exception as e:
            失败清单.append({"代码":code,"原因":str(e)})
            print(f"{i}/{len(codes)} {code} 异常")
        time.sleep(CONFIG["sleep_sec"])
    大表=pd.concat(成功, ignore_index=True) if 成功 else pd.DataFrame()
    return 大表, 失败清单




# ==========================================================
# ③ 清洗
#   日线：
#     - 代码补 6 位、日期转类型
#     - 数值列 to_numeric(errors="coerce")
#     - 按 ["股票代码", "日期"] 排序
#     - 按 ["股票代码", "日期"] 查重
#   返回清洗后的表
# ==========================================================

def clean_daily(df):
    # TODO ③
    df["股票代码"]=df["股票代码"].astype(str).str.zfill(6)
    df["日期"]=pd.to_datetime(df["日期"])
    

    日线数值列= ["开盘", "最高", "最低", "收盘", "成交量", "成交额", "流通股本", "换手率"]
    for col in 日线数值列:
        df[col]=pd.to_numeric(df[col], errors="coerce")

    df=df.sort_values(["股票代码", "日期"])
    df=df.drop_duplicates(subset=["股票代码", "日期"])
    return df

# ==========================================================
# ④ 落盘
#   save(df, "daily") → data/clean_daily.csv
#   同时打印行数和列数，让你知道存了什么
# ==========================================================

def save(df, name):
    # TODO ④
    out=data_dir/f"clean_{name}.csv"
    df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"已存 {out}：{df.shape[0]} 行 × {df.shape[1]} 列")


# ==========================================================
# ⑤ 主流程
#   把 ①→②→③→④ 串起来，每步打一条日志。
#   任何一步失败，后面的步骤不执行，并明确告诉你是哪一步。
# ==========================================================

def main():
    # TODO ⑤
    log("加载名单")
    名单=load_constituents()
    if 名单 is None:
        log("名单加载失败，停止加载")
        return

    if CONFIG["max_stocks"]:        # 先跑 10 只
        名单 = 名单.head(CONFIG["max_stocks"])
    log(f"名单 {len(名单)} 只")

    log("拉日线")
    日线, 失败 = fetch_daily_all(名单["代码"].tolist())
    if 日线.empty:
        log("日线全失败，停止")
        return
    log(f"日线 {len(日线)} 行，失败 {len(失败)} 只")

    log("清洗")
    日线 = clean_daily(日线)

    log("落盘")
    save(日线, "daily")

if __name__ == "__main__":
    main()


# ==========================================================
# 明天（10.24 周六）补：
#   ⑥ 估值：fetch_valuation_all(codes)（百度，逐只三指标）
#   ⑦ 合并：名单 + 估值 → clean_valuation.csv / 主表
#   ⑧ 数据质量报告：复用 day23 的写法
#   ⑨ 健壮性：已存在的文件是否跳过、连跑两次是否正常
# ==========================================================
