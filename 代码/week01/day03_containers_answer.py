# day03_containers_answer.py ｜ 参考答案
# 先自己做，卡住 30 分钟以上再来看。看完关掉重敲一遍。


# ---------- 题 1  列表 ----------
stocks = ["贵州茅台", "宁德时代", "招商银行", "中国平安", "隆基绿能"]

stocks.append("比亚迪")
stocks.insert(1, "中芯国际")
print(f"追加和插入后：{stocks}")

stocks.remove("隆基绿能")
print(f"删掉隆基绿能后：{stocks}，共 {len(stocks)} 个")

print(f"前三个：{stocks[:3]}")
print(f"最后两个：{stocks[-2:]}")
print(f"反转（切片，不改原列表）：{stocks[::-1]}")

stocks.sort()
print(f"原地排序后：{stocks}")
# 中文排序是按字符编码排的，不是按拼音，所以顺序看着有点怪，正常。


# ---------- 题 2  元组 ----------
stock = ("600519", "贵州茅台", 1680.5)

code, name, price = stock
print(f"{code} {name} 现价 {price}")

# stock[2] = 1700.0
# 报错：TypeError: 'tuple' object does not support item assignment
# 元组创建后不能改，改了就报错，这就是「不可变」。

a, b = 1, 2
a, b = b, a
print(f"交换后 a={a} b={b}")
# 右边先算出一个元组 (2, 1)，再拆包给左边，所以不需要第三个变量。


# ---------- 题 3  字典 ----------
prices = {"600519": 1680.5, "300750": 210.3, "600036": 35.8}

prices["601318"] = 48.6
prices["600036"] = 36.9
del prices["300750"]
print(f"现在的字典：{prices}")

print(f"所有键：{list(prices.keys())}")
print(f"所有值：{list(prices.values())}")

for code, price in prices.items():
    print(f"代码 {code} 价格 {price}")

print(f"查 999999 的结果：{prices.get('999999', '查不到')}")
# get() 查不到不会报错，返回默认值；prices["999999"] 会直接报 KeyError。

prices2 = {
    "600519": {"name": "贵州茅台", "price": 1680.5},
    "600036": {"name": "招商银行", "price": 36.9},
}
print(f"600519 的名字：{prices2['600519']['name']}")


# ---------- 题 4  集合 ----------
fund_a = ["贵州茅台", "宁德时代", "招商银行", "中国平安", "贵州茅台"]
fund_b = ["招商银行", "中国平安", "比亚迪", "中芯国际"]

set_a = set(fund_a)
set_b = set(fund_b)
print(f"去重后：{set_a}，共 {len(set_a)} 个")

print(f"共同持有（交集）：{set_a & set_b}")
print(f"两者都有过（并集）：{set_a | set_b}")
print(f"只有 A 有（差集）：{set_a - set_b}")
# 集合最大的用处就是去重和「找共同点」，做因子池、股票池筛选时天天用。


# ---------- 题 5  字频统计 ----------
text = "金融科技是用数据和技术改造金融业务的方向，数据是金融科技的基础"

clean = text.replace("，", "").replace("。", "").replace(" ", "")
print(f"去标点后：{clean}")

counts = {}
for ch in clean:
    counts[ch] = counts.get(ch, 0) + 1
print(f"字频字典：{counts}")

top3 = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:3]
print(f"出现最多的 3 个字：{top3}")

once = [ch for ch, n in counts.items() if n == 1]
print(f"只出现过一次的字：{len(once)} 个，分别是 {once}")
