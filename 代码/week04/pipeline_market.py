"""名单、估值、行业和财务数据读取。"""

import time

import akshare as ak
import pandas as pd

from pipeline_config import INDICATORS, data_dir
from pipeline_state import log


def load_constituents():
    """读取沪深300名单；本地不存在时从接口获取。"""
    try:
        constituents = pd.read_csv(
            data_dir / "hs300_constituents.csv",
            encoding="utf-8",
            dtype={"代码": str},
        )
    except Exception:
        log("本地名单不存在，尝试从接口拉取")
        try:
            raw = ak.index_stock_cons_csindex(symbol="000300")
            constituents = pd.DataFrame({
                "代码": raw["成分券代码"].astype(str).str.zfill(6),
                "名称": raw["成分券名称"],
                "交易所": raw["交易所"],
            })
            constituents.to_csv(
                data_dir / "hs300_constituents.csv",
                index=False,
                encoding="utf-8-sig",
            )
        except Exception as exc:
            log(f"中证接口失败：{exc}")
            return None

    return constituents


def fetch_valuation(code):
    """获取单只股票最新的总市值、市盈率和市净率。"""
    row = {"代码": code}
    ok_count = 0

    for indicator_name, column_name in INDICATORS.items():
        try:
            data = ak.stock_zh_valuation_baidu(
                symbol=code,
                indicator=indicator_name,
                period="近一年",
            )
            data = data.sort_values("date")
            row[column_name] = float(data["value"].iloc[-1])
            ok_count += 1
        except Exception as exc:
            print(f"{code}{indicator_name}失败：{type(exc).__name__}")
            row[column_name] = None
        time.sleep(0.2)

    return row if ok_count > 0 else None


def fetch_valuation_all(codes):
    """批量获取估值，返回估值表和失败清单。"""
    rows = []
    failed = []

    for i, code in enumerate(codes, start=1):
        valuation = fetch_valuation(code)
        if valuation is None:
            failed.append({"代码": code, "原因": "三个指标均失败"})
            print(f"{i}/{len(codes)} {code} 失败")
        else:
            rows.append(valuation)
            print(f"{i}/{len(codes)} {code} 成功")
        time.sleep(0.2)

    return pd.DataFrame(rows), failed


def load_industry(constituents):
    """把申万一级行业映射合并到成分股名单。"""
    path = data_dir / "industry_map.csv"
    if not path.exists():
        log("本地没有行业映射，先运行 day25 生成")
        return constituents

    industry = pd.read_csv(path, dtype={"代码": str}, encoding="utf-8-sig")
    clean_constituents = constituents.drop(columns=["行业"], errors="ignore")
    merged = pd.merge(clean_constituents, industry, on="代码", how="left")
    coverage = merged["行业"].notna().sum()
    log(f"行业覆盖 {coverage}/{len(merged)}（{coverage / len(merged) * 100:.1f}%）")
    return merged


def load_financial():
    """读取本地财务缓存。"""
    path = data_dir / "financial_all.csv"
    if not path.exists():
        log("本地不存在财务数据，先运行 day28_financial_all.py")
        return None

    financial = pd.read_csv(path, dtype={"股票代码": str})
    log(f"财务数据 {len(financial)} 行，{financial['股票代码'].nunique()} 只")
    return financial