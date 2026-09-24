# day08_csv_stats.py ｜ 2026.9.19 周六傍晚（1h+）：CSV 统计脚本（本周硬交付物）
#
# 运行方式：
#   cd 金融科技学习/代码/week01
#   python3 day08_csv_stats.py
#
# 数据文件：hs300_sample.csv（就在同一个目录里）
#   12 行数据，字段是 代码 / 名称 / 收盘价 / 涨跌幅 / 市盈率 / 成交额
#   里面故意留了几个空格子，那是缺失值——真实数据永远有缺失，
#   这份小数据就是让你在安全的环境里先练一遍怎么处理它们。
#
# 今天要交的东西：
#   一个能读 CSV、数出多少行、每列缺几个、数值列平均多少的脚本，
#   最后打印成一张表。
#
# 提醒：这一步只用 Python 自带的 csv 模块，不碰 pandas。
#       pandas 是十月份的事，现在用基础工具把逻辑走通，
#       以后换成 pandas 你会发现只是换了写法，思路一模一样。


# ==========================================================
# 题 1  先用最原始的方式看一眼 CSV 长什么样
#   用 import csv 引入模块，用 csv.reader 打开文件。
#   注意第一行是表头（列名），后面每一行才是数据。
#   要求：打印表头，再打印前两行数据，看看每行是什么形状。
#   你会看到每一行是一个列表，像 ['600519', '贵州茅台', '1680.5', ...]
#   小提示：想只取第一行，用 next(reader)
# ==========================================================

# TODO 1
import csv
with open("代码/week01/hs300_sample.csv", "r", encoding="utf-8") as f:
    reader=csv.reader(f)
    header=next(reader) #取第一行（表头）
    print(header)
    print(next(reader))
    print(next(reader))




# ==========================================================
# 题 2  换成 DictReader，每行变成字典
#   用 csv.DictReader，它会把表头当键，每行数据变成一个字典。
#   要求：打印第一行，看看它长什么样，应该是
#     {'代码': '600519', '名称': '贵州茅台', ...}
#   这一步的意义：后面你要按列名取值，写 row["收盘价"] 比记「第几列」
#   清楚得多。这就是字典为什么值得学。
# ==========================================================

# TODO 2
import csv
with open("代码/week01/hs300_sample.csv", "r", encoding="utf-8") as f:
    reader=csv.DictReader(f)
    print(next(reader))

# ==========================================================
# 题 3  数一数有多少行数据
#   要求：打印数据行数，注意不含表头。
#   自查：应该是 12 行。
#   做法提示：DictReader 可以像列表一样一次性转出来，也可以边读边数。
# ==========================================================

# TODO 3
#参考AI
import csv
with open("代码/week01/hs300_sample.csv", "r", encoding="utf-8") as f:
    reader=csv.DictReader(f)
    count=0
    for row in reader:
        count=count+1
    print(count)
#卡住：怎么打印行数

import csv
with open("代码/week01/hs300_sample.csv", "r", encoding="utf-8") as f:
    reader=csv.DictReader(f)
    rows=list(reader) #把剩下所有的行一次性装进列表里
    print(rows)
    print(len(rows))

# ==========================================================
# 题 4  统计每一列有几个缺失值
#   规则：某个格子里是空字符串，就算这一行的这一列缺失。
#   要求：对每一列，打印出「列名 + 缺了几个」。
#   自查：
#     代码 0、名称 0、收盘价 0
#     涨跌幅 3、市盈率 2、成交额 1
#   做法提示：用一个字典记「列名 → 缺失个数」，
#            遍历每一行、每一列，遇到空字符串就给这个列名加一。
#            这就是你在 day03 写过的字频累加，只是把「字」换成了「列名」。
# ==========================================================

# TODO 4
import csv
with open("代码/week01/hs300_sample.csv", "r", encoding="utf-8") as f:
    reader=csv.DictReader(f)
    rows=list(reader)

所有列=["代码","名称","收盘价","涨跌幅","市盈率","成交额"]

missing={}
for col in 所有列:
    missing[col]=0

for row in rows:
    for col,value in row.items():
        if value=="":
            missing[col] +=1

print(missing)
        

#卡住：如何遍历空字符

          


# ==========================================================
# 题 5  对数值列求均值
#   数值列是：收盘价、涨跌幅、市盈率、成交额。
#   两个坑：
#     一是空字符串不能直接转成数字，必须先跳过它
#        （这一列参与计算的行数会变少，这是正常的）
#     二是从 CSV 读出来的数字是字符串，要转成 float 才能算
#   要求：对四个数值列，各打印出列名和均值，保留两位小数。
#   自查：
#     收盘价 209.83（12 行参与）
#     涨跌幅 0.28（9 行参与）
#     市盈率 22.38（10 行参与）
#     成交额 26.43（11 行参与）
#   做法提示：把「参与计算的行数」也打印出来，这能帮你确认
#            自己是不是真的跳过了缺失值，而不是把 0 算进去了。
# ==========================================================

# TODO 5
#参考AI
import csv
with open("代码/week01/hs300_sample.csv", "r", encoding="utf-8") as f:
    reader=csv.DictReader(f)
    rows=list(reader)
数值列=["收盘价","涨跌幅","市盈率","成交额"]


for col in 数值列:
    values=[]
    for row in rows:
        v=row[col]
        if v=="":
            continue
        values.append(float(v))       
                
    avg=sum(values)/len(values)
    print(f"{col} {avg:.2f} {len(values)}")





# ==========================================================
# 题 6  打印成一张表
#   把前面的结果整理成三列：列名 / 缺失个数 / 均值（非数值列留空）
#   打印的时候排整齐，像这样：
#     列名       缺失     均值
#     代码          0
#     收盘价        0   209.83
#   提示：f-string 里可以用 :<10 表示左对齐占 10 格，:>8 表示右对齐占 8 格
# ==========================================================

# TODO 6
#卡住：参考AI
import csv
with open("代码/week01/hs300_sample.csv", "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

# 两份列名清单
所有列 = ["代码", "名称", "收盘价", "涨跌幅", "市盈率", "成交额"]
数值列 = ["收盘价", "涨跌幅", "市盈率", "成交额"]

# ① 缺失值统计：所有列先归零，再扫空值 +1
missing = {}
for col in 所有列:
    missing[col] = 0
for row in rows:
    for col, value in row.items():
        if value == "":
            missing[col] += 1

# ② 数值列均值：一列一列算，存进字典
均值 = {}
for col in 数值列:
    values = []
    for row in rows:
        v = row[col]
        if v == "":
            continue
        values.append(float(v))
    均值[col] = sum(values) / len(values)

# ③ 打印表：表头 + 逐行，数值列带均值，非数值列留空
print(f"{'列名':<10}{'缺失':>8}{'均值':>12}")
for col in 所有列:
    m = missing[col]
    if col in 均值:
        print(f"{col:<10}{m:>8}{均值[col]:>12.2f}")
    else:
        print(f"{col:<10}{m:>8}{'':>12}")



# ==========================================================
# 主菜  把整件事封装成函数 analyze_csv(path)
#   要求：
#     1) 输入一个 CSV 路径，返回统计结果
#        （建议返回一个字典：行数 + 每列缺失 + 每列均值）
#     2) 文件不存在时不许崩，打印一句提示并返回 None
#        （用 day06 学的 try / except FileNotFoundError）
#     3) 最后调用这个函数，把结果打印成上一步那张表
#   两个测试：
#     analyze_csv("hs300_sample.csv")     正常出结果
#     analyze_csv("没有这个文件.csv")      打印提示、不崩
#   加分：
#     - 在函数和关键步骤上写注释，说清「为什么这么做」，
#       这是给下周的自己看的，也是面试时能讲出口的东西
#     - 想一个坑：代码这一列看着也是数字（600519），
#       但它应不应该被当成数值列、去算平均值？如果让程序
#       自动判断「能转成数字就是数值列」，会发生什么？
#       把这个坑写进你的注释里，这是真实数据里的经典问题。
#   交付标准：这个脚本能一把跑通、输出那张表，就算完成交付物 1
# ==========================================================

# TODO 主菜

def analyze_csv(path):
    try:
        with open(path,"r", encoding="utf-8") as f:
            reader=csv.DictReader(f)
            rows=list(reader)
        
    
    except FileNotFoundError:
        print("没有此文件")
        return None

    所有列=["代码", "名称", "收盘价", "涨跌幅", "市盈率", "成交额"]
    missing = {}
    for col in 所有列:
        missing[col] = 0
    for row in rows:
        for col, value in row.items():
            if value == "":
                missing[col] += 1

# ② 数值列均值：一列一列算，存进字典
    均值 = {}
    for col in 数值列:
        values = []
        for row in rows:
            v = row[col]
            if v == "":
                continue
            values.append(float(v))
        均值[col] = sum(values) / len(values)

    return {"行数":len(rows),"缺失":missing,"均值":均值}
 

r1=analyze_csv("代码/week01/hs300_sample.csv")
r2=analyze_csv("代码/week01/没有这个文件.csv")
print(r1)
print(r2)

# ==========================================================
# 收尾
#   1) 把 规划/计划-0918至1011.md 里今天剩下的条目打勾
#   2) 明天（9.20 周日）：刷题 25 道 + 注册 GitHub 把代码推上去
#   3) 明天晚上记得让我出今天这份「类与 CSV」的总结
# ==========================================================
