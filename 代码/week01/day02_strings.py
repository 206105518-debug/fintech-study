# day02_strings.py ｜ 2026.9.14 周一（执行周二内容：变量 / 类型 / 字符串）
#
# 今天的规矩：
#   1. 先自己写，写不出来再看同目录的 day02_strings_answer.py
#   2. 卡住 30 分钟就注释一句「卡住：xxx」，往下走，周六回来解决
#   3. 写一段跑一次，在终端里执行：python3 day02_strings.py
#   4. 目标：动手时间 >= 80 分钟


# ==========================================================
# 题 1  变量与数据类型
#   定义 4 个变量：名字(str)、城市(str)、年龄(int)、身高(float)
#   用 type() 打印四个类型，再用 f-string 打印一行自我介绍
#   期望输出类似：
#     <class 'str'> <class 'str'> <class 'int'> <class 'float'>
#     我是 xxx，来自 xxx，今年 22 岁，身高 1.75 米
# ==========================================================

# TODO 1：你的代码写在这里
name="乔静"
city="四川"
age=23
height=1.62
print(type(name),type(city),type(age),type(height))
print(f"我叫{name}，来自{city}，今年{age}岁，身高{height}米")

name=input(str)
city=input(str)
age=int(input())
height=float(input())
print(type(name))#卡住：type不会用
print(type(city))
print(type(age))
print(type(height))
print(f"我叫{name}，来自{city}，今年{age}岁，身高{height}米")

#根据答案自己又写了一遍
name="乔静"
city="北京"
age=23
height=1.62
print(type(name),type(city),type(age),type(height))
print(f"我叫{name}，来自{city}，今年{age}岁，身高{height}米")
# ==========================================================
# 题 2  类型转换
#   a) "3.14" 转 float，"2026" 转 int
#   b) 把年龄拼进句子，分别用 + 和 f-string 各写一次
#   c) 打印 3.14 * 2 和 "3.14" * 2，然后用一句话注释解释为什么结果不同
# ==========================================================

# TODO 2
a="3.14"
b="2026"
c=float(a)
d=int(b)
print("今年是"+str(d)+"年")
print(f"今年是{d}年")
print(c*2)
print(a*2)

#卡住：这题的知识点都不太明白
a="3.14"
b=float(a)
c="2026"
d=int(c)
print("我今年"+str(d)+"岁")
print(f"我今年{d}岁")
print(a*2) #a是字符串，a*2是重复两次字符串的内容
print(b*2) #b是浮点型数字，b*2是数字乘二


# ==========================================================
# 题 3  字符串常用方法
#   a) strip() 去掉两端空格
#   b) split() 切成词，再用 join() 拼成 "Python|是|数据分析|..."
#   c) count() 数 "Python" 出现几次，find() 找它第一次出现的位置
#   观察：split() 不带参数时，连着几个空格会被当成一个分隔符
# ==========================================================

sentence = "  Python 是  数据分析  的 基础 工具，Python 很好用  "

# TODO 3
sentence = "  Python 是  数据分析  的 基础 工具，Python 很好用  "
s1=sentence.strip()
word=s1.split()
s2="｜".join(word)
num=s1.count("Python")
place=s1.find("Python")
print(s1)
print(word)
print(s2)
print(num)
print(place)

sentence = "  Python 是  数据分析  的 基础 工具，Python 很好用  "
sentence1=sentence.strip()
print(sentence)
print(sentence1)
sentence2=sentence.split()
print(sentence2)
sentence3="｜".join(sentence2)#卡住：join用法不清楚
print(sentence3)
print(sentence.count("Python"))
print(sentence1.find("Python"))
# ==========================================================
# 题 4  动手小项目（今天的主菜，别跳过）
#   一句话先写死，别用 input()：
#     text = "金融科技是用数据和技术改造金融业务的方向"
#   然后依次做四件事：
#     1) 去掉标点和空格，得到干净的字符串
#     2) 反转整句话
#     3) 打印总字数 len() 和不同字的个数 len(set())
#     4) 加餐：打印出现次数最多的 3 个字（提示：字典记数 + sorted）
# ==========================================================

text = " 金融科技，是用数据和技术改造金融业务的方向。 "

# TODO 4
text = " 金融科技，是用数据和技术改造金融业务的方向。 "
t1=text.replace("，","").replace(" ","").replace("。","")
t2=t1[::-1]
print(t1)
print(t2)
print(len(t1))
print(len(set(t1)))

text = " 金融科技，是用数据和技术改造金融业务的方向。 "
text1=text.replace("，","").replace("。","").replace(" ","")
print(text1)
#卡住：如何反转？
text2=text1[::-1]
number1=len(text1)
number2=len(set(text1))
print(f"反转整句话后:{text2}")
print(f"总字数是：{number1}")
print(f"不同字的个数是：{number2}")

#卡住：第四个问题好难



# ==========================================================
# 收尾（写完后做）
#   1) 把今天四道题都在终端跑通，截图或复制输出留档
#   2) 编辑返回上一级目录，确认 规划/ 里的 09.14 那行打勾
#   3) 明天（9.15）预读：列表、元组、字典、集合
# ==========================================================
