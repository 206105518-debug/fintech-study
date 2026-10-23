# day23_clean.py ｜ 2026.10.23 周五：统一字段、查重、缺失体检
#
# 运行方式：
#   cd 金融科技学习/代码/week04
#   python3 day23_clean.py
#
# 今天把三张表洗成「可以直接拿去用」的版本：
#   名单：hs300_constituents.csv（300 只）
#   日线：daily_batch.csv（10 只 × 约 190 天）
#   估值：valuation_10.csv（10 只）
#
# 输出：
#   data/clean_constituents.csv
#   data/clean_daily.csv
#   data/clean_valuation.csv
#   data/data_quality_report.csv
#
# 为什么值得单独用一天做清洗：
#   脏数据不会报错，它只会让结论悄悄错掉。
#   今天的每一道检查，都是为了把「看不见的问题」变成「看得见的数字」。

from pathlib import Path

import pandas as pd

BASE = Path(__file__).parent
data_dir = BASE / "data"

# 三张表的主键（查重用）
KEYS = {
    "名单": ["代码"],
    "日线": ["股票代码", "日期"],
    "估值": ["代码"],
}



# ==========================================================
# 题 1  读进来，看它们长什么样
#   三张表都读（代码列用 dtype=str 保住前导零）
#   对每张表打印：shape、columns、dtypes
#   动手：写个循环，一次性打印三张表的概况
# ==========================================================

# TODO 1
名单=pd.read_csv(data_dir/"hs300_constituents.csv", encoding="utf-8", dtype={"代码":str})
日线=pd.read_csv(data_dir/"daily_batch.csv", encoding="utf-8", dtype={"股票代码":str})
估值=pd.read_csv(data_dir/"valuation_10.csv",encoding="utf-8", dtype={"代码":str})

表名={"名单":名单,"日线":日线,"估值":估值}
for 名, 表 in 表名.items():
    print(f"{名}概况")
    print("shape",表.shape)
    print("columns", 表.columns.tolist())
    print(表.dtypes)
    print()
# ==========================================================
# 题 2  统一字段（三件事）
#   a) 代码补成 6 位：.astype(str).str.zfill(6)
#   b) 日期转时间类型：pd.to_datetime
#   c) 数值列统一：pd.to_numeric(errors="coerce")
#      —— 注意「市盈率TTM」可能有负值，不要一律当错误
#   动手：三张表都处理一遍，处理完再打印一次 dtypes
# ==========================================================

# TODO 2
名单["代码"]=名单["代码"].astype(str).str.zfill(6)
日线["股票代码"]=日线["股票代码"].astype(str).str.zfill(6)
日线["日期"]=pd.to_datetime(日线["日期"])
估值["代码"]=估值["代码"].astype(str).str.zfill(6)

估值数值列=["总市值","市盈率TTM","市净率"]
for col in 估值数值列:
    估值[col]=pd.to_numeric(估值[col], errors="coerce")

日线数值列= ["开盘", "最高", "最低", "收盘", "成交量", "成交额", "流通股本", "换手率"]

for col in 日线数值列:
    日线[col]=pd.to_numeric(日线[col], errors="coerce")

print(估值.dtypes)
print()
print(日线.dtypes)
print()
# ==========================================================
# 题 3  查重（按主键，不是按整行）
#   df.duplicated(subset=KEYS[表名]).sum()
#   为什么按主键而不是整行：
#     日线里「同一只股票同一天」只能有一条，哪怕其他列有细微差别也算重复。
#   动手：三张表各查一次，打印重复条数
#   自查：都应该是 0
# ==========================================================

# TODO 3
重复1=名单.duplicated(subset=KEYS["名单"]).sum()
重复2=估值.duplicated(subset=KEYS["估值"]).sum()
重复3=日线.duplicated(subset=KEYS["日线"]).sum()
print(重复1)
print(重复2)
print(重复3)
print()
# ==========================================================
# 题 4  缺失体检
#   对每张表：
#     a) 每列缺几个
#     b) 只打印「有缺失」的列（全 0 的列不用看）
#   动手：三张表都出一份
#   提示：可以写个小循环，用 df.isna().sum() 再筛 >0
# ==========================================================

# TODO 4
表名={"名单":名单,"日线":日线,"估值":估值}
for 名, 表 in 表名.items():
    缺失=表.isna().sum()
    缺失列数=int((表.isna().sum()>0).sum())
    print(f"{名}有缺失的列: ")
    print(缺失列数)
print()
# ==========================================================
# 题 5  跨表一致性检查（今天最有价值的一段）
#   a) 覆盖率：
#        日线覆盖了几只 = df_daily["股票代码"].nunique() / 名单 300
#        估值覆盖了几只 = df_val["代码"].nunique() / 名单 300
#      （现在只有 10 只，是正常的——本周只拉了 10 只）
#   b) 日期范围：日线的 min / max
#   c) 每只股票的行数：groupby("股票代码").size()
#      如果出现 185 和 190 并存，说明有停牌
#   d) 停牌天数：(df_daily["成交量"] == 0).sum()
#   动手：四项都打印出来
# ==========================================================

# TODO 5
日线覆盖率= 日线["股票代码"].nunique() / len(名单)
估值覆盖率 = 估值["代码"].nunique() / len(名单) 
print(f"日线覆盖率{日线覆盖率*100:.2f}%")
print(f"估值覆盖率{估值覆盖率*100:.2f}%")

日线=日线.sort_values("日期")
print(日线["日期"].iloc[0])
print(日线["日期"].iloc[-1])

行数=日线.groupby("股票代码").size()
print(行数)

停牌天数=(日线["成交量"] == 0).sum()
print(停牌天数)
# ==========================================================
# 主菜  写 clean_all()，输出三张干净表 + 一份质量报告
#   要求：
#     1) 清洗逻辑抽成函数（题 1-4 的步骤）
#     2) 输出 clean_constituents.csv / clean_daily.csv / clean_valuation.csv
#     3) 生成 data_quality_report.csv，至少包含这些列：
#          表名 / 行数 / 列数 / 主键重复数 / 有缺失的列数
#   写完跑一次，打印这份报告。
#
#   这份报告就是你的「数据体检单」：
#   以后每跑一次管道，看一眼它就知道数据有没有变脏。
# ==========================================================

# TODO 主菜
def clean_all():
    名单=pd.read_csv(data_dir/"hs300_constituents.csv", encoding="utf-8", dtype={"代码":str})
    日线=pd.read_csv(data_dir/"daily_batch.csv", encoding="utf-8", dtype={"股票代码":str})
    估值=pd.read_csv(data_dir/"valuation_10.csv",encoding="utf-8", dtype={"代码":str})

    名单["代码"]=名单["代码"].astype(str).str.zfill(6)
    日线["股票代码"]=日线["股票代码"].astype(str).str.zfill(6)
    日线["日期"]=pd.to_datetime(日线["日期"])
    估值["代码"]=估值["代码"].astype(str).str.zfill(6)

    估值数值列=["总市值","市盈率TTM","市净率"]
    for col in 估值数值列:
        估值[col]=pd.to_numeric(估值[col], errors="coerce")

    日线数值列= ["开盘", "最高", "最低", "收盘", "成交量", "成交额", "流通股本", "换手率"]
    for col in 日线数值列:
        日线[col]=pd.to_numeric(日线[col], errors="coerce")

    名单.to_csv(data_dir / "clean_constituents.csv", index=False, encoding="utf-8-sig")
    日线.to_csv(data_dir / "clean_daily.csv", index=False, encoding="utf-8-sig")
    估值.to_csv(data_dir / "clean_valuation.csv", index=False, encoding="utf-8-sig")
    
    报告=[]
    表名={"名单":名单,"日线":日线,"估值":估值}
    for 名, 表 in 表名.items():
        缺失列数=int((表.isna().sum()>0).sum())
        报告.append({
            "表名":名,
            "行数":len(表),
            "列数":表.shape[1],
            "主键重复数":int(表.duplicated(subset=KEYS[名]).sum()),
            "有缺失的列数":缺失列数
        })
    return pd.DataFrame(报告)

报告 = clean_all()
报告.to_csv(data_dir / "data_quality_report.csv", index=False, encoding="utf-8-sig")
print("=== 数据质量报告 ===")
print(报告.to_string(index=False))
# ==========================================================
# 收尾
#   1) 记住：查重按主键、缺失只列有问题的列、覆盖率要报
#   2) 明天（10.24 周六）：把五段串成 pipeline.py，一条命令跑完
#   3) 提交推送
# ==========================================================
