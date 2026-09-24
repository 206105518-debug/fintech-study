# day05_functions_answer.py ｜ 参考答案
# 先自己做，卡住 30 分钟以上再来看。看完关掉重敲一遍。


# ---------- 题 1 ----------
def greet(name):
    print(f"你好，{name}")


def add(a, b):
    return a + b


greet("乔静")

result = add(3, 5)          # 把交出来的结果接住
print(f"add(3, 5) 交回来的：{result}")


# ---------- 题 2  只打印 vs 交出结果 ----------
def add_print(a, b):
    print(a + b)            # 只喊了一声，什么都没交出来


def add_return(a, b):
    return a + b            # 把结果交出来


x = add_print(2, 3)         # 屏幕上会出现 5，但 x 接不到东西
print(f"add_print 交回来的东西：{x}")        # None

y = add_return(2, 3)
print(f"add_return 交回来的东西：{y}")       # 5

print(f"交出来的结果还能继续算：{add_return(2, 3) * 10}")
# print(f"打印出来的结果没法接着算：{add_print(2, 3) * 10}")   # 会报错
# 报错：TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'


# ---------- 题 3  默认参数和关键字参数 ----------
def make_signal(name, window=20, weight=1.0):
    return f"{name} 因子，窗口 {window} 天，权重 {weight}"


print(make_signal("动量"))
print(make_signal("动量", 60))
print(make_signal("动量", weight=0.5))
print(make_signal(window=10, name="价值"))    # 关键字传参，顺序自由


# ---------- 题 4  作用域 ----------
def scoped():
    inner = "我只活在函数里"
    print(f"函数里能看到：{inner}")


scoped()

# print(inner)
# 报错：NameError: name 'inner' is not defined
# 函数是个封闭的小房间，房间里的东西外面拿不到，想递出来就得 return。


# 加餐：可变对象的坑
def add_one_num(n):
    n = n + 1               # 数字不可变，改的是房间里的副本，外面不受影响


def add_one_list(lst):
    lst.append("被函数改了")  # 列表可变，函数里改的是同一个列表，外面会跟着变


num = 10
add_one_num(num)
print(f"数字传进去之后：{num}")        # 还是 10

my_list = ["原来的"]
add_one_list(my_list)
print(f"列表传进去之后：{my_list}")     # 多了一项


# ---------- 题 5  把旧代码改写成函数 ----------
def rate_label(change):
    if change >= 5:
        return "大涨"
    elif change >= 3:
        return "上涨"
    elif change >= 0:
        return "微涨"
    elif change >= -3:
        return "微跌"
    else:
        return "下跌"


for change in [6, 3.2, 0, -3, -8]:
    print(f"{change}% → {rate_label(change)}")


def count_chars(text):
    clean = text.replace("，", "").replace("。", "").replace(" ", "")
    counts = {}
    for ch in clean:
        counts[ch] = counts.get(ch, 0) + 1
    return counts


print(count_chars("宁德时代比亚迪宁德时代比亚迪宁德时代"))


def find_primes(limit):
    primes = []
    for i in range(2, limit + 1):
        is_prime = True
        for j in range(2, i):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    return primes


print(f"1 到 100 的质数：{len(find_primes(100))} 个")


def print_table(n):
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            print(f"{j}×{i}={i * j}", end="\t")
        print()


print_table(9)


# ---------- 题 6  lambda 和排序 ----------
prices = {"600519": 1680.5, "300750": 210.3, "600036": 35.8}
moves = [("贵州茅台", 3.2), ("宁德时代", -1.5), ("招商银行", 0.8)]

print("按价格从高到低：")
for code, price in sorted(prices.items(), key=lambda kv: kv[1], reverse=True):
    print(f"  {code} {price}")
# 这一行和你在字频那题里写的是同一个东西，只是换了个数据。

print("按涨跌幅从高到低：")
for name, move in sorted(moves, key=lambda item: item[1], reverse=True):
    print(f"  {name} {move}%")

square = lambda x: x * x
print(f"lambda 算平方：{square(7)}")
# 实际写代码时更推荐用 def，lambda 只在「递给别的函数当规则」时才划算。


# ---------- 主菜  summarize ----------
def summarize(text):
    clean = text.replace("，", "").replace("。", "").replace(" ", "")
    counts = {}
    for ch in clean:
        counts[ch] = counts.get(ch, 0) + 1
    top3 = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:3]
    return len(clean), len(set(clean)), top3


text = "宁德时代比亚迪宁德时代比亚迪宁德时代"
total, distinct, top3 = summarize(text)     # 三个值一起接住，这叫拆包
print(f"总字数 {total}，不同字 {distinct}，出现最多的三个：{top3}")


# ---------- 顺带把昨天欠的列表推导式补上 ----------
squares = [i * i for i in range(1, 21)]
threes = [i for i in range(1, 51) if i % 3 == 0]
holdings = ["贵州茅台", "宁德时代", "招商银行"]
labels = [f"{name}：持有" for name in holdings]
print(squares)
print(threes)
print(labels)
