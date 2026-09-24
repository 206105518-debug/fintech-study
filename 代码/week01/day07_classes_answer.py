# day07_classes_answer.py ｜ 参考答案
# 先自己做，卡住 30 分钟以上再来看。看完关掉重敲一遍。


# ---------- 题 1  第一个类 ----------
class Stock:
    def __init__(self, code, name, price):
        self.code = code        # 把传进来的 code 存到这个对象身上
        self.name = name
        self.price = price

    def describe(self):
        print(f"{self.code} {self.name} 现价 {self.price}")


moutai = Stock("600519", "贵州茅台", 1680.5)     # 造对象：自动跑 __init__
ningde = Stock("300750", "宁德时代", 210.3)
moutai.describe()
ningde.describe()


# ---------- 题 2  改属性 ----------
moutai.price = 1700.0
print("改价之后：")
moutai.describe()


# ---------- 题 3  带参数的方法 ----------
class Stock2:
    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        self.price = price

    def describe(self):
        print(f"{self.code} {self.name} 现价 {self.price}")

    def change(self, percent):
        self.price = self.price * (1 + percent / 100)
        return self.price


s = Stock2("600519", "贵州茅台", 1680.5)
print(f"涨 5% 之后：{s.change(5):.2f}")
print(f"再跌 3% 之后：{s.change(-3):.2f}")
s.describe()


# ---------- 题 4  两个对象互不影响 ----------
a = Stock2("600519", "贵州茅台", 1680.5)
b = Stock2("300750", "宁德时代", 210.3)

a.change(10)
print(f"a 现在的价格：{a.price:.2f}")
print(f"b 现在的价格：{b.price:.2f}")      # 一点没变


# ---------- 题 5  用类重写字频 ----------
class TextCounter:
    def __init__(self, text):
        self.clean = text.replace("，", "").replace("。", "").replace(" ", "")
        self.counts = {}
        for ch in self.clean:
            self.counts[ch] = self.counts.get(ch, 0) + 1

    def total(self):
        return len(self.clean)

    def distinct(self):
        return len(self.counts)

    def top(self, n=3):
        return sorted(self.counts.items(), key=lambda kv: kv[1], reverse=True)[:n]


text = "宁德时代比亚迪宁德时代比亚迪宁德时代"
c = TextCounter(text)
print(f"总字数 {c.total()}，不同字 {c.distinct()}，前两名 {c.top(2)}")


# ---------- 主菜  再加两个能力 ----------
class TextCounter2:
    def __init__(self, text):
        self.clean = text.replace("，", "").replace("。", "").replace(" ", "")
        self.counts = {}
        for ch in self.clean:
            self.counts[ch] = self.counts.get(ch, 0) + 1

    def total(self):
        return len(self.clean)

    def distinct(self):
        return len(self.counts)

    def top(self, n=3):
        return sorted(self.counts.items(), key=lambda kv: kv[1], reverse=True)[:n]

    def once(self):
        return [ch for ch, n in self.counts.items() if n == 1]

    def summary(self):
        return f"总字数 {self.total()}，不同字 {self.distinct()}，前三名 {self.top()}"


text2 = "数据管道数据清洗数据质量"
c1 = TextCounter2("宁德时代比亚迪宁德时代比亚迪宁德时代")
c2 = TextCounter2(text2)

print("第一个对象：", c1.summary())
print("第二个对象：", c2.summary())
print("只出现一次的字：", c2.once())
print("第一个对象的 counts 还在：", c1.counts)
print("两个对象的 counts 是不同的东西：", c1.counts is not c2.counts)
