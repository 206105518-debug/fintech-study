# day07_classes.py ｜ 2026.9.19 周六上午（3h）：类与对象
#
# 运行方式：
#   cd 金融科技学习/代码/week01
#   python3 day07_classes.py
#
# 今天为什么要学类：
#   你已经会写函数了，函数是「把动作装起来」。
#   但真实的业务里，数据和动作是长在一起的——
#   一只股票有代码、名称、价格（数据），还有涨跌、描述（动作）。
#   类就是把这些装进同一个盒子，造一次模板，用很多次。
#
#   一句话：函数是给动作起名字，类是给「一类东西」起名字。


# ==========================================================
# 题 1  第一个类
#   定义一个叫 Stock 的类，它有三个属性：code、name、price。
#   再给它一个方法 describe()，打印一句话，例如：
#     600519 贵州茅台 现价 1680.5
#   然后造两个对象（一只茅台、一只宁德时代），各调用一次 describe。
#
#   三个必须知道的事：
#     1) __init__ 是一个特殊方法，在你造对象的时候自动执行，用来塞初始数据
#     2) self 的意思是「这个对象自己」，方法里访问属性都要写 self.xxx
#     3) 定义类时括号里可以先空着，写成 class Stock: 也可以
# ==========================================================

# TODO 1
#参考AI
class Stock:
    def __init__(self, code, name, price):
        self.code=code
        self.name=name
        self.price=price

    def describe(self):
        print(f"{self.code} {self.name} {self.price}")
a=Stock(600589, "茅台",1000)
a.describe()

b=Stock(600509, "宁德时代",1200)
b.describe()


# ==========================================================
# 题 2  属性是可以改的
#   把题 1 里那只茅台的 price 改掉，再调用一次 describe。
#   体会：数据变了，同一个对象打印出来的话就变了，不需要重新造对象。
# ==========================================================

# TODO 2
#参考答案
a.price=1300.0
a.describe()

# ==========================================================
# 题 3  带参数的方法
#   给 Stock 加一个方法 change(percent)，含义是「按百分比涨跌」：
#     价格变成 原来的价格 × (1 + percent / 100)
#   它应该同时做两件事：把 self.price 更新掉，并把新价格返回。
#   然后调用两次试试：一次 +5，一次 -3。
#   体会：方法就是函数，唯一的区别是第一个参数永远是 self，
#         调用的时候不用自己传，Python 会自动把对象塞进去。
# ==========================================================

# TODO 3
#卡住：如何给类加新方法
#参考AI
class Stock:
    def __init__(self, code, name, price):
        self.code=code
        self.name=name
        self.price=price

    def describe(self):
        print(f"{self.code} {self.name} {self.price}")

    def change(self,percent):
        self.price=self.price*(1+percent/100)
        return self.price
a=Stock(600589, "茅台",1000)
a.describe()
#卡住：如何调用
print(f"{a.change(5)}")
print(a.change(-3))

# ==========================================================
# 题 4  两个对象互不影响（这是类最重要的价值）
#   造 a、b 两个对象，改 a 的价格，然后打印 b 的价格，确认它没变。
#   一句话理解：类是模板，对象是按模板做出来的一个个实物。
#   你在实物上动手，不会影响模板，也不会影响另一个实物。
#   这一点在回测里是命根子——两个策略各有各的资金曲线，
#   要是它们共用同一份数据，一个策略的盈亏会串到另一个身上。
# ==========================================================

# TODO 4
#卡住：怎么造对象
class Stock:
    def __init__(self,code,name,price):
        self.code=code
        self.name=name
        self.price=price
    def describe(self):
            print(f"{self.code} {self.name} {self.price}")
    
    def change(self,percent):
        self.price=self.price*(1+percent/100)
        return self.price

a=Stock(1111,"茅台",1200)
b=Stock(2222,"五粮液",1300)

a.change(10)
a.describe()
b.describe()

# ==========================================================
# 题 5  用类把字频统计重写一遍（计划里要求的那个动作）
#   写一个 TextCounter 类：
#     1) __init__(self, text)：把标点和空格去掉，存进 self.clean；
#        顺手统计好每个字的次数，存进 self.counts
#        （这两步就是你在 day03 写过的逻辑，原样搬进来即可）
#     2) total(self)：返回总字数
#     3) distinct(self)：返回不同字的个数
#     4) top(self, n=3)：返回出现次数最多的 n 个，默认三个
#   然后造一个对象，把四个方法都调用一遍打印出来。
#
#   写的时候想一件事：为什么把统计放在 __init__ 里，而不是每次调用
#   total() 都重新算一遍？因为数据一旦装进对象就不会变，
#   初始化时算一次，后面反复用，这是最常见的写法。
# ==========================================================

text = "  宁德时代，比亚迪，宁德时代，比亚迪，宁德时代。"

# TODO 5
#卡住：没有理解到类的写法，最终答案参考AI
class TextCounter:
    def __init__(self,text): #造对象，把统计算好
        t1=text.replace("，","").replace("。","").replace(" ","")
        self.clean=t1
        counts={}
        for ch in t1:
            counts[ch]=counts.get(ch,0)+1
        self.counts=counts  
    
    def total(self): #从self中取结果
        return len(self.clean)
    
    def distinct(self):
        return len(self.counts)

    def top(self,n=3):
        return sorted(self.counts.items(), key=lambda kv:kv[1], reverse=True)[:n]

t=TextCounter("  宁德时代，比亚迪，宁德时代，比亚迪，宁德时代。") #造对象，调用
print(t.total())
print(t.distinct())
print(t.top(3))
    
        


# ==========================================================
# 主菜  给 TextCounter 再加两个能力
#   1) once(self)：返回「只出现过一次」的字，用列表装
#      （提示：遍历 self.counts 的配对，次数等于 1 的留下，可以写成一行）
#   2) summary(self)：返回一句话，把总字数、不同字个数、前三名串起来
#   写完做两件事：
#     a) 用两段不同的文字各造一个对象，验证它们的结果互不影响
#     b) 把 self.counts 单独打印出来，确认它一直在对象里存着
# ==========================================================

text2 = "数据管道数据清洗数据质量"

# TODO 主菜
#卡住：没有特别明白
class TextCounter:
    def __init__(self,text):
        t1=text.replace("，","").replace("。","").replace(" ","")
        self.clean=t1
        counts={}
        for ch in t1:
            counts[ch]=counts.get(ch,0)+1
        self.counts=counts  

    def total(self): #从self中取结果
        return len(self.clean)
                
    def distinct(self):
        return len(self.counts)
            
    def top(self,n=3):
        return sorted(self.counts.items(), key=lambda kv:kv[1], reverse=True)[:n]

    def once(self):
        return [ch for ch,n in self.counts.items() if n==1]

    def summary(self):
        return f"总字数{self.total()}，不同字个数{self.distinct()}，前三名{self.top(3)}"

b=TextCounter("数据管道数据清洗数据质量")
print(b.summary())
print(b.once())
print(b.total())
print(b.top())
print(b.distinct())

t=TextCounter("  宁德时代，比亚迪，宁德时代，比亚迪，宁德时代。")
print(t.total())
print(t.distinct())
print(t.top(3))
print(t.counts)

# ==========================================================
# 收尾
#   1) 回答自己：什么时候该用类，什么时候一个函数就够了
#      （提示：如果一堆数据总是成组出现、还总是一起被处理，就该用类）
#   2) 把 规划/计划-0918至1011.md 里上午那两条打勾
#   3) 傍晚开始：写 CSV 统计脚本，文件是 day08_csv_stats.py
# ==========================================================
