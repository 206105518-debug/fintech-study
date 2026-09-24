# day08_csv_stats_answer.py ｜ 参考答案（交付物 1）
# 先自己做，卡住 30 分钟以上再来看。看完关掉重敲一遍。

import csv

PATH = "hs300_sample.csv"


# ---------- 题 1  最原始的读法 ----------
with open(PATH, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)          # 第一行是表头
    print("表头：", header)
    for i, row in enumerate(reader):
        print("一行数据：", row)
        if i >= 1:                 # 只看前两行
            break


# ---------- 题 2  DictReader ----------
with open(PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    first = next(reader)
print("转换后的第一行：", first)
print("取收盘价：", first["收盘价"])


# ---------- 题 3  行数 ----------
with open(PATH, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
print(f"数据行数：{len(rows)}")


# ---------- 题 4  每列缺失值 ----------
columns = rows[0].keys()
missing = {}
for col in columns:
    missing[col] = 0                       # 先各记 0
for row in rows:
    for col in columns:
        if row[col] == "":                 # 空字符串就是缺失
            missing[col] = missing[col] + 1

print("每列缺失个数：")
for col, n in missing.items():
    print(f"  {col}: {n}")


# ---------- 题 5  数值列求均值 ----------
numeric_cols = ["收盘价", "涨跌幅", "市盈率", "成交额"]
means = {}
used = {}

for col in numeric_cols:
    values = []
    for row in rows:
        if row[col] != "":                 # 先跳过缺失
            values.append(float(row[col])) # 再转成数字
    means[col] = sum(values) / len(values)
    used[col] = len(values)

for col in numeric_cols:
    print(f"{col}: 均值 {means[col]:.2f}，参与计算 {used[col]} 行")


# ---------- 题 6  打印成一张表 ----------
print()
print(f"{'列名':<8}{'缺失':>6}{'均值':>12}")
for col in columns:
    if col in means:
        print(f"{col:<8}{missing[col]:>6}{means[col]:>12.2f}")
    else:
        print(f"{col:<8}{missing[col]:>6}")


# ---------- 主菜  analyze_csv ----------

# 数值列用一张写死的名单，不靠「能不能转成数字」去猜。
# 原因：代码这一列看着是数字（600519），但它是编号，不是数量。
# 如果按「能转成数字就算数值列」自动判断，代码这一列的均值会算成
# 400779.33 —— 一个毫无意义的数字。真实项目里也是这么做的：
# 哪些列是数值、哪些是文本，由配置或数据字典指定，不靠猜。
NUMERIC_COLS = ["收盘价", "涨跌幅", "市盈率", "成交额"]


def analyze_csv(path):
    """读一个 CSV，返回行数、每列缺失个数、数值列均值。

    为什么用 try 包住：数据文件名写错、文件被移走是常态，
    脚本应该给个提示继续往下走，而不是整段崩掉。
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"读不到文件：{path}")
        return None

    if not rows:
        print(f"{path} 里没有任何数据行")
        return None

    columns = list(rows[0].keys())

    # 每列缺失个数：和字频累加是同一个模式，只是把「字」换成「列名」
    missing = {col: 0 for col in columns}
    for row in rows:
        for col in columns:
            if row[col] == "":
                missing[col] += 1

    # 均值：只算名单里的列，先跳过缺失、再把字符串转成数字
    means = {}
    for col in NUMERIC_COLS:
        values = [float(row[col]) for row in rows if row[col] != ""]
        if values:
            means[col] = sum(values) / len(values)

    return {"行数": len(rows), "缺失": missing, "均值": means}


def print_report(result):
    if result is None:
        return
    print(f"\n数据行数：{result['行数']}")
    print(f"{'列名':<8}{'缺失':>6}{'均值':>12}")
    for col, miss in result["缺失"].items():
        mean = result["均值"].get(col)
        if mean is None:
            print(f"{col:<8}{miss:>6}")
        else:
            print(f"{col:<8}{miss:>6}{mean:>12.2f}")


print("\n=== 交付物：CSV 统计表 ===")
print_report(analyze_csv(PATH))
print("\n=== 文件不存在时 ===")
print_report(analyze_csv("没有这个文件.csv"))
