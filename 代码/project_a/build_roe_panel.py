"""合并 point-in-time ROE，完成因子标准化和五分组。"""

import pandas as pd

from config import OUTPUT_DIR, SOURCE_DATA_DIR


def load_inputs():
    """读取动量面板、年度财务数据和行业映射。"""
    momentum = pd.read_csv(
        OUTPUT_DIR / "momentum_12_1_panel.csv",
        dtype={"股票代码": str},
        parse_dates=["signal_date"],
    )
    financial = pd.read_csv(
        SOURCE_DATA_DIR / "clean_financial.csv",
        dtype={"股票代码": str},
        parse_dates=["报告期", "可用日"],
    )
    valuation = pd.read_csv(
        SOURCE_DATA_DIR / "clean_valuation.csv",
        dtype={"代码": str},
    )
    return momentum, financial, valuation


def add_latest_roe(momentum, financial):
    """为每个信号日匹配当时已披露的最新 ROE。"""
    financial = (
        financial[
            ["股票代码", "报告期", "可用日", "净资产收益率(%)"]
        ]
        .rename(
            columns={
                "报告期": "roe_report_period",
                "可用日": "roe_available_date",
                "净资产收益率(%)": "ROE",
            }
        )
        .sort_values(["roe_available_date", "股票代码"])
    )

    panel = pd.merge_asof(
        momentum.sort_values(["signal_date", "股票代码"]),
        financial,
        left_on="signal_date",
        right_on="roe_available_date",
        by="股票代码",
        direction="backward",
    )
    assert (
        panel["roe_available_date"] <= panel["signal_date"]
    ).all()
    return panel


def winsorize(series, lower_q=0.01, upper_q=0.99):
    """按给定分位数限制极端值。"""
    return series.clip(
        lower=series.quantile(lower_q),
        upper=series.quantile(upper_q),
    )


def zscore(series):
    """计算横截面标准化分数。"""
    std = series.std(ddof=0)
    if pd.isna(std) or std == 0:
        return pd.Series(0.0, index=series.index)
    return (series - series.mean()) / std


def assign_quintiles(series):
    """按分数排序并分成五组，Q5 为最高组。"""
    return pd.qcut(
        series.rank(method="first"),
        q=5,
        labels=["Q1", "Q2", "Q3", "Q4", "Q5"],
    )


def build_factor_panel():
    """构造包含 ROE、标准化得分和分组的完整因子面板。"""
    momentum, financial, valuation = load_inputs()
    panel = add_latest_roe(momentum, financial)

    industry = valuation[["代码", "行业"]].rename(
        columns={"代码": "股票代码"}
    )
    panel = panel.merge(industry, on="股票代码", how="left")

    for source, prefix in [
        ("momentum_12_1", "momentum"),
        ("ROE", "ROE"),
    ]:
        panel[f"{prefix}_winsorized"] = (
            panel.groupby("month")[source].transform(winsorize)
        )

    for prefix in ["momentum", "ROE"]:
        panel[f"{prefix}_z"] = (
            panel.groupby("month")[f"{prefix}_winsorized"]
            .transform(zscore)
        )

    panel["score"] = (panel["momentum_z"] + panel["ROE_z"]) / 2
    panel["group"] = panel.groupby("month")["score"].transform(
        assign_quintiles
    )

    assert not panel.duplicated(["month", "股票代码"]).any()
    assert panel["行业"].notna().all()
    assert panel["score"].notna().all()
    return panel.reset_index(drop=True)


def calculate_group_returns(panel):
    """计算每月 Q1-Q5 和各月股票池的等权收益。"""
    group_returns = (
        panel.groupby(["month", "group"], observed=True)["future_return"]
        .mean()
        .unstack()
    )
    benchmark = panel.groupby("month")["future_return"].mean()
    return group_returns, benchmark


def main():
    """运行因子构造、检查并保存结果。"""
    panel = build_factor_panel()
    group_returns, benchmark = calculate_group_returns(panel)

    print("因子面板：", panel.shape)
    print("月份数：", panel["month"].nunique())
    print("主键重复数：", panel.duplicated(["month", "股票代码"]).sum())
    print("\n分组记录数：")
    print(panel.groupby("group", observed=True).size().to_string())
    print("\n分组收益（%）：")
    print((group_returns * 100).round(2).to_string())
    print("\n股票池等权收益（%）：")
    print((benchmark * 100).round(2).to_string())

    OUTPUT_DIR.mkdir(exist_ok=True)
    panel.to_csv(
        OUTPUT_DIR / "factor_panel.csv",
        index=False,
        encoding="utf-8-sig",
    )
    group_returns.to_csv(
        OUTPUT_DIR / "group_returns.csv",
        encoding="utf-8-sig",
    )
    print("\n因子面板和分组收益已保存。")


if __name__ == "__main__":
    main()
