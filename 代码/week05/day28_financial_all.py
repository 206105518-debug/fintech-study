# day28_financial_all.py ｜ 2026.10.31 周六：全量财务字段
#
# 运行方式：
#   cd 金融科技学习/代码/week05
#   python3 day28_financial_all.py
#
# 今天的目标：
#   把 10 只的财务试点扩到 300 只，产出 data/financial_all.csv
#
#   规模：300 只 × 2 次请求 = 600 次，加 sleep 大约 8–12 分钟。
#   跑的时候别干等，可以去把 README 补了。

import sys
import time
from pathlib import Path

import pandas as pd

BASE = Path(__file__).parent
data_dir = BASE.parent / "week04" / "data"

# fetchers.py 在 week04，这个脚本在 week05，要把 week04 加进模块搜索路径
sys.path.append(str(BASE.parent / "week04"))
from fetchers import fetch_financial   # noqa: E402


# ==========================================================
# 题 1  读名单，取全部代码
#   读 data/constituents_with_industry.csv，取「代码」列。
#   动手：打印总数（应该是 300）
# ==========================================================

# TODO 1
表=pd.read_csv(data_dir/"constituents_with_industry.csv", encoding="utf-8", dtype={"代码":str})
代码列=表["代码"]
print(len(代码列))
# ==========================================================
# 题 2  批量拉取
#   复用昨天写过的模式：
#     - 成功 append，失败记清单（代码 + 原因）
#     - 每只 sleep(0.2)
#     - 每 20 只打印一次进度（300 只逐条打印会刷屏）
#     - 用 enumerate 算 i/总数
#   动手：先跑前 20 只验证，再全量
# ==========================================================

# TODO 2
全列=代码列.tolist()
成功=[]
失败=[]
for i,code in enumerate(全列,start=1):
    df=fetch_financial(code)
    if df is not None:
        成功.append(df)
        print(f"{i}/{len(全列)}, 代码{code}, {len(df)}期")
    else:
        失败.append(code)
        print(f"原因：拉取失败")
    time.sleep(0.2)
年报=pd.concat(成功, ignore_index=True) if 成功 else pd.DataFrame()
print(f"成功{len(成功)}只，失败{len(失败)}只，共{len(年报)}行")
print(年报["股票代码"].nunique(), "只股票")
年报.to_csv(data_dir/"financial_all.csv", encoding="utf-8-sig", index=False)
if 失败:
    pd.DataFrame(失败).to_csv(data_dir / "financial_failed.csv", index=False, encoding="utf-8-sig")
# ==========================================================
# 题 3  合并与检查
#   concat 所有成功的表，然后检查：
#     a) 总行数、股票只数（每只 6 期 → 约 1800 行）
#     b) 每只的期数分布（有没有某只少了几年）
#     c) ROE 的缺失率和范围
#     d) 营收增速的缺失率 —— 预计银行/券商那一批会缺
#   动手：四项都打印
# ==========================================================

# TODO 3


# ==========================================================
# 题 4  存盘
#   存 data/financial_all.csv，index=False、utf-8-sig
#   再存一份失败清单 data/financial_failed.csv（如果有失败）
# ==========================================================

# TODO 4


# ==========================================================
# 主菜  接进 pipeline
#   在 pipeline.py 里加 load_financial()：
#     1) 读 data/financial_all.csv（缓存，不存在就提示先跑本脚本）
#     2) 返回财务表，不在这里 merge（日线是日频、财务是年频，
#        什么时候合并由下游决定）
#   然后在 main() 里加一步日志，保存财务表到 clean_financial.csv。
#
#   注意：不要把财务表和日线在 pipeline 里 merge。
#   频率不同，怎么对齐（按可用日 + ffill）是回测阶段的事，
#   管道只负责「把干净的数据准备好」。
# ==========================================================

# TODO 主菜


# ==========================================================
# 收尾
#   1) 记录覆盖率与缺失结构（金融机构的营收增速）
#   2) 更新 README 的已知缺口
#   3) 提交推送
# ==========================================================
