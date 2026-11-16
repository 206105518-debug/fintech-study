"""运行 Q5 组合回测：权重、换手、交易成本和扣费后收益。"""

import pandas as pd

from config import OUTPUT_DIR

ONE_WAY_COST = 0.0015


def load_factor_panel():
    """读取完整因子面板。"""
    return pd.read_csv(
        OUTPUT_DIR / "factor_panel.csv",
        dtype={"股票代码": str},
    )


def build_target_weights(panel):
    """给每个月 Q5 股票分配等权目标权重。"""
    q5 = panel[panel["group"] == "Q5"].copy()
    q5["target_weight"] = 1 / q5.groupby("month")[
        "股票代码"
    ].transform("count")

    assert not q5.duplicated(["month", "股票代码"]).any()
    assert (
        q5.groupby("month")["target_weight"]
        .sum()
        .round(10)
        .eq(1)
        .all()
    )
    return q5


def run_backtest(q5, one_way_cost=ONE_WAY_COST):
    """模拟 Q5 组合并计算换手、成本和扣费后收益。"""
    results = []
    previous_weights = None

    for month in sorted(q5["month"].unique()):
        current = q5[q5["month"] == month].set_index("股票代码")
        target_weights = current["target_weight"]

        if previous_weights is None:
            # 首次从现金建仓，买入金额约等于全部资产。
            turnover = target_weights.sum()
        else:
            universe = target_weights.index.union(previous_weights.index)
            new_aligned = target_weights.reindex(
                universe, fill_value=0
            )
            old_aligned = previous_weights.reindex(
                universe, fill_value=0
            )
            turnover = (new_aligned - old_aligned).abs().sum()

        transaction_cost = turnover * one_way_cost
        gross_return = (
            current["target_weight"] * current["future_return"]
        ).sum()
        net_return = (1 - transaction_cost) * (1 + gross_return) - 1

        results.append({
            "month": month,
            "stock_count": len(current),
            "turnover": turnover,
            "transaction_cost": transaction_cost,
            "gross_return": gross_return,
            "net_return": net_return,
        })

        # 持有期结束后，按照股票收益还原自然漂移后的权重。
        ending_value = (
            current["target_weight"] * (1 + current["future_return"])
        )
        previous_weights = ending_value / ending_value.sum()

    return pd.DataFrame(results)


def add_benchmark(results, panel):
    """加入未扣交易成本的股票池等权基准。"""
    benchmark = (
        panel.groupby("month")["future_return"]
        .mean()
        .rename("benchmark_gross_return")
    )
    results = results.join(benchmark, on="month")
    results["excess_gross_vs_benchmark"] = (
        results["gross_return"] - results["benchmark_gross_return"]
    )
    results["excess_net_vs_gross_benchmark"] = (
        results["net_return"] - results["benchmark_gross_return"]
    )
    return results


def main():
    """运行回测、打印结果并保存 CSV。"""
    panel = load_factor_panel()
    q5 = build_target_weights(panel)
    results = add_benchmark(
        run_backtest(q5).set_index("month"),
        panel,
    )

    print("组合回测结果（%）：")
    print(
        results[
            [
                "turnover",
                "transaction_cost",
                "gross_return",
                "net_return",
                "benchmark_gross_return",
                "excess_gross_vs_benchmark",
                "excess_net_vs_gross_benchmark",
            ]
        ].mul(100).round(4).to_string()
    )

    cumulative_gross = (1 + results["gross_return"]).prod() - 1
    cumulative_net = (1 + results["net_return"]).prod() - 1
    cumulative_benchmark = (
        1 + results["benchmark_gross_return"]
    ).prod() - 1

    print("\n累计收益（%）：")
    print(f"Q5 扣费前：{cumulative_gross * 100:.2f}")
    print(f"Q5 扣费后：{cumulative_net * 100:.2f}")
    print(f"等权基准未扣费：{cumulative_benchmark * 100:.2f}")

    output_path = OUTPUT_DIR / "backtest_results.csv"
    results.reset_index().to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
    )
    print("\n回测结果已保存：", output_path)


if __name__ == "__main__":
    main()
