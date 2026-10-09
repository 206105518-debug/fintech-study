# day09_numpy_answer.py ｜ 参考答案
# 先自己做，卡住 30 分钟以上再来看。看完关掉重敲一遍。

import numpy as np


# ---------- 题 1  创建与属性 ----------
a = np.array([1, 2, 3, 4, 5])
b = np.zeros(5)
c = np.ones(3)
d = np.arange(1, 11)
e = np.linspace(0, 1, 5)

print(f"a = {a}")
print(f"全 0：{b}")
print(f"全 1：{c}")
print(f"arange(1, 11)：{d}")        # 右端不含 11
print(f"linspace(0, 1, 5)：{e}")    # 含两端，切成 5 个点
print(f"a 的 shape={a.shape}，ndim={a.ndim}，dtype={a.dtype}")


# ---------- 题 2  索引与切片 ----------
a = np.array([10, 20, 30, 40, 50])
print(f"a[0]={a[0]}，a[-1]={a[-1]}")
print(f"a[1:4]={a[1:4]}")           # 右端不含，拿到 20 30 40
print(f"a[::-1]={a[::-1]}")         # 反转

m = np.array([[1, 2, 3], [4, 5, 6]])
print(f"第一行 m[0]：{m[0]}")
print(f"第二列 m[:, 1]：{m[:, 1]}")   # 冒号表示「所有行」
print(f"第二行第三列 m[1, 2]：{m[1, 2]}")
print(f"所有大于 3 的数 m[m > 3]：{m[m > 3]}")


# ---------- 题 3  向量化 ----------
# a) 平方
squares_loop = []
for x in range(1, 21):
    squares_loop.append(x * x)

arr = np.arange(1, 21)
squares_np = arr ** 2
print(f"循环版：{squares_loop[:5]}...")
print(f"numpy 版：{squares_np[:5]}...")
print(f"两者完全相同：{squares_loop == squares_np.tolist()}")

# b) 1 加到 100
total_loop = 0
for i in range(1, 101):
    total_loop = total_loop + i
total_np = np.arange(1, 101).sum()
print(f"循环版 1 到 100 的和：{total_loop}")
print(f"numpy 版：{total_np}")

# c) 1000 个随机数里有多少个大于 0
np.random.seed(42)
data = np.random.normal(0, 1, 1000)

count_loop = 0
for x in data:
    if x > 0:
        count_loop = count_loop + 1
count_np = (data > 0).sum()
print(f"循环版数出 {count_loop} 个正数")
print(f"numpy 版数出 {count_np} 个")     # (data > 0) 是一串 True/False，求和就是个数


# ---------- 题 4  广播 ----------
v = np.array([1, 2, 3])
print(f"v + 10 = {v + 10}")
print(f"v * 2  = {v * 2}")

m = np.array([[1, 2, 3], [4, 5, 6]])
print(f"矩阵每行都加 [10, 20, 30]：\n{m + np.array([10, 20, 30])}")


# ---------- 题 5  统计函数与 axis ----------
np.random.seed(42)
arr = np.random.normal(0, 1, 1000)
print(f"均值 {arr.mean():.3f}，标准差 {arr.std():.3f}")
print(f"最大 {arr.max():.3f}，最小 {arr.min():.3f}")
print(f"中位数 {np.percentile(arr, 50):.3f}")

m = np.random.normal(0, 0.02, (5, 3))
print(f"矩阵形状：{m.shape}")
print(f"按列算 axis=0，结果形状 {m.mean(axis=0).shape}：{m.mean(axis=0)}")
print(f"按行算 axis=1，结果形状 {m.mean(axis=1).shape}：{m.mean(axis=1)}")


# ---------- 题 6  随机数 ----------
np.random.seed(42)
data = np.random.normal(0, 1, 1000)
print(f"1000 个标准正态随机数：均值 {data.mean():.3f}，标准差 {data.std():.3f}，中位数 {np.percentile(data, 50):.3f}")


# ---------- 主菜  5 天 × 5 只股票的收益率矩阵 ----------
np.random.seed(42)
returns = np.random.normal(0, 0.02, (5, 5))

print("\n=== 收益率矩阵（%）===")
print(np.round(returns * 100, 2))

# a) 每只股票 5 天的平均：把「天」这一维压掉 → axis=0
per_stock = returns.mean(axis=0)
print(f"\n每只股票的平均日收益（%）：{np.round(per_stock * 100, 3)}")
print(f"结果有 {len(per_stock)} 个，对应 5 只股票")

# b) 每天 5 只股票的平均：把「股票」这一维压掉 → axis=1
per_day = returns.mean(axis=1)
print(f"每天的平均收益（%，每行一天）：{np.round(per_day * 100, 3)}")
print(f"结果有 {len(per_day)} 个，对应 5 天")

# c) 极值
print(f"\n最大单日涨幅：{returns.max() * 100:.2f}%")
print(f"最大单日跌幅：{returns.min() * 100:.2f}%")

# d) 上涨的有几个
print(f"25 个收益率里上涨的有 {(returns > 0).sum()} 个")
