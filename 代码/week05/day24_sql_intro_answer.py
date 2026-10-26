# day24_sql_intro_answer.py ｜ 参考答案

import sqlite3
from pathlib import Path

import pandas as pd

BASE = Path(__file__).parent
csv_path = BASE.parent / "week04" / "data" / "clean_valuation.csv"

估值 = pd.read_csv(csv_path, dtype={"代码": str})
conn = sqlite3.connect(":memory:")
估值.to_sql("stocks", conn, index=False, if_exists="replace")


def q(sql):
    return pd.read_sql_query(sql, conn)


# ---------- 题 0  建库 ----------
print("表结构：")
print(q("PRAGMA table_info(stocks)")[["name", "type"]])
print()


# ---------- 题 1  SELECT ----------
print("全部列，前 3 行：")
print(q("SELECT * FROM stocks LIMIT 3"))

print("\n只取三列：")
print(q("SELECT 代码, 名称, 总市值 FROM stocks"))
print()


# ---------- 题 2  WHERE ----------
print("总市值 > 1000：")
print(q("SELECT 代码, 名称, 总市值 FROM stocks WHERE 总市值 > 1000"))

print("\n0 < 市盈率TTM < 20：")
print(q('SELECT 代码, 名称, "市盈率TTM" FROM stocks WHERE "市盈率TTM" > 0 AND "市盈率TTM" < 20'))

print("\n名称含「银行」：")
print(q("SELECT 代码, 名称 FROM stocks WHERE 名称 LIKE '%银行%'"))
print()


# ---------- 题 3  ORDER BY + LIMIT ----------
print("市值前 5：")
print(q("SELECT 代码, 名称, 总市值 FROM stocks ORDER BY 总市值 DESC LIMIT 5"))

print("\n市盈率从小到大：")
print(q('SELECT 代码, 名称, "市盈率TTM" FROM stocks ORDER BY "市盈率TTM" ASC'))
print()


# ---------- 题 4  聚合 ----------
print("行数 / 平均市值 / 最大最小市盈率：")
print(q('SELECT COUNT(*) AS 只数, AVG(总市值) AS 平均市值, MAX("市盈率TTM") AS 最大PE, MIN("市盈率TTM") AS 最小PE FROM stocks'))
print()


# ---------- 题 5  GROUP BY ----------
print("按交易所分组：")
print(q("SELECT 交易所, COUNT(*) AS 只数, AVG(总市值) AS 平均市值 FROM stocks GROUP BY 交易所 ORDER BY 平均市值 DESC"))
print()


# ---------- 主菜  五个问题 ----------
print("1) 市值最大的股票：")
print(q("SELECT 代码, 名称, 总市值 FROM stocks ORDER BY 总市值 DESC LIMIT 1"))

print("\n2) 最低的正市盈率：")
print(q('SELECT 代码, 名称, "市盈率TTM" FROM stocks WHERE "市盈率TTM" > 0 ORDER BY "市盈率TTM" ASC LIMIT 1'))

print("\n3) 亏损公司数：")
print(q('SELECT COUNT(*) AS 亏损家数 FROM stocks WHERE "市盈率TTM" < 0'))

print("\n4) 各交易所平均市值：")
print(q("SELECT 交易所, AVG(总市值) AS 平均市值 FROM stocks GROUP BY 交易所"))

print("\n5) 市值前 3 的平均市盈率：")
print(q('''SELECT AVG("市盈率TTM") AS 前三大平均PE FROM (
    SELECT "市盈率TTM" FROM stocks ORDER BY 总市值 DESC LIMIT 3
)'''))
