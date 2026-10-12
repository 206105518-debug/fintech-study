# performance_report.py ｜ 交付物 3：收益与回撤评估脚本
#
# 运行方式：
#   cd 金融科技学习/代码/week02
#   python3 performance_report.py
#
# 这个脚本要做什么：
#   生成一条模拟的日收益率序列 → 算出四个绩效指标 → 画出两张图。
#
# 为什么要有这个文件：
#   day10 和 day11 是你练习时一段一段写出来的，能跑，但顺序零散。
#   这个文件把它们整理成「函数分块 + 一个主流程」的成品形态。
#   十一月做多因子回测时，你会把这个文件里的函数直接搬过去用。
#
# 整理的原则只有一条：**一个函数只做一件事。**
#   生成数据、算净值、算指标、画图，各自独立；
#   主流程只负责按顺序调用它们，不干别的。

import numpy as np
import matplotlib.pyplot as plt

# 中文字体：不设这两行，图上的中文会变成方框
plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "Heiti SC"]
plt.rcParams["axes.unicode_minus"] = False


# ==========================================================
# 第一部分：参数区
#   把「可以改的东西」集中放在最上面，别散落在代码里。
#   以后换数据、换假设，只改这里，下面的函数一行都不用动。
# ==========================================================
SEED = 42
DAYS = 500
ANNUAL_RETURN = 0.10
ANNUAL_VOL = 0.20
TRADING_DAYS = 252


# ==========================================================
# 第二部分：数据生成
# ==========================================================

def generate_returns(days=DAYS, annual_return=ANNUAL_RETURN,
                     annual_vol=ANNUAL_VOL, seed=SEED):
    """生成日收益率序列。

    输入：天数、年化收益、年化波动、随机种子
    返回：一个长度为 days 的一维数组

    提示：日收益均值 = 年化收益 / 252；日标准差 = 年化波动 / √252。
    """
    # TODO
    
    np.random.seed(seed)
    daily_mean=annual_return/TRADING_DAYS
    daily_std=annual_vol/np.sqrt(TRADING_DAYS)
    return np.random.normal(daily_mean, daily_std, days)


def to_nav(returns):
    """把日收益率累乘成净值曲线，返回和输入等长的数组。"""
    # TODO
    
    return (1 + returns).cumprod()


# ==========================================================
# 第三部分：四个指标
#   每个函数只算一个数，输入输出都写在 docstring 里。
# ==========================================================

def total_return(nav):
    """累计收益率：最后一期净值相对 1 元的涨跌。"""
    # TODO
    
    return nav[-1]-1


def annual_return(nav, trading_days=TRADING_DAYS):
    """年化收益率（复利口径）：(1 + 累计收益) ** (252 / 天数) - 1。"""
    # TODO

    cum=nav[-1]-1
    return (1+cum)**(trading_days/len(nav))-1

def annual_volatility(returns, trading_days=TRADING_DAYS):
    """年化波动率：日收益率标准差 × √252。

    注意：直接用传进来的 returns，不要在这里重新生成数据。
    """
    # TODO
    
    return returns.std() * np.sqrt(trading_days)

def max_drawdown(nav):
    """最大回撤：nav / 历史最高净值 - 1 的最小值，一定是负数或 0。"""
    # TODO
    
    hist_max_drawdown=np.maximum.accumulate(nav) #历史最高净值
    day_drawdown= nav / hist_max_drawdown - 1
    return day_drawdown.min()


# ==========================================================
# 第四部分：画图
#   两个函数各管一张图，都直接把图片存成文件，不返回东西。
# ==========================================================

def plot_nav(days, nav, filename="nav_curve.png"):
    """画净值曲线：带本金参考线、标题、轴标签，存成 png。"""
    # TODO

    plt.figure()

    x=days
    y=nav

    plt.plot(x, y, color="steelblue", linewidth=1.5)
    plt.title("模拟基金净值曲线(500个交易日)")
    plt.xlabel("交易日")
    plt.ylabel("净值")
    plt.axhline(1.0, color="gray", linestyle="--")
    plt.grid(alpha=0.3)

    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close()


def plot_drawdown(days, nav, filename="drawdown.png"):
    """画回撤曲线：用 fill_between 把水下部分填色，纵轴用百分比。"""
    # TODO

    drawdown = nav / np.maximum.accumulate(nav) - 1
    x=days
    y=drawdown*100

    plt.plot(x,y) #画线
    plt.title("回撤曲线(500个交易日)")
    plt.xlabel("交易日")
    plt.ylabel("日回撤%")

    plt.fill_between(x, drawdown*100, 0, color="salmon", alpha=0.5)

    plt.savefig(filename, dpi=150, bbox_inches="tight")


# ==========================================================
# 第五部分：主流程
#   它只负责「按顺序喊名字」，不写具体计算。
# ==========================================================

def main():
    returns = generate_returns()
    nav = to_nav(returns)

    # 1) 打印指标表：用 total_return / annual_return / annual_volatility / max_drawdown
    # TODO
    print(f"{'指标':<8}{'数值':>8}")
    print(f"{'累计收益率':<8}{total_return(nav)*100:>8.2f}%")
    print(f"{'年化收益率':<8}{annual_return(nav)*100:>8.2f}%")
    print(f"{'年化波动率':<8}{annual_volatility(returns)*100:>8.2f}%")
    print(f"{'最大回撤':<8}{max_drawdown(nav)*100:>8.2f}%")


  


    # 2) 画两张图
    days = np.arange(1, len(nav) + 1)
    # TODO
    plot_nav(days,nav)
    plot_drawdown(days,nav)
    
    print("完成：指标表已打印，两张图已保存")


# 这一行的意思：只有「直接运行这个脚本」时才执行 main()；
# 如果别人 import 这个文件去用里面的函数，主流程不会自己跑起来。
if __name__ == "__main__":
    main()
