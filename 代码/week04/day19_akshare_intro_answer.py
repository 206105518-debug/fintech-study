# day19_akshare_intro_answer.py ｜ 参考答案
# 注意：这份答案需要联网才能跑。如果接口报错，把报错原文发我，那多半是网络或接口变动。

from pathlib import Path
import numpy as np
import pandas as pd
import akshare as ak

BASE = Path(__file__).parent
data_dir = BASE / "data"
data_dir.mkdir(exist_ok=True)


# ---------- 题 1  第一次调用 ----------
print(f"akshare 版本：{ak.__version__}")

df = ak.index_stock_cons_csindex(symbol="000300")
print(f"形状：{df.shape}")
print(f"列名：{list(df.columns)}")
print(df.head())
print()


# ---------- 题 2  看懂数据 ----------
print("代码列示例：", df["成分券代码"].head(5).tolist())
print("代码列类型：", df["成分券代码"].dtype)
print("不重复的代码数：", df["成分券代码"].nunique())
print("重复行数：", df.duplicated().sum())
print("每列缺失：")
print(df.isna().sum())
print()


# ---------- 题 3  清洗 ----------
名单 = pd.DataFrame({
    "代码": df["成分券代码"].astype(str).str.zfill(6),
    "名称": df["成分券名称"],
})
名单["交易所"] = np.where(名单["代码"].str.startswith(("60", "68")), "SH", "SZ")
print(名单.head(10))
print()


# ---------- 题 4  存盘 ----------
out_path = data_dir / "hs300_constituents.csv"
名单.to_csv(out_path, index=False, encoding="utf-8-sig")
print(f"已保存：{out_path}")

回读 = pd.read_csv(out_path, dtype={"代码": str})
print(f"读回来：{回读.shape}，代码类型 {回读['代码'].dtype}，示例 {回读['代码'].head(3).tolist()}")
print()


# ---------- 主菜  fetch_hs300 ----------
def fetch_hs300():
    """拉沪深300成分股，返回 代码/名称/交易所 三列。

    优先用中证官网接口；失败时退回新浪接口（列名不同，需要分别处理）。
    """
    try:
        raw = ak.index_stock_cons_csindex(symbol="000300")
        out = pd.DataFrame({
            "代码": raw["成分券代码"].astype(str).str.zfill(6),
            "名称": raw["成分券名称"],
        })
    except Exception as e:
        print(f"中证接口失败（{type(e).__name__}），改用新浪接口")
        try:
            raw = ak.index_stock_cons(symbol="000300")
            out = pd.DataFrame({
                "代码": raw["品种代码"].astype(str).str.zfill(6),
                "名称": raw["品种名称"],
            })
        except Exception as e2:
            print(f"新浪接口也失败了：{type(e2).__name__}: {e2}")
            return None

    out["交易所"] = np.where(out["代码"].str.startswith(("60", "68")), "SH", "SZ")
    return out.drop_duplicates(subset="代码").reset_index(drop=True)


result = fetch_hs300()
if result is not None:
    path = data_dir / "hs300_constituents.csv"
    result.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"共 {len(result)} 只股票，已保存到 {path}")
else:
    print("今天没拉到数据，检查网络后再试")
