# day11_plot_answer.py ｜ 参考答案
# 先自己做，卡住 30 分钟以上再来看。

import numpy as np
import matplotlib.pyplot as plt


# ---------- 题 0  中文显示 ----------
plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "Heiti SC"]
plt.rcParams["axes.unicode_minus"] = False   # 让负号正常显示


# ---------- 题 1  第一条折线图 ----------
x = np.arange(1, 11)
y = x ** 2

plt.figure(figsize=(8, 4.5))
plt.plot(x, y)
plt.title("y 等于 x 的平方")
plt.xlabel("x")
plt.ylabel("y")
plt.legend(["y = x²"])
plt.savefig("test_plot.png", dpi=150, bbox_inches="tight")
plt.close()
print("已保存 test_plot.png")


# ---------- 题 2  存成文件（见上面 savefig 的用法）----------
# 三个参数：文件名、dpi 清晰度、bbox_inches="tight" 裁掉多余空白
# 顺序要点：savefig 必须写在 show 之前


# ---------- 题 3  净值曲线 ----------
np.random.seed(42)
DAYS = 500
daily_mean = 0.10 / 252
daily_std = 0.20 / np.sqrt(252)
returns = np.random.normal(daily_mean, daily_std, DAYS)
nav = (1 + returns).cumprod()
days = np.arange(1, DAYS + 1)

plt.figure(figsize=(9, 4.5))
plt.plot(days, nav, color="steelblue", linewidth=1.5)
plt.axhline(1.0, color="gray", linestyle="--", linewidth=1)   # 本金线
plt.title("模拟基金净值曲线（500 个交易日）")
plt.xlabel("交易日")
plt.ylabel("净值")
plt.grid(alpha=0.3)
plt.annotate(f"最终净值 {nav[-1]:.3f}",
             xy=(days[-1], nav[-1]),
             xytext=(days[-1] - 150, nav[-1] - 0.12),
             arrowprops=dict(arrowstyle="->", color="gray"))
plt.savefig("nav_curve.png", dpi=150, bbox_inches="tight")
plt.close()
plt.show()
print("已保存 nav_curve.png")


# ---------- 题 5  回撤曲线 ----------
running_max = np.maximum.accumulate(nav)
drawdown = nav / running_max - 1

plt.figure(figsize=(9, 4.5))
plt.plot(days, drawdown * 100, color="firebrick", linewidth=1)
plt.fill_between(days, drawdown * 100, 0, color="salmon", alpha=0.5)
plt.title("回撤曲线（从历史最高点算起）")
plt.xlabel("交易日")
plt.ylabel("回撤（%）")
plt.grid(alpha=0.3)
plt.annotate(f"最大回撤 {drawdown.min() * 100:.2f}%",
             xy=(days[drawdown.argmin()], drawdown.min() * 100),
             xytext=(days[drawdown.argmin()] + 30, drawdown.min() * 100 + 6),
             arrowprops=dict(arrowstyle="->", color="gray"))
plt.savefig("drawdown.png", dpi=150, bbox_inches="tight")
plt.close()
print("已保存 drawdown.png")
