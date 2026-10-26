# day24_sql_intro.py ｜ 2026.10.26 周一：SQL 入门
#
# 运行方式：
#   cd 金融科技学习/代码/week05
#   python3 day24_sql_intro.py
#
# 今天为什么先在本机跑：
#   SQL 和 pandas 解决的是同一类问题——从表里取数、筛选、汇总。
#   你在本机用 sqlite3 就能跑，写完立刻看到结果，
#   比在网页上一题一题提交反馈快得多。
#
#   sqlite3 是 Python 自带的数据库，不用安装。今天建的是一个「内存数据库」，
#   程序结束就没了——重点是练 SQL 语法，不是存数据。

import sqlite3
from pathlib import Path

import pandas as pd

BASE = Path(__file__).parent
csv_path = BASE.parent / "week04" / "data" / "clean_valuation.csv"

# 上周做好的估值表，10 只股票
估值 = pd.read_csv(csv_path, dtype={"代码": str})


# ==========================================================
# 题 0  建库：把 DataFrame 变成一张 SQL 表
#   conn = sqlite3.connect(":memory:")       建一个内存数据库
#   估值.to_sql("stocks", conn, index=False, if_exists="replace")
#       把 DataFrame 写进表 stocks
#   写一个查询函数，省得每次都重复三行：
#     def q(sql):
#         return pd.read_sql_query(sql, conn)
#   动手：建库 + 建函数，然后 q("SELECT * FROM stocks") 看一眼
# ==========================================================

# TODO 0


# ==========================================================
# 题 1  最基本的查询：SELECT
#   a) 取全部列：SELECT * FROM stocks
#   b) 只取三列：SELECT 代码, 名称, 总市值 FROM stocks
#   c) 取前 3 行：... LIMIT 3
#   对比 pandas：df[["代码","名称","总市值"]] 就是同一个意思。
#   SQL 里用 SELECT 指定「要哪几列」，用 FROM 指定「从哪张表」。
# ==========================================================

# TODO 1


# ==========================================================
# 题 2  筛选：WHERE
#   a) 总市值大于 1000：WHERE 总市值 > 1000
#   b) 市盈率大于 0 且小于 20：WHERE "市盈率TTM" > 0 AND "市盈率TTM" < 20
#   c) 交易所是 SZ：WHERE 交易所 = 'SZ'
#   d) 名称里含「银行」：WHERE 名称 LIKE '%银行%'
#   注意：字符串用单引号；列名里有特殊字符时用双引号包住。
#   对比 pandas：df[df["总市值"] > 1000] 是同一个意思。
# ==========================================================

# TODO 2


# ==========================================================
# 题 3  排序与取前几名：ORDER BY + LIMIT
#   a) 按总市值从大到小：ORDER BY 总市值 DESC
#   b) 取前 5 名：... LIMIT 5
#   c) 按市盈率从小到大：ORDER BY "市盈率TTM" ASC
#   对比 pandas：df.sort_values("总市值", ascending=False).head(5)
# ==========================================================

# TODO 3


# ==========================================================
# 题 4  聚合：COUNT / AVG / MAX / MIN
#   a) 一共几只：SELECT COUNT(*) FROM stocks
#   b) 平均市值：SELECT AVG(总市值) FROM stocks
#   c) 最大、最小市盈率：SELECT MAX("市盈率TTM"), MIN("市盈率TTM") FROM stocks
#   d) 给结果改名字：SELECT AVG(总市值) AS 平均市值 FROM stocks
#   对比 pandas：df["总市值"].mean()
# ==========================================================

# TODO 4


# ==========================================================
# 题 5  分组：GROUP BY
#   a) 每个交易所有几只：SELECT 交易所, COUNT(*) FROM stocks GROUP BY 交易所
#   b) 每个交易所的平均市值：SELECT 交易所, AVG(总市值) AS 平均市值
#                            FROM stocks GROUP BY 交易所
#   c) 排序：在 GROUP BY 后面加 ORDER BY 平均市值 DESC
#   对比 pandas：df.groupby("交易所")["总市值"].mean()
#   **这就是你上周学的 groupby，换了个语法。**
# ==========================================================

# TODO 5


# ==========================================================
# 主菜  用 SQL 回答五个业务问题
#   每个问题写成一句 SQL，跑出结果，并把答案写在注释里：
#     1) 总市值最大的股票是哪只？
#     2) 市盈率最低的「正 PE」股票是哪只？（排除亏损）
#     3) 亏损的公司有几家？
#     4) 深市（SZ）和沪市（SH）的平均市值各是多少？
#     5) 市值前 3 名的公司，平均市盈率是多少？
#        提示：先用子查询筛出前 3 名，再在外层算平均：
#          SELECT AVG("市盈率TTM") FROM (
#              SELECT "市盈率TTM" FROM stocks ORDER BY 总市值 DESC LIMIT 3
#          )
#   这五题覆盖了 SELECT / WHERE / ORDER BY / LIMIT / 聚合 / 子查询。
# ==========================================================

# TODO 主菜


# ==========================================================
# 收尾
#   1) 记住：SELECT 选列、WHERE 筛行、GROUP BY 分组、ORDER BY 排序
#   2) 去牛客网 SQL 篇做 5 道同类型题，把语法迁移到陌生数据上
#   3) 提交推送
# ==========================================================
