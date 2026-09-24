# day05_functions.py ｜ 2026.9.17 周四（计划里周五的内容：函数）
#
# 今天的规矩：
#   1. 前 15 分钟：把昨天欠的列表推导式补掉（题 5 的三处，各写成一行）
#   2. 接着开始下面的题，写一段跑一次
#   3. 卡住 30 分钟就注释「卡住：xxx」跳过，周六回来解决
#   4. 运行方式：python3 day05_functions.py
#
# 函数是什么：
#   把一段会重复用的代码，起个名字装起来。
#   以后要用，喊名字就行，不用再抄一遍。
#   一句话：函数是「给代码起名字」，参数是「原料」，返回值是「成品」。


# ==========================================================
# 题 1  第一个函数：def / 参数 / 返回值
#   a) 写一个 greet(name)，接收一个名字，打印一句问候
#   b) 写一个 add(a, b)，返回两个数的和
#      注意 b 是用 return 把结果「交出去」，不是打印
#   c) 调用 add(3, 5)，把交回来的结果存进变量，再打印这个变量
# ==========================================================

# TODO 1
def greet(name):
    print(f"{name}你好！")

greet("张三")

def add(a,b):
    return a+b


x=add(3,5)
print(x)

# ==========================================================
# 题 2  只打印 vs 交出结果（今天最重要的一题）
#   写两个长得几乎一样的函数：
#     add_print(a, b)  —— 把两数之和打印出来
#     add_return(a, b) —— 把两数之和用 return 交出来
#   然后做三件事：
#     a) 用变量接住 add_print 的「返回值」，打印出来看看是什么
#     b) 用变量接住 add_return 的返回值，打印出来看看是什么
#     c) 试着打印 add_return(2, 3) * 10，再试试 add_print(2, 3) * 10
#   体会：打印是「说给别人听」，return 是「把东西交出去」，
#         只有交出去的东西，才能拿去做下一步运算。
#   这个区别在后面写回测、写评分卡时天天遇到：
#         函数只打印，你就没法把它的结果喂给下一个函数。
# ==========================================================

# TODO 2
#参考AI
def add_print(a,b):
    print(f"add_print={a+b}")


def add_return(a,b):
    add_return=a+b
    return add_return

x1=add_print(2,3)

x2=add_return(2,3)

print(x1)  #None
print(x2)

print(f"{add_return(2,3)*10}")
#print(f"{add_print(2,3)*10}") #报错：None无法乘10
# ==========================================================
# 题 3  默认参数和关键字参数
#   写一个 make_signal(name, window=20, weight=1.0)，返回一句话描述这个因子
#   要求能这样调用：
#     make_signal("动量")                       用默认的窗口和权重
#     make_signal("动量", 60)                   只改窗口
#     make_signal("动量", weight=0.5)           只改权重
#     make_signal(window=10, name="价值")        用关键字乱序传入
#   两个规则：
#     一是带默认值的参数必须写在后面，不带默认值的写前面；
#     二是按位置传的时候顺序不能错，按关键字传的时候顺序自由。
# ==========================================================

# TODO 3
#卡住
def make_signal(name,window=20,weight=1.0):
    return f"{name}因子，窗口{window}，权重{weight}"
print(make_signal("动量"))
print(make_signal("动量",60))
print(make_signal("动量",weight=0.5))
print(make_signal(window=10,name="价值"))
# ==========================================================
# 题 4  作用域：函数里的变量，外面看不见
#   a) 写一个函数，在函数内部定义一个变量，在里面打印它
#   b) 在函数外面也打印一下这个变量，运行看看报什么错，把报错抄进注释
#   这说明：函数是个封闭的小房间，房间里的东西外面拿不到。
#   想拿到，就得用 return 递出来。
#   （加餐，想不明白留到周六：函数接收一个列表参数时，
#     在函数里改这个列表，外面的列表会跟着变；
#     但如果接收的是一个数字，在函数里改，外面不会变。
#     原因和你在元组那题学过的「可变 / 不可变」是同一件事。）
# ==========================================================

# TODO 4
#参考AI
def hanshu():
    bianliang=1
    print(bianliang)
hanshu()



def hanshu():
    bianliang=1
    return bianliang
x=hanshu()
print(x)

# ==========================================================
# 题 5  把之前写过的代码改写成函数（这条是计划里的要求）
## TODO 5
#卡住：不会

#   四个函数的具体要求如下，照着写：
#
#   5-1  rate_label(change)
#        输入：一个涨跌幅数字，比如 3.2
#        输出：用 return 交出一个字符串，规则是
#              >= 5 大涨 / >= 3 上涨 / >= 0 微涨 / >= -3 微跌 / 其他 下跌
#        不许用 print 打印，必须 return
#        自查：rate_label(6) 是 "大涨"，rate_label(0) 是 "微涨"，
#              rate_label(-3) 是 "微跌"，rate_label(-8) 是 "下跌"
#        写完再用 for 循环把 [6, 3.2, 0, -3, -8] 五个值各测一遍

def rate_label(change):
    if change >=5:
        return "大涨"
    elif 3<= change <5:
        return "上涨"
    elif 0<= change <3:
        return "微涨"
    elif -3<= change <0:
        return "微跌"
    else:
        return "下跌"
x=rate_label(3)
print(x)

for i in [6, 3.2, 0, -3, -8]:
    y=rate_label(i)
    print(y)

#   5-2  count_chars(text)
#        输入：一段字符串
#        输出：返回一个字典，键是字，值是出现次数
#        要求：函数内部自己把标点（，。）和空格去掉，
#              外面调用的人不用管这件事
#        自查：先用小文本验证——count_chars("宁德时代")
#              应该得到 {'宁': 1, '德': 1, '时': 1, '代': 1}
#              再换成带标点的长文本，确认标点没被算进去
#
def count_chars(text):
    t1=text.replace("，","").replace("。","").replace(" ","")
    counts={}
    for ch in t1:
        counts[ch]=counts.get(ch,0)+1
    return counts
print(count_chars("宁德时代，宁德时代。"))
#卡住：空字典写成了 counts=[]

#   5-3  find_primes(limit)
#        输入：一个上限数字，比如 100
#        输出：返回一个列表，装着 2 到 limit 之间所有质数
#        要求：不许在函数里打印，必须把列表交出来
#        自查：len(find_primes(100)) 是 25，
#              换成 len(find_primes(10)) 应该是 4（2、3、5、7）
#
def find_primes(limit):
    primes=[]
    for i in range(2,limit+1):
        is_prime=True #is_prime 是标记法的布尔 flag：先设为 True（假设是质数），试除时一旦找到反例就翻成 False，最后看它还是不是 True 来决定收不收进列表。
        for j in range(2,i):
            if i%j==0:
                is_prime=False
                break
        if is_prime:
            primes.append(i)
    return primes
find_primes(100)
print(find_primes(100))
print(len(find_primes(100)))



#   5-4  print_table(n)
#        输入：要打多少行，比如 9
#        输出：直接把乘法表打到屏幕上，不交回任何东西
#        自查：print_table(3) 只打三行，最后一行是 1×3=3 2×3=6 3×3=9
#
#   四个写完回头看一眼：5-1、5-2、5-3 都用 return，5-4 直接打印。
#   判断标准是「这个结果还有没有人要接着用」。
# ==========================================================
def print_table(n):
    for i in range(1,n+1):
        for j in range(1,i+1):
            print(f"{j}*{i}={j*i}",end="\t")
        print()
print_table(9)


# ==========================================================
# 题 6  lambda 和排序
#   a) 下面这个字典，按价格从高到低打印出来
#      （提示：你在字频那题里已经写过一模一样的东西，回去看看）
#   b) 下面这个列表里是「股票名 + 涨跌幅」，按涨跌幅从高到低排序
#      提示：每一对有两项，要告诉排序函数按第 2 项比
#   c) 用 lambda 写一个能算平方的小函数，存成变量，调用它试试
#
#   一句话理解 lambda：它是「用完就扔的小规则」，
#   没有名字、只写一行、专门递给别的函数当参数用。
# ==========================================================

prices = {"600519": 1680.5, "300750": 210.3, "600036": 35.8}
moves = [("贵州茅台", 3.2), ("宁德时代", -1.5), ("招商银行", 0.8)]

# TODO 6
t1=list(prices.items())
print(sorted(t1,key=lambda kv:kv[1],reverse=True))

print(sorted(moves,key=lambda kv:kv[1],reverse=True))

#卡住：如何用lambda写函数？
平方=lambda x:x**2 #lambda 参数：返回值
print(平方(5))

# ==========================================================
# 主菜  把今天的几样东西串起来：summarize(text)
#   要求写一个函数，输入一段文字，一次性返回三样东西：
#     1) 总字数
#     2) 不同字的个数
#     3) 出现次数最多的 3 个字
#   关键点：一个函数要返回多个值时，把几个值一起写在 return 后面，
#           外面接收的时候也用几个变量一起接——这叫做「拆包」，
#           你在元组那题里已经见过了。
#   写完后：
#     total, distinct, top3 = summarize(text)
#     print(total, distinct, top3)
#   自查：这段文本总字数 18，不同字 7，
#         出现最多的三个都是 3 次（四个字并列，谁被选中不唯一）。
# ==========================================================

text = "宁德时代比亚迪宁德时代比亚迪宁德时代"

# TODO 主菜
#参考AI
def summarize(text):
   counts=count_chars(text)
   total=len(text)
   distinct=len(counts)
   top3=sorted(counts.items(), key=lambda kv:kv[1], reverse=True)[:3]
   return total,distinct,top3
total,distinct,top3=summarize("宁德时代比亚迪宁德时代比亚迪宁德时代")
print(total,distinct,top3)
# ==========================================================
# 收尾
#   1) 用一句话回答自己：什么时候该 return，什么时候直接 print
#   2) 编辑 规划/两周计划-0914至0927.md，把已完成的行打勾
#   3) 明天（9.18）预读：文件读写 open / with、异常处理 try / except
# ==========================================================
