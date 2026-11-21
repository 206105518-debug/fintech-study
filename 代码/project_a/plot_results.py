"""生成项目 A 的累计收益图和分组收益图。"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).parent
DATA_DIR = BASE / "data"
FIGURE_DIR = BASE / "figures"
FIGURE_DIR.mkdir(exist_ok=True)

plt.rcParams["font.sans-serif"] = [
    "Arial Unicode MS",
    "Heiti TC",
    "SimHei",
]
plt.rcParams["axes.unicode_minus"] = False


def load_results():
    """读取回测结果和分组收益。"""
    backtest = pd.read_csv(DATA_DIR / "backtest_results.csv")
    groups = pd.read_csv(
        DATA_DIR / "group_returns.csv",
        index_col=0,
    )
    return backtest, groups


def plot_performance(backtest, groups):
    """绘制累计收益和每月分组平均收益。"""
    dates = pd.to_datetime(backtest["month"])

    q5_gross = (1 + backtest["gross_return"]).cumprod()
    q5_net = (1 + backtest["net_return"]).cumprod()
    benchmark = (
        1 + backtest["benchmark_gross_return"]
    ).cumprod()

    fig, axes = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(13, 5),
    )

    axes[0].plot(dates, q5_gross, marker="o", label="Q5 扣费前")
    axes[0].plot(dates, q5_net, marker="o", label="Q5 扣费后")
    axes[0].plot(
        dates,
        benchmark,
        marker="o",
        linestyle="--",
        label="等权基准（未扣费）",
    )
    axes[0].set_title("累计净值（2025-01 至 2025-08）")
    axes[0].set_xlabel("月份")
    axes[0].set_ylabel("累计净值")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    average_returns = groups.mean()
    axes[1].bar(
        average_returns.index,
        average_returns.values * 100,
    )
    axes[1].set_title("Q1–Q5 平均月度收益")
    axes[1].set_xlabel("分组")
    axes[1].set_ylabel("平均月度收益（%）")
    axes[1].grid(axis="y", alpha=0.3)

    fig.tight_layout()

    output_path = FIGURE_DIR / "backtest_performance.png"
    fig.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(fig)

    print("图表已保存：", output_path)
    print("\nQ1–Q5 平均月度收益（%）：")
    print((average_returns * 100).round(2).to_string())


def main():
    """运行图表生成。"""
    backtest, groups = load_results()
    plot_performance(backtest, groups)


if __name__ == "__main__":
    main()