# day06_file_io_answer.py ｜ 参考答案
# 先自己做，卡住 30 分钟以上再来看。看完关掉重敲一遍。


# ---------- 题 1  写入文件 ----------
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("第一行：金融科技\n")
    f.write("第二行：Python 基础\n")
    f.write("第三行：文件读写\n")
# 注意：write 后面不加 \n 的话，三行会连成一行。


# ---------- 题 2  三种读法 ----------
with open("notes.txt", "r", encoding="utf-8") as f:
    content = f.read()
print("read 的结果：")
print(content)
print(f"类型是 {type(content)}，长度 {len(content)}")

with open("notes.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
print("readlines 的结果：")
print(lines)                 # 列表，每项末尾带着 \n

with open("notes.txt", "r", encoding="utf-8") as f:
    print("逐行读的结果：")
    for line in f:
        print(line.strip())   # strip 去掉末尾的换行符


# ---------- 题 3  追加写 vs 覆盖写 ----------
with open("notes.txt", "a", encoding="utf-8") as f:
    f.write("第四行：追加进来的\n")

with open("notes.txt", "r", encoding="utf-8") as f:
    print("追加之后：")
    print(f.read())

with open("notes.txt", "w", encoding="utf-8") as f:
    pass                     # "w" 一打开就清空了，什么也不写

with open("notes.txt", "r", encoding="utf-8") as f:
    print(f"用 w 模式空开一次之后，文件里剩下：[{f.read()}]")


# ---------- 题 4  异常处理 ----------
# with open("不存在.txt", "r", encoding="utf-8") as f:
#     print(f.read())
# 报错：FileNotFoundError: [Errno 2] No such file or directory: '不存在.txt'

try:
    with open("不存在.txt", "r", encoding="utf-8") as f:
        print(f.read())
except FileNotFoundError:
    print("文件不存在，先跳过")


# ---------- 题 5  常见异常名 ----------
# {"a": 1}["b"]   → KeyError         字典里没有这个键
# int("abc")      → ValueError       类型对但值不合法
# 1 / 0           → ZeroDivisionError 除零
# [1, 2, 3][5]    → IndexError       下标越界
# "abc" + 1       → TypeError        类型不匹配（和 add_print 那次是同一类）
for bad in [
    lambda: {"a": 1}["b"],
    lambda: int("abc"),
    lambda: 1 / 0,
    lambda: [1, 2, 3][5],
    lambda: "abc" + 1,
]:
    try:
        bad()
    except Exception as e:
        print(f"{type(e).__name__}: {e}")


# ---------- 题 6  模块导入 ----------
import math
print(f"math.sqrt(2) = {math.sqrt(2)}")

from math import sqrt
print(f"sqrt(2) = {sqrt(2)}")           # 少写一个 math.，但名字容易撞车

import random
print(f"随机小数：{random.random()}")
print(f"1 到 100 的随机整数：{random.randint(1, 100)}")

from datetime import date
print(f"今天：{date.today()}")


# ---------- 主菜  read_lines ----------
def read_lines(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f]     # 顺手用上了列表推导式
    except FileNotFoundError:
        print(f"读不到文件：{path}")
        return []


with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("金融科技\nPython\n数据管道\n")

print(f"读 notes.txt：{read_lines('notes.txt')}")
print(f"读一个不存在的文件：{read_lines('随便一个名字.txt')}")
print("程序照常往下走，没有崩。")
