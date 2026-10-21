# day21_batch_fetch.py ｜ 2026.10.21 周三：批量拉取 + 限流 + 失败清单
#
# 运行方式：
#   cd 金融科技学习/代码/week04
#   python3 day21_batch_fetch.py
#
# 今天的目标不是「拉得多」，是「拉得稳」：
#   10 只里坏 1 只，剩下 9 只必须照常跑完，
#   并且告诉你坏的是哪一只、为什么。
#
#   这就是「脚本」和「管道」的分界：
#     脚本：一只失败，整个崩掉
#     管道：一只失败，记下来，继续跑

import time
from pathlib import Path

import pandas as pd

from fetchers import fetch_daily

BASE = Path(__file__).parent
data_dir = BASE / "data"
data_dir.mkdir(exist_ok=True)

START, END = "20250101", "20251017"


# ==========================================================
# 题 1  从名单里取前 10 只
#   读 data/hs300_constituents.csv，dtype={"代码": str} 别忘了
#   取前 10 行，打印代码和名称
# ==========================================================

# TODO 1
df=pd.read_csv(data_dir/"hs300_constituents.csv", dtype={"代码": str})
print(df[["代码","名称"]].head(10))
print()
# ==========================================================
# 题 2  循环拉取（先写最朴素的一版）
#   对 10 只代码逐个调用 fetch_daily(code, START, END)
#   成功的 DataFrame 收进一个列表
#   每拉完一只打印进度：「3/10 600036 招商银行 190 行」
#   为什么要打印进度：批量任务动辄几分钟，
#   没有进度你分不清是「还在跑」还是「卡死了」
# ==========================================================

# TODO 2
codes=df.head(10)["代码"].tolist()
s=[]
for i,code in enumerate(codes,start=1):
    data=fetch_daily(code,START, END)
    if data is not None:
        s.append(data)
        print(f"{i}/{len(codes)} {code} {len(data)}行")
print()
# ==========================================================
# 题 3  加限流与失败清单（今天的核心）
#   a) 每只之间 time.sleep(0.3)，别把接口当自家服务器
#   b) 用 try/except 包住每一次调用：
#      有了它，某一只抛异常也不会中断整个循环
#   c) 失败的记下来：失败.append({"代码": code, "原因": str(e)})
#
#   注意 fetch_daily 有两种失败方式，都要接住：
#     返回 None  → 记一笔「拉取失败」
#     抛出异常    → 记一笔异常信息
#   这就是防御性编程的两层：函数内部兜一次，调用处再兜一次。
# ==========================================================

# TODO 3
codes=df.head(10)["代码"].tolist()
成功=[]
失败=[]

for i,code in enumerate(codes,start=1):
    try:
        data=fetch_daily(code,START,END)
        if data is not None:
            成功.append(data)
            print(f"{i}/{len(codes)} {code} {len(data)}行")
        else:
            失败.append({"代码": code, "原因": "拉取失败（返回 None)"})
    except Exception as e:
        失败.append({"代码":code,"原因":str(e)})
        print(f"{i}/{len(codes)} {code} 异常")
    time.sleep(0.3)
print()
# ==========================================================
# 题 4  把成功的拼成一张大表
#   pd.concat(成功的数据列表, ignore_index=True)
#   然后检查三件事：
#     a) 总行数
#     b) 每只股票各自多少行：df.groupby("股票代码").size()
#     c) 有没有重复：df.duplicated(subset=["股票代码", "日期"]).sum()
#   为什么要查重复：重跑时如果追加而不覆盖，
#   同一天就会出现两条记录
# ==========================================================

# TODO 4

table=pd.concat(成功, ignore_index=True)
print(f"总行数为{len(table)}")
print(f"每只股票行为{table.groupby('股票代码').size()}")
print(table.duplicated(subset=["股票代码", "日期"]).sum())
# ==========================================================
# 题 5  存盘 + 出报告
#   a) 大表存成 data/daily_batch.csv
#   b) 打印总结：成功 X 只、失败 Y 只、共 Z 行
#   c) 有失败就打印失败清单
#   验收标准：不管几只失败，脚本都要跑到底并给出这份总结
# ==========================================================

# TODO 5
table.to_csv(data_dir/"daily_batch.csv", index=False, encoding="utf-8-sig")
print(f"成功了{len(成功)}只，失败了{len(失败)}只，共{len(table)}行")
if 失败:
    print("失败清单：")
    for item in 失败:
        print(f"{item['代码']}:{item['原因']}")
# ==========================================================
# 主菜  封装成 fetch_many()
#   def fetch_many(codes, start, end, sleep_sec=0.3):
#       返回 (成功的大表, 失败清单)
#   要求：
#     1) 循环 + 限流 + 单只异常隔离
#     2) 进度打印成「3/10 …」
#     3) 失败清单是 list[dict]，每项含代码和原因
#   写完用它拉 10 只、存盘、打印总结。
#
#   为什么返回两个值：调用方需要知道「拿到了什么」和「缺了什么」。
#   真实的数据工作里，第二样往往更重要——
#   你缺的那部分会决定结论能不能用。
# ==========================================================

# TODO 主菜
def fetch_many(codes, start, end, sleep_sec=0.3):
    成功=[]
    失败=[]
    for i,code in enumerate(codes,start=1):
        try:
            data=fetch_daily(code,start,end)
            if data is not None:
                成功.append(data)
                print(f"{i}/{len(codes)} {code} {len(data)}行")
            else:
                失败.append({"代码": code, "原因": "拉取失败（返回 None)"})
        except Exception as e:
            失败.append({"代码":code,"原因":str(e)})
            print(f"{i}/{len(codes)} {code} 异常")
        time.sleep(sleep_sec)
    大表=pd.concat(成功, ignore_index=True) if 成功 else pd.DataFrame()
    return 大表, 失败

大表, 失败=fetch_many(codes, START, END)
大表.to_csv(data_dir/"daily_batch.csv", index=False, encoding="utf-8-sig")
print(f"成功了{len(codes)-len(失败)}只，失败了{len(失败)}只，共{len(大表)}行")
if 失败:
    print("失败清单：")
    for item in 失败:
        print(f"{item['代码']}:{item['原因']}")

# ==========================================================
# 收尾
#   1) 批量任务三件套 = 限流 + 异常隔离 + 失败清单
#   2) 明天（10.22）：补市值与估值
#   3) 提交推送
# ==========================================================
