"""把历史 EP、BP 加入因子面板，并生成三因子得分。"""

import pandas as pd

from build_roe_panel import assign_quintiles, winsorize, zscore
from config import OUTPUT_DIR

def load_inputs():
    """读取两因子面板和历史 PE/PB。"""
    factor_panel = pd.read_csv(
        OUTPUT_DIR / "factor_panel.csv",
        dtype={"股票代码": str},
    )
    valuation = pd.read_csv(
        OUTPUT_DIR / "historical_valuation.csv",
        dtype={"股票代码": str},
    )
    return factor_panel, valuation

def build_three_factor_panel():
    """构造 EP、BP、价值综合分和三因子总分。"""
    factor_panel, valuation = load_inputs()

    panel = factor_panel.merge(
        valuation[
            ["month", "股票代码", "市盈率(TTM)", "市净率"]
        ],
        on=["month", "股票代码"],
        how="left",
    )

    assert panel["市盈率(TTM)"].notna().all()
    assert panel["市净率"].notna().all()

    panel["EP"] = 1 / panel["市盈率(TTM)"].where(
        panel["市盈率(TTM)"] != 0
    )
    panel["BP"] = 1 / panel["市净率"].where(
        panel["市净率"] > 0
    )

    for source, prefix in [
        ("EP", "EP"),
        ("BP", "BP"),
    ]:
        panel[f"{prefix}_winsorized"] = (
            panel.groupby("month")[source].transform(winsorize)
        )

    for prefix in ["EP", "BP"]:
        panel[f"{prefix}_z"] = (
            panel.groupby("month")[f"{prefix}_winsorized"]
            .transform(zscore)
        )

    panel["value_z"] = (
        panel["EP_z"] + panel["BP_z"]
    ) / 2

    panel["score"] = (
        panel["momentum_z"]
        + panel["ROE_z"]
        + panel["value_z"]
    ) / 3

    panel["group"] = panel.groupby("month")["score"].transform(
        assign_quintiles
    )

    assert not panel.duplicated(["month", "股票代码"]).any()
    assert panel["value_z"].notna().all()
    assert panel["score"].notna().all()

    return panel

def main():
    """运行三因子面板并保存。"""
    panel = build_three_factor_panel()

    print("三因子面板：", panel.shape)
    print("月份数：", panel["month"].nunique())
    print("主键重复数：", panel.duplicated(
        ["month", "股票代码"]
    ).sum())

    print("\n分组数量：")
    print(panel.groupby("group", observed=True).size().to_string())

    output_path = OUTPUT_DIR / "factor_panel_3factor.csv"
    panel.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
    )
    print("\n已保存：", output_path)


if __name__ == "__main__":
    main()
