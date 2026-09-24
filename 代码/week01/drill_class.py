# drill_class.py ｜ 类脱敏练习（不许看 day07 和任何答案，卡住就停下来）
#
# 为什么要做这个文件：
#   你在 day03 写过 count_chars 这个函数，day05 又把它封装成函数，
#   day07 再用类把同一件事包了第三遍。
#   三遍都在做同一件事，而类是「换个写法」——类的价值根本没体现出来，
#   大脑当然记不住一个「多此一举的写法」。
#
#   所以这个练习换个路子：不去重写旧代码，而是让你亲手写一个
#   「用函数写会很别扭、用类写才自然」的东西。
#
# 规矩：
#   1. 每一步都不许看 day07，也不许问 AI
#   2. 写不出来就停在那一行，用注释写下「我卡在哪」，然后告诉我
#   3. 卡点比答案值钱，你卡住的地方就是真正没懂的地方


# ==========================================================
# 第一步（5 分钟）｜只有数据，没有动作
#   写一个 Account 类，__init__ 只干一件事：
#   把传进来的「主人姓名」和「余额」存到这个对象身上。
#   然后造两个对象：
#     a) 你的账户，余额 10000
#     b) 另一个账户，余额 500
#   分别打印两个对象的余额。
#   自查：两个对象打印出来的余额不一样。
# ==========================================================
class Account:
    def __init__(self,name,money):
        self.name=name
        self.money=money
        

a=Account("qiaojing",10000)
b=Account("jiayunlong",500)

print(a.money)
print(b.money)
#卡住：如何造对象并打印


# ==========================================================
# 第二步（10 分钟）｜给对象加一个动作
#   给 Account 加一个 show() 方法，打印一句话：
#     xxx 的账户余额 yyy 元
#   两个对象各调用一次。
#   注意：方法里取余额要写 self.余额，不能只写 余额。
# ========================================================== 

class Account:
    def __init__(self,name,money):
        self.name=name
        self.money=money
        

    def show(self):
        print(f"{self.name}的账户余额{self.money}元")

a=Account("qiaojing",10000)
b=Account("jiayunlong",500)

a.show()
b.show()

# ==========================================================
# 第三步（10 分钟）｜让动作改变对象自己的数据（这一步才是类的价值）
#   再加两个方法：
#     deposit(amount)  —— 余额增加 amount
#     withdraw(amount) —— 余额减少 amount
#   然后照着这个剧本走一遍：
#     先打印余额          应该是 10000
#     存入 2000 再打印     应该是 12000
#     取出 500 再打印      应该是 11500
#   关键体会：**同一个对象，调一次方法，它自己记着的数字就变了。**
# ==========================================================

class Account:
    def __init__(self,name,money):
        self.name=name
        self.money=money

    def show(self):
        print(f"{self.name}的账户余额{self.money}元")

    def deposit(self,amount):
        self.money=self.money+amount

    def withdraw(self,amount):
        self.money=self.money-amount

a=Account("qiaojing",10000)
b=Account("jiayunlong",500)
print(a.money)
a.deposit(2000) #只是方法，不打印东西
print(a.money)
a.withdraw(500)
print(a.money)

# ==========================================================
# 第四步（想明白了再往下走）｜为什么这件事非得用类
#   同样的事只用函数写，会长成这样：
#       balance = deposit(balance, 2000)
#       balance = withdraw(balance, 500)
#   每办一件事，都要把余额递进去、再接回来，稍不留神就传错。
#   而对象自己记着余额，你只要说 account.deposit(2000)。
#
#   一句话：类是「带记忆的函数」，记忆存在对象身上。
#
#   现在回头看 day07 的 TextCounter：
#   它把 clean 和 counts 存在对象里，所以 total()、distinct()、top()
#   不用每次重新算、也不用每次重新传。那一刻类才真有用。
#   把上面这几句想通，再去看那天的代码，感觉会不一样。
# ==========================================================



# ==========================================================
# 第五步（可选，明天做）｜加一开始的流水记录
#   在 __init__ 里加一个 self.记录 = []，
#   每次存款、取款都往里面 append 一条，比如 "存入 2000"。
#   再加一个 history() 方法，把记录逐行打印出来。
#   这一步就是真实系统里的「交易流水」，
#   也是你以后写回测时一定会用到的东西。
# ==========================================================
class Account:
    def __init__(self,name,money):
        self.name=name
        self.money=money
        self.record=[]

    def deposit(self,amount):
        self.money=self.money+amount
        self.record.append(f"存入{amount}")#怎么把存取款写进去
    
    def withdraw(self,amount):
        self.money=self.money-amount
        self.record.append(f"取出{amount}")

    def history(self):
        for 一条 in self.record:
            print(一条)
    

a=Account("qiaojing",10000)
b=Account("jiayunlong",500)
print(a.money)
a.deposit(2000) #只是方法，不打印东西
print(a.money)
a.withdraw(500)
print(a.money) 
b.deposit(100)
a.history()
b.history()


# ==========================================================
# 收尾
#   写完把两个问题回答自己一遍：
#     1) self 到底代表什么？为什么方法里取数据都要写 self.xxx？
#     2) 如果一个东西「算完就完，下次还要重来」，它该写成函数还是类？
#   然后把这份文件发我，我只看你卡住的地方，不看你写得漂不漂亮。
# ==========================================================
