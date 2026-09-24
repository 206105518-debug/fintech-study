# day04_control_answer.py ｜ 参考答案
# 先自己做，卡住 30 分钟以上再来看。看完关掉重敲一遍。


# ---------- 题 1  条件判断 ----------
change = 3.2

if change >= 5:
    print("大涨")
elif change >= 3:
    print("上涨")
elif change >= 0:
    print("微涨")
elif change >= -3:
    print("微跌")
else:
    print("下跌")

# 边界测试：把 change 换成 5 / 3 / 0 / -3 / -5 各跑一次，看落点对不对。
for change in [5, 3, 0, -3, -5]:
    if change >= 5:
        print(f"{change} → 大涨")
    elif change >= 3:
        print(f"{change} → 上涨")
    elif change >= 0:
        print(f"{change} → 微涨")
    elif change >= -3:
        print(f"{change} → 微跌")
    else:
        print(f"{change} → 下跌")


# ---------- 题 2  for 循环 ----------
for i in range(1, 11):            # a) range(1, 11) 是 1 到 10，不含 11
    print(i)

for i in range(2, 11, 2):         # b) 步长 2，从 2 开始就是偶数
    print(i)

for i in range(10, 0, -1):        # c) 步长 -1 就是倒着走
    print(i)

total = 0                         # d) 和字频累加是同一个模式
for i in range(1, 101):
    total = total + 1 * i
print(f"1 到 100 的和：{total}")   # 5050

stocks = ["贵州茅台", "宁德时代", "招商银行"]
codes = ["600519", "300750", "600036"]

for idx, name in enumerate(stocks):      # e) 索引默认从 0 开始
    print(idx, name)

for idx, name in enumerate(stocks, start=1):   # 想从 1 开始就加 start=1
    print(f"{idx}. {name}")

for code, name in zip(codes, stocks):    # f) 一对一配对
    print(f"{code} 是 {name}")


# ---------- 题 3  while ----------
i = 1
total = 0
while i <= 100:
    total += i          # 等价于 total = total + i
    i += 1              # 这一行千万别忘，忘了就是死循环
print(f"while 版 1 到 100 的和：{total}")

n = 10
while n > 0:
    print(n)
    n -= 2              # 10 8 6 4 2


# ---------- 题 4  break 和 continue ----------
for i in range(1, 100):
    if i % 3 == 0 and i % 7 == 0:
        print(f"第一个能同时被 3 和 7 整除的数是 {i}")
        break

for i in range(1, 11):
    if i % 3 == 0:
        continue        # 这一次不算，直接回去做下一次
    print(i)


# ---------- 题 5  列表推导式 ----------
squares = [i * i for i in range(1, 21)]
print(squares)

threes = [i for i in range(1, 51) if i % 3 == 0]
print(threes)

holdings = ["贵州茅台", "宁德时代", "招商银行"]
labels = [f"{name}：持有" for name in holdings]
print(labels)


# ---------- 主菜 A  九九乘法表 ----------
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}×{i}={i * j}", end="\t")
    print()             # 内层跑完，换到下一行


# ---------- 主菜 B  1 到 100 的质数 ----------
primes = []
for n in range(2, 101):
    is_prime = True
    for d in range(2, n):
        if n % d == 0:
            is_prime = False
            break       # 已经确认不是质数，剩下的除数不用试了
    if is_prime:
        primes.append(n)

print(f"1 到 100 的质数共 {len(primes)} 个：{primes}")
