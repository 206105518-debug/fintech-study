# day19_akshare_intro.py ｜ 2026.10.19 周一：akshare 入门 + 拉沪深300成分股
#
# 运行方式：
#   cd 金融科技学习/代码/week04
#   python3 day19_akshare_intro.py
#
# 今天要完成三件事：
#   1) 装好 akshare（一个免费的数据接口库，A股行情/指数/财务数据都能拉）
#   2) 拉到沪深300的成分股名单
#   3) 把名单清洗好、存成本地 CSV
#
# 为什么从成分股名单开始：
#   它是整条数据管道的入口。后面要拉的日线、市值、估值，
#   都要按这份名单里的代码去循环请求。名单错了，后面全错。

try:
    import akshare as ak
    print(f"akshare 版本：{ak.__version__}")
    import numpy as np
    import pandas as pd
    from pathlib import Path
except ImportError:
    print("还没装 akshare，先在终端运行：")
    print("  python3 -m pip install akshare --upgrade")
    raise SystemExit

print()

# ==========================================================
# 题 1  第一次调用：把沪深300成分股拉下来
#   akshare 里有两个常用接口：
#     ak.index_stock_cons_csindex(symbol="000300")   中证指数官网
#     ak.index_stock_cons(symbol="000300")           新浪
#   先试第一个，报错就换成第二个。
#   动手：调用一次，打印三样东西：
#     df.shape      —— 多少行多少列（沪深300应该是 300 行左右）
#     df.columns    —— 有哪些列（不同接口列名不一样，先看清）
#     df.head()     —— 前 5 行长什么样
#
#   ⚠️ 网络请求可能失败（接口限流、网络不通），这时候先把报错原文看清楚，
#      别急着改代码。很可能是网络问题，不是你的问题。
# ==========================================================

# TODO 1
df=ak.index_stock_cons_csindex(symbol="000300")
print(f"行和列分别是{df.shape}")
print(f"列名有{df.columns}")
#列名有Index(['日期', '指数代码', '指数名称', '指数英文名称', '成分券代码',
# '成分券名称', '成分券英文名称', '交易所','交易所英文名称'],
print(f"前五行是{df.head(5)}")
print()
# ==========================================================
# 题 2  看懂这份数据
#   不管接口返回什么列，先回答四个问题：
#     a) 哪一列是股票代码？哪一列是名称？
#     b) 代码是 6 位字符串，还是被当成数字了？
#        （这是你从 day12 起就反复踩的坑：000858 不能变成 858）
#     c) 有没有重复的股票？
#     d) 有没有缺失？
#   动手：用 pandas 检查一遍，把结果打印出来。
#   提示：
#     df["某列"].nunique()        有几个不重复的值
#     df.duplicated().sum()       有几行重复
#     df.isna().sum()             每列缺几个
# ==========================================================

# TODO 2
print(df[["成分券代码","成分券名称"]])
print(f"成分券代码的类型为{df["成分券代码"].dtype}") #str
print(f"重复的股票有{df["成分券代码"].duplicated().sum()}")
print(f"缺失了{df["成分券代码"].isna().sum()}")
print()
# ==========================================================
# 题 3  清洗成一张能用的名单
#   目标：得到三列 —— 代码（6 位字符串）、名称、交易所
#   规则（A股的交易所后缀）：
#     60 开头 → 上交所，后缀 .SH
#     68 开头 → 科创板，后缀 .SH
#     00 开头 → 深交所，后缀 .SZ
#     30 开头 → 创业板，后缀 .SZ
#   做法提示：
#     code = df["代码列"].astype(str).str.zfill(6)     ← zfill 补足 6 位
#     df["交易所"] = np.where(code.str.startswith(("60", "68")), "SH", "SZ")
#   动手：清洗完打印前 10 行，确认代码是 6 位、交易所标注正确
#   为什么必须补足 6 位：接口有时会把 "000858" 读成 858，
#   拿到手先 zfill，比事后 debug 便宜得多。
# ==========================================================

# TODO 3
code=df["成分券代码"].astype(str).str.zfill(6)
df["交易所"] = np.where(code.str.startswith(("60", "68")), "SH", "SZ")
print("前十行代码")
print(code.head(10))
print("前十行交易所名称")
print(df["交易所"].head(10))
print()


# ==========================================================
# 题 4  存成本地文件
#   存到 代码/week04/data/hs300_constituents.csv
#   两个参数：index=False，encoding="utf-8-sig"
#   动手前先建目录（Python 里也能建）：
#     BASE = Path(__file__).parent
#     data_dir = BASE / "data"
#     data_dir.mkdir(exist_ok=True)
#   动手：存完用 ls 看一眼文件是否真的出现，再读回来确认能读
# ==========================================================

# TODO 4
BASE = Path(__file__).parent
data_dir = BASE / "data"
data_dir.mkdir(exist_ok=True)
名单 = df[["成分券代码", "成分券名称", "交易所"]].copy()
名单["成分券代码"] = 名单["成分券代码"].astype(str).str.zfill(6)
名单 = 名单.rename(columns={"成分券代码": "代码", "成分券名称": "名称"})
名单.to_csv(data_dir / "hs300_constituents.csv", index=False, encoding="utf-8-sig")


# ==========================================================
# 主菜  封装成 fetch_hs300()
#   要求：
#     1) 优先用 csindex 接口，失败就自动退回 index_stock_cons
#     2) 返回清洗好的 DataFrame（代码 / 名称 / 交易所）
#     3) 任何异常都打印一句人话，并返回 None，不要让整个脚本崩掉
#     4) 调用它，存盘，打印「共 X 只股票」
#   为什么要做降级：
#     免费接口最常见的故障就是「今天这个源不通」，写好备用路径，
#     你的管道才不会因为一个接口挂掉就整个停摆。
#     这就是「健壮性」在数据工程里的具体样子。
# ==========================================================

# TODO 主菜
def fetch_hs300():
    try:
        df=ak.index_stock_cons_csindex(symbol="000300")
    except Exception as e:
        print(f"csindex接口失败：{e},退回新浪")
        try:
            df=ak.index_stock_cons(symbol="000300")
        except Exception as e2:
            print(f"新浪接口失败：{e2}")
            return None
    print(df.columns)
    code=df["成分券代码"].astype(str).str.zfill(6)
    df["交易所"] = np.where(code.str.startswith(("60", "68")), "SH", "SZ")
    名单 = df[["成分券代码", "成分券名称", "交易所"]].copy()
    名单["成分券代码"] = 名单["成分券代码"].astype(str).str.zfill(6)
    名单 = 名单.rename(columns={"成分券代码": "代码", "成分券名称": "名称"})
    return 名单

df=fetch_hs300()
if df is not None:
    df.to_csv(data_dir / "hs300_constituents.csv", index=False, encoding="utf-8-sig")
    print(f"共 {len(df)} 只股票")

# ==========================================================
# 收尾
#   1) 记住：名单是管道的入口，代码必须补足 6 位
#   2) 明天（10.20）：按名单拉日线行情
#   3) 提交推送
# ==========================================================

