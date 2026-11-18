"""比较 6-1 和 12-1 动量的覆盖范围与相关性。"""

from pathlib import Path

import pandas as pd

BASE = Path(__file__).parent
DATA_DIR = BASE / "data"

def load_momentum():
    """读取 6-1 与 12-1 动量面板。"""
    six = pd.read_csv(
        DATA_DIR / "momentum_panel.csv",
        dtype={"股票代码": str},
    )
    twelve = pd.read_csv(
        DATA_DIR / "momentum_12_1_panel.csv",
        dtype={"股票代码": str},
    )
    return six, twelve

def compare_coverage(six, twelve):
    """统计两种动量每月覆盖的股票数。"""
    six_count = (
        six.groupby("month").size().rename("momentum_6_1")
    )
    twelve_count = (
        twelve.groupby("month").size().rename("momentum_12_1")
    )
    return pd.concat(
        [six_count, twelve_count],
        axis=1,
    ).fillna(0).astype(int)

def compare_correlation(six, twelve):
    """在共同股票样本上比较两种动量。"""
    common = six[
        ["month", "股票代码", "momentum_6_1"]
    ].merge(
        twelve[
            ["month", "股票代码", "momentum_12_1"]
        ],
        on=["month", "股票代码"],
        how="inner",
    )

    rows = []
    for month, group in common.groupby("month"):
        pearson = group["momentum_6_1"].corr(
            group["momentum_12_1"]
        )
        spearman = (
            group["momentum_6_1"].rank()
            .corr(group["momentum_12_1"].rank())
        )
        rows.append({
            "month": month,
            "common_stocks": len(group),
            "pearson": pearson,
            "spearman": spearman,
        })

    return common, pd.DataFrame(rows)

def main():
    """运行比较并保存结果。"""
    six, twelve = load_momentum()

    coverage = compare_coverage(six, twelve)
    common, correlation = compare_correlation(six, twelve)

    print("每月覆盖范围：")
    print(coverage.to_string())

    print("\n共同样本相关性：")
    print(correlation.round(4).to_string(index=False))

    output_path = DATA_DIR / "momentum_comparison.csv"
    correlation.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
    )
    print("\n比较结果已保存：", output_path)


if __name__ == "__main__":
    main()