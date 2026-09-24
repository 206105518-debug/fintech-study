# day06_file_io.py ｜ 2026.9.18 周五（计划内容：文件读写 + 异常处理）
#
# 今天的规矩：
#   1. 前 40 分钟看和学，后 80 分钟动手敲
#   2. 写一段跑一次，看到输出再往下写
#   3. 卡住 30 分钟就注释「卡住：xxx」跳过
#   4. 运行方式：python3 day06_file_io.py
#
# 今天为什么重要：
#   前面几天所有数据都是你写在代码里的。真实工作里数据在文件里——
#   几百 MB 的行情表、几万行贷款记录。不会读写文件，前面学的一切都用不上。


# ==========================================================
# 题 1  写入文件
#   在 代码/week01/ 下建一个 notes.txt，写入三行内容
#   要点：
#     - 用 open(文件名, "w", encoding="utf-8")
#     - "w" 是写模式，文件不存在会新建，已存在会被清空
#     - 一定要写 encoding="utf-8"，否则中文可能变乱码
#     - 推荐用 with 包起来，代码块结束会自动关闭文件
#     - write 不会自动换行，想换行要自己在字符串末尾写 \n
#   写完后用命令行 ls 看一下，确认文件真的出现了
# ==========================================================

# TODO 1
with open("代码/week01/notes.txt","w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")   
    f.write("第三行\n")


# ==========================================================
# 题 2  读文件：三种读法，看它们各自返回什么
#   a) f.read()       —— 一次性读全部，返回一整个字符串
#   b) f.readlines()  —— 一次性读全部，返回一个列表，每行是列表里的一项
#                       注意：每行末尾带着换行符 \n，看起来会有空行
#   c) for line in f  —— 一行一行读，最适合文件很大时用
#   三种都试一遍，各打印一次，比较它们的结果长什么样
#   小提示：想去掉每行末尾的换行符，用 line.strip()
# ==========================================================

# TODO 2
with open("代码/week01/notes.txt","r",encoding="utf-8") as f:
    content1=f.read()
print(content1)

with open("代码/week01/notes.txt","r",encoding="utf-8") as f:
    c2=f.readlines()
print(c2)

with open("代码/week01/notes.txt","r",encoding="utf-8") as f:
    for line in f:
        print(line.strip())

# ==========================================================
# 题 3  追加写，以及 "w" 和 "a" 的区别
#   a) 用 "a" 模式往 notes.txt 再写一行，然后读回来，确认是在后面接着写的
#   b) 把同一个文件用 "w" 模式打开、什么也不写、直接关闭，再读回来看
#      你会发现内容全没了——这就是 "w" 会清空文件的含义
#   这一步是故意的，让你亲眼看到覆盖的危害：写数据时用错模式，一次就能毁掉原文件
# ==========================================================

# TODO 3 
with open("代码/week01/notes.txt","a",encoding="utf-8") as f:
    f.write("第四行\n")

f=open("代码/week01/notes.txt","w",encoding="utf-8")
f.close()

with open("代码/week01/notes.txt","w",encoding="utf-8") as f:
    f.close()

# ==========================================================
# 题 4  异常处理：让程序遇到问题时不要整个崩掉
#   a) 先不加保护，直接去读一个不存在的文件，运行一次，
#      把报错信息抄进下面这行注释里：
#      报错：
#      （抄完把这行代码注释掉，别让它一直报错）
#   b) 然后用 try / except 把它包起来：
#        try 里写「可能出事的代码」，
#        except 后面写「出事了怎么办」。
#      让它打印一句「文件不存在，先跳过」，而不是崩掉
#   体会这个区别：程序不是不能出错，而是出错之后要能继续往下走。
#   在金融数据里这一点很实在——某只股票停牌、某个接口挂了，
#   脚本应该跳过继续，而不是跑了两小时的管道全白费。
# ==========================================================

# TODO 4
#with open("代码/week02/notes.txt","r",encoding="utf-8") as f:
#   content=f.read()
#FileNotFoundError: [Errno 2] No such file or directory: '代码/week02/notes.txt'

try:
    with open("代码/week02/notes.txt","r",encoding="utf-8") as f:
        content=f.read()
except FileNotFoundError:
    print("文件不存在，先跳过")




# ==========================================================
# 题 5  认识几个最常见的异常名（先猜，再跑一遍验证）
#   下面五段代码各会报什么错？把答案写在每行后面的注释里，然后跑一遍验证：
#     {"a": 1}["b"]         → ？KeyError 字典里没有这个键
#     int("abc")            → ？ValueError 值类型不对，转不成整数
#     1 / 0                 → ？ZeroDivisionError 除以零
#     [1, 2, 3][5]          → ？IndexError 下标越界
#     "abc" + 1             → ？TypeError 字符串不能加数字
#   这几个名字以后你会天天在终端里看到，混个脸熟，
#   报错一出来就知道大概是哪类问题，比一行行 debug 快得多。
# ==========================================================

# TODO 5


# ==========================================================
# 题 6  模块导入
#   a) 用 import math 引入数学库，算一下根号 2
#   b) 用 from math import sqrt 再算一次，体会这两种写法用起来有什么不同
#   c) 引入 random，生成一个 0 到 1 的随机小数，再生成一个 1 到 100 的随机整数
#   d) 引入 datetime，打印今天的日期
#   一句话区别：import 是把整个工具箱搬进来，用的时候要写「工具箱.工具」；
#              from ... import ... 是只拿某一件工具，用的时候直接喊名字。
# ==========================================================

# TODO 6
#参考AI
import math
print(math.sqrt(2))

from math import sqrt
print(sqrt(2))

import random
print(random.random())

import random
print(random.randint(1,100))

import datetime
print(datetime.date.today())
# ==========================================================
# 主菜  把今天三样东西串起来：read_lines(path)
#   要求写一个函数，输入一个文件路径，返回一个列表，
#   列表里每一项是文件中的一行（去掉末尾的换行和空白）。
#   难点在异常：如果这个文件根本不存在，
#   不要让程序崩掉，而是打印一句提示，并返回一个空列表。
#   写法提示：
#     try 里面放「打开并读取」，except FileNotFoundError 里放兜底。
#   写完做两个测试：
#     1) 传 notes.txt，应该拿到你写进去的那几行
#     2) 传一个不存在的文件名，应该打印提示、返回空列表，程序照常结束
#   加分：返回列表那一行能不能用列表推导式写成一行？
# ==========================================================

# TODO 主菜
#卡住：参考AI
with open("代码/week01/notes.txt","w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")   
    f.write("第三行\n")


def read_lines(path):
    try:
        with open(path,"r",encoding="utf-8") as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        print("文件不存在，返回空列表")
        return []
print(read_lines("代码/week01/notes.txt"))
print(read_lines("代码/week02/notes.txt"))


def read_lines(path):
    try:
        with open(path,"r",encoding="utf-8") as f:
            result=[]
            for line in f:
                result.append(line.strip())
            return result
    except FileNotFoundError:
        print("文件不存在，返回空列表")
        return []
print(read_lines("代码/week01/notes.txt"))
print(read_lines("代码/week02/notes.txt"))

# ==========================================================
# 收尾
#   1) 回答自己：为什么推荐用 with，而不是自己 open 再 close
#   2) 在 规划/计划-0918至1011.md 里把今天做完的条目打勾
#   3) 明天（9.19 周六）预读：class、__init__、self，并准备写 CSV 统计脚本
# ==========================================================
