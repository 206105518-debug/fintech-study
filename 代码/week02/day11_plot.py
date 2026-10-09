# day11_plot.py ｜ 2026.10.9 提前开始（原定 10.10）：matplotlib 画图
#
# 运行方式：
#   cd 金融科技学习/代码/week02
#   python3 day11_plot.py
#
# 今天（10.9）做前四题，把净值曲线画出来。
# 明天（10.10，只有 2 小时）做题 5：回撤曲线 + 两张图收口 → 交付物 3。
#
# 为什么画图重要：
#   研报、汇报、面试，没人看你的终端输出。一张净值曲线图能说明的事，
#   胜过十行数字。而且「看图找异常」是回测时的重要手感——
#   曲线突然跳一下，往往就是数据出了问题。

import numpy as np
import matplotlib.pyplot as plt

# 如果运行时报错、或者图窗口一闪而过：在 import matplotlib.pyplot 之前加两行
#   import matplotlib
#   matplotlib.use("Agg")
# 这样只存图片、不弹窗口，最稳（我们要的交付物本来就是存成 png）。


# ==========================================================
# 题 0  先解决中文显示（不做这步，图上中文会变成一排方框）
#   在 import 之后加上这两行：
#     plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "Heiti SC"]
#     plt.rcParams["axes.unicode_minus"] = False
#   第一行是指定中文字体（你电脑上这两款都有）。
#   第二行是让负号正常显示 —— 中文字体里的负号是另一种符号，
#   不设这一行，纵轴的负号会变成方块。
#   动手：加上之后，随便画一张带中文标题的图试试
# ==========================================================

# TODO 0
plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "Heiti SC"]
plt.rcParams["axes.unicode_minus"] = False



# ==========================================================
# 题 1  画第一条折线图
#   先造点简单数据：x = np.arange(1, 11)，y = x ** 2
#   然后四个基本动作：
#     plt.plot(x, y)              画线
#     plt.title("标题")           标题
#     plt.xlabel("x 轴") / plt.ylabel("y 轴")   轴标签
#     plt.legend(["y = x²"])      图例（有多个数据系列时才需要）
#   最后 plt.show() 在屏幕上显示出来。
#   提示：如果你在终端里跑，窗口可能一闪而过，用 savefig 存成图片更省事
# ==========================================================

# TODO 1
#怎么画图？

x = np.arange(1, 11)
y = x ** 2

plt.plot(x, y)
plt.title("标题")
plt.xlabel("x 轴")
plt.ylabel("y 轴")
plt.legend(["y = x²"])


# ==========================================================
# 题 2  把图存成文件
#   用 plt.savefig("文件名.png", dpi=150, bbox_inches="tight")
#   三个参数的意思：
#     文件名 —— 存成 png 方便看，也可以存 pdf 给打印用
#     dpi=150 —— 清晰度，150 够看，300 适合放简历
#     bbox_inches="tight" —— 把周围多余的空白裁掉
#   动手：把题 1 那张图存成 test_plot.png，然后去文件夹里确认它真的存在
#   注意：savefig 要写在 show 之前，写在 show 后面经常存出来是一张白图
#   （因为 show 之后画布就被清掉了——这个坑很多人踩过）
# ==========================================================

# TODO 2
plt.savefig("test_plot.png", dpi=150, bbox_inches="tight")
plt.close()

# ==========================================================
# 题 3  用昨天的数据画净值曲线
#   把 day10 的思路搬过来（可以复制那几行）：
#     seed(42) → 生成 500 天日收益率 → cumprod 算出净值
#   然后画出来：
#     x 轴是第几天（np.arange(1, 501)）
#     y 轴是净值
#   加三样东西让它像一张正经的图：
#     标题「模拟基金净值曲线（500 个交易日）」
#     轴标签「交易日」「净值」
#     一条水平参考线 plt.axhline(1.0, color="gray", linestyle="--")
#       —— 净值 1.0 是初始本金，线在它上面就是赚钱，在下面就是亏钱
#   动手：存成 nav_curve.png
# ==========================================================

# TODO 3
np.random.seed(42)
returns=np.random.normal(0.1/252 ,0.2/(252**0.5),500)
nav = (1 + returns).cumprod()

x=np.arange(1,501)
y=nav

plt.plot(x, y, color="steelblue", linewidth=1.5)
plt.title("模拟基金净值曲线(500个交易日)")
plt.xlabel("交易日")
plt.ylabel("净值")
plt.axhline(1.0, color="gray", linestyle="--")


# ==========================================================
# 题 4  换个颜色、加个标注（可选，5 分钟）
#   a) plot 里加 color 和 linewidth：plt.plot(x, y, color="steelblue", linewidth=1.5)
#   b) 用 plt.annotate 在图上标一句话，比如最终净值是多少
#   c) 给图加网格：plt.grid(alpha=0.3)（alpha 是透明度）
#   这些不是必须的，但一张干净清楚的图在汇报里很加分
# ==========================================================

# TODO 4

plt.annotate(f"最终净值为{nav[-1]:.2f}",
             xy=(500,nav[-1]),
             xytext=(400,nav[-1]*0.9),
             arrowprops=dict(arrowstyle="->",color="grey"))
#在净值曲线最后一个点 (500, 最终净值) 上戳一根箭头，箭头旁边摆一行字「最终净值 1.84」，
# 字放在左下方、位置大概是净值的 90% 高度。

plt.grid(alpha=0.3)

plt.savefig("nav_curve.png", dpi=150, bbox_inches="tight")
plt.close()
# ==========================================================
# 题 5  回撤曲线（明天做，今天可以先看一眼思路）
#   回撤序列你昨天已经算过了：nav / cummax - 1，永远小于等于 0。
#   画法上比净值曲线多一个技巧：
#     plt.fill_between(x, drawdown, 0, color="salmon", alpha=0.5)
#     —— 把回撤和 0 之间的区域填色，看上去就是机构研报里那种「水下阴影」
#   要求：
#     标题、轴标签齐全；y 轴用百分比显示；存成 drawdown.png
#   明天做完这一题，把题 3 和题 5 拼成一个脚本，交付物 3 就完成了
# ==========================================================

# TODO 5（明天做）#y轴是日回撤 x轴是时间

drawdown = nav / np.maximum.accumulate(nav) - 1

x=np.arange(1,501)
y=drawdown*100

plt.plot(x,y) #画线
plt.title("回撤曲线(500个交易日)")
plt.xlabel("交易日")
plt.ylabel("日回撤%")

max_dd_day = x[drawdown.argmin()]   # 最大回撤发生在第几天
max_dd_val = drawdown.min()*100         # 最大回撤的值（最负的那个）

plt.annotate(f"最大日回撤是 {max_dd_val:.2f}%",
             xy=(max_dd_day, max_dd_val),
             xytext=(max_dd_day, max_dd_val * 0.9),
             arrowprops=dict(arrowstyle="->"))

plt.fill_between(x, drawdown*100, 0, color="salmon", alpha=0.5)

plt.savefig("drawdown.png", dpi=150, bbox_inches="tight")
plt.show()

# ==========================================================
# 收尾
#   1) 记住 savefig 要写在 show 之前
#   2) 明天（10.10，2h）：题 5 + 把两张图整理成一个脚本 → 交付物 3
#   3) 提交代码：git add . && git commit -m "..." && git push
# ==========================================================
