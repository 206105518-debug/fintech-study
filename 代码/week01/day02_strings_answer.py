# day02_strings_answer.py ｜ 参考答案
# 先自己做，卡住 30 分钟以上再来看这里。看完要关掉重敲一遍，别复制粘贴。


# ---------- 题 1 ----------
name = "qiaojing"
city = "北京"
age = 22
height = 1.75

print(type(name), type(city), type(age), type(height))
print(f"我是{name}，来自{city}，今年{age}岁，身高{height}米")


# ---------- 题 2 ----------
a = float("3.14")
b = int("2026")

with_plus = "我今年" + str(age) + "岁"        # 字符串只能拼字符串，所以要先转
with_fstring = f"我今年{age}岁"                # f-string 会自动转
print(a, b)
print(with_plus, with_fstring)

print(3.14 * 2)      # 6.28      数字：乘法
print("3.14" * 2)    # 3.143.14  字符串：重复两遍
# 解释：同一个 * 号，作用对象类型不同，行为就不同。


# ---------- 题 3 ----------
sentence = "  Python 是  数据分析  的 基础 工具，Python 很好用  "

s = sentence.strip()
words = s.split()

print(f"原始：[{sentence}]")
print(f"strip 后：{s}")
print(f"split 后：{words}，共 {len(words)} 个词")
print("join 后：" + "|".join(words))
print(f"Python 出现 {s.count('Python')} 次")
print(f"Python 第一次出现在第 {s.find('Python')} 个位置（从 0 数起）")
# split() 不带参数时按任意空白切，并且会把连续空格折叠成一个分隔符。


# ---------- 题 4 ----------
text = "金融科技是用数据和技术改造金融业务的方向"

clean = text.replace("，", "").replace("。", "").replace(" ", "")
print(f"去标点后：{clean}")
print(f"反转整句：{clean[::-1]}")
print(f"总字数：{len(clean)}")
print(f"不同字的个数：{len(set(clean))}")

counts = {}
for ch in clean:
    counts[ch] = counts.get(ch, 0) + 1

top3 = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:3]
print(f"出现最多的 3 个字：{top3}")
