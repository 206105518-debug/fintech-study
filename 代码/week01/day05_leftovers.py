# day05_leftovers.py ｜ 2026.9.17 补漏：还没做完的五件事
#
# 全部做完大约 20 分钟。做完这个文件，第一周的语法就齐了。
#
# 五件事：
#   1  列表推导式 b、c 两小问（a 你自己已经写出来了）
#   2  map 和 filter（计划里点到，但还没碰过）
#   3  count_chars 补上「去空格」
#   4  find_primes 的结果用变量接住，只调用一次
#   5  day05_functions.py 里题 1 的两处清理（在那边改，不在这里写）
#
# 答案放在文件最底部，是注释状态。做完再取消注释对照，别一上来就翻。


# ==========================================================
# 补 1  列表推导式 b、c
#   你在 day04_control.py 第 158 行自己写出了这个：
#       squares = [i*i for i in range(1,21)]
#   形状你已经拿到了。下面两小问自己写一遍，不要照抄。
#
#   b) 挑出 1 到 50 里所有能被 3 整除的数，存进 threes
#   c) 把 holdings 变成 ["贵州茅台：持有", "宁德时代：持有", ...]，存进 labels
#   自查：b 应该是 16 个数（3 到 48），c 是三项，中间用中文冒号
# ==========================================================

holdings = ["贵州茅台", "宁德时代", "招商银行"]

# 你的 threes 写在这里：
three=[i for i in range(1,51) if i%3==0]
print(three)

# 你的 labels 写在这里：
labels=[i+"：持有" for i in ["贵州茅台", "宁德时代", "招商银行"]]
print(labels)
# ==========================================================
# 补 2  map 和 filter
#   这两个和 sorted 是一家人：都递一条 lambda 规则进去，它替你挨个用一遍。
#     map    —— 对每个元素做同一件事，出来的还是一串，个数不变
#     filter —— 对每个元素问一句「要不要」，出来的个数会变少
#
#   要求：
#     a) 用 map 把 nums 里每个数平方
#     b) 用 filter 挑出 nums 里的偶数
#     c) 先直接 print 这两个结果，看它打出什么奇怪的东西；
#        再用 list() 包一层打印，看看变成什么
#   重点是 c，你会看到一个带内存地址的东西，那是 Python 3 的经典现象。
# ==========================================================

nums = [1, 2, 3, 4, 5]

# a) 你的 map 写在这里：
平方=map(lambda num: num**2, nums)

# b) 你的 filter 写在这里：
偶数=filter(lambda x:x%2==0 ,nums)
# c) 直接 print 一次，再套 list() 打印一次：
#print(平方) #<map object at 0x10314ffa0>
print(list(平方)) 
#print(偶数) #<filter object at 0x10314ffa0>
print(list(偶数))
# ==========================================================
# 补 3  count_chars 补上「去空格」
#   要求：把 ，。和空格三样都去掉。
#   自查：count_chars("宁德 时代，宁德 时代。") 的结果里
#         不应该出现空格这个键，宁、德、时、代 各 2 次。
#         （下面先给了一个空壳，能跑，但结果是空字典，等你补完才是对的）
# ==========================================================

def count_chars(text):
    t1=text.replace("，","").replace("。","").replace(" ","")
    counts = {}
    for ch in t1:
        counts[ch]=counts.get(ch,0)+1
    return counts


print(count_chars("宁德 时代，宁德 时代。"))


# ==========================================================
# 补 4  find_primes 的结果要用变量接住
#   上次你写成 find_primes(100) 然后 print(primes)，会报 NameError，
#   因为 primes 是函数房间里的东西，外面拿不到。
#   这次要求：只调用一次函数，用变量接住结果，
#             然后打印这个变量，再打印它的长度。
#   自查：打印出 25 个数，长度也是 25。
# ==========================================================

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


# 你的调用写在这里：
result = find_primes(100)
print(result)
print(len(result))
# ==========================================================
# 补 5  回 day05_functions.py 改题 1（这里不写代码）
#   a) add 定义了两遍，删掉一个
#   b) 函数体里 add = a + b 那个局部变量，改名成 total，
#      或者干脆直接写 return a + b
# ==========================================================


# ==========================================================
# 答案区（做完再取消注释对照）
# ==========================================================
# ---- 补 1 ----
# threes = [i for i in range(1, 51) if i % 3 == 0]
# print(threes)
#
# labels = [f"{name}：持有" for name in holdings]
# print(labels)
#
# ---- 补 2 ----
# nums = [1, 2, 3, 4, 5]
# squares = map(lambda x: x * x, nums)
# evens = filter(lambda x: x % 2 == 0, nums)
# print(squares)          # <map object at 0x...> 就是那个奇怪的东西
# print(list(squares))    # [1, 4, 9, 16, 25]
# print(list(evens))      # [2, 4]
# 注意：map / filter 交出来的是「一次性」的东西，
#       取过一次就空了。所以要么马上 list() 存起来，要么只用一次。
#
# ---- 补 3 ----
# def count_chars(text):
#     clean = text.replace("，", "").replace("。", "").replace(" ", "")
#     counts = {}
#     for ch in clean:
#         counts[ch] = counts.get(ch, 0) + 1
#     return counts
#
# ---- 补 4 ----
# result = find_primes(100)
# print(result)
# print(len(result))
