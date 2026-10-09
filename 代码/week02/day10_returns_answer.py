# day10_returns_answer.py ｜ 参考答案
# 先自己做，卡住 30 分钟以上再来看。

import numpy as np


# ---------- 题 1  生成日收益率 ----------
np.random.seed(42)

DAYS = 500                 # 交易日数，大约 2 年
ANNUAL_RETURN = 0.10       # 假设的长期年化收益
ANNUAL_VOL = 0.20          # 假设的年化波动
TRADING_DAYS = 252         # 一年 252 个交易日，这是行业约定

daily_mean = ANNUAL_RETURN / TRADING_DAYS
daily_std = ANNUAL_VOL / np.sqrt(TRADING_DAYS)

returns = np.random.normal(daily_mean, daily_std, DAYS)
print(f"日收益率前 5 个：{np.round(returns[:5], 4)}")


# ---------- 题 2  净值曲线 ----------
nav = (1 + returns).cumprod()
print(f"净值曲线：第一天 {nav[0]:.4f}，最后一天 {nav[-1]:.4f}")


# ---------- 题 3  累计收益率 ----------
cum_return = nav[-1] - 1
print(f"累计收益率：{cum_return * 100:.2f}%")


# ---------- 题 4  年化收益率 ----------
ann_ret = (1 + cum_return) ** (TRADING_DAYS / DAYS) - 1
print(f"年化收益率：{ann_ret * 100:.2f}%")


# ---------- 题 5  年化波动率 ----------
ann_vol = returns.std() * np.sqrt(TRADING_DAYS)
print(f"年化波动率：{ann_vol * 100:.2f}%")
# 严格说样本标准差要用 returns.std(ddof=1)，差别很小，先不用纠结。


# ---------- 题 6  最大回撤 ----------
running_max = np.maximum.accumulate(nav)
drawdown = nav / running_max - 1
max_dd = drawdown.min()
print(f"最大回撤：{max_dd * 100:.2f}%")
print(f"（回撤序列的最大值是 {drawdown.max():.4f}，应该是 0）")


# ---------- 主菜  封装成函数 ----------
def total_return(nav):
    """累计收益率：最后一期净值 / 第一期之前的值 - 1。"""
    return nav[-1] / 1.0 - 1


def annual_return(nav, trading_days=252):
    """年化收益率：把累计收益按交易日数折算成年化（复利口径）。"""
    days = len(nav)
    cum = nav[-1] / 1.0 - 1
    return (1 + cum) ** (trading_days / days) - 1


def annual_volatility(returns, trading_days=252):
    """年化波动率：日收益率标准差 × √交易天数。"""
    return returns.std() * np.sqrt(trading_days)


def max_drawdown(nav):
    """最大回撤：从每个历史高点到之后最低点的最大跌幅，一定是负数或 0。"""
    running_max = np.maximum.accumulate(nav)
    drawdown = nav / running_max - 1
    return drawdown.min()


print("\n=== 绩效指标 ===")
print(f"{'指标':<12}{'数值':>10}")
print(f"{'累计收益率':<12}{total_return(nav) * 100:>9.2f}%")
print(f"{'年化收益率':<12}{annual_return(nav) * 100:>9.2f}%")
print(f"{'年化波动率':<12}{annual_volatility(returns) * 100:>9.2f}%")
print(f"{'最大回撤':<12}{max_drawdown(nav) * 100:>9.2f}%")
