# 10.12 核心代码总结｜pandas 入门

> 对应代码：`代码/week03/day12_pandas_intro.py`
> 一句话理解 pandas：**Excel 的代码版**。DataFrame 是一张表，Series 是表里的一列。

---

## 一、读文件：路径和类型一次都写对

```python
from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent                      # 这个脚本所在的目录
csv_path = BASE.parent / "week01" / "hs300_sample.csv"

df = pd.read_csv(csv_path, encoding="utf-8", dtype={"代码": str})
```

**两个关键点，都是踩过坑才记住的：**

- `Path(__file__).parent` 让路径跟着脚本走，**从哪个目录运行都能找到文件**。
- `dtype={"代码": str}`：pandas 默认把整列数字读成整数，`000858` 会变成 `858`，
  前导零直接丢掉。**凡是编号（股票代码、身份证号、订单号），都要显式指定成文本。**

---

## 二、看数据：六个命令建立第一印象

```python
df.head()        # 前 5 行，看长什么样
df.shape         # (行数, 列数)
df.columns       # 列名
df.dtypes        # 每列类型：int64 / float64 / object(str)
df.info()        # 行列数、列名、类型、非空个数（看缺失最快）
df.describe()    # 数值列的统计摘要
```
返回字典用 .to_dict()
拿到任何一份数据，先跑这六条。**`info()` 里的非空个数和总行数对不上，就是有缺失。**

---

## 三、Series 与 DataFrame

```python
df["收盘价"]                      # Series：一列，没有列名那一行
df[["代码", "名称", "收盘价"]]     # DataFrame：一张表，双层方括号
```

区别不在写法，在于**拿到手的东西是什么**：Series 只有一列，DataFrame 是一张表。
后面很多报错都是因为拿 Series 当 DataFrame 用（比如 `df["收盘价"]["涨跌幅"]` 必然报错）。

---

## 四、筛选与排序

```python
# 单条件
df[df["涨跌幅"] > 0]

# 多条件：每个条件要加括号，用 & 不用 and
df[(df["市盈率"] < 30) & (df["涨跌幅"] > 0)]

# 排序
df.sort_values("收盘价", ascending=False)

# 取最大/最小的几行
df.nlargest(3, "成交额")
df.nsmallest(3, "市盈率")
```

**两个坑**：多条件里的括号不能省（`&` 的优先级比比较运算高，不写括号会算错）；
必须用 `&`、`|`，不能用 `and`、`or`。

---

## 五、存出去

```python
df.to_csv("picked.csv", index=False, encoding="utf-8-sig")
```

- `index=False`：不把行号存进去，否则会多出一列没用的数字。
- `encoding="utf-8-sig"`：**存 CSV 给 Excel 看时用这个**，不然中文会乱码。
  读的时候用 `utf-8` 就行，写的时候要多一个 `-sig`。

---

## 六、今天和 day08 的对比

同样一件事——读 CSV、数行数、统计每列缺失、算数值列均值：

| | day08 手写版 | pandas 版 |
| --- | --- | --- |
| 代码量 | 八十多行 | 八行 |
| 缺失值 | 自己写循环判断空字符串 | `df.isna().sum()` |
| 区分数值列 | 手写一张列名名单 | `df.mean(numeric_only=True)` |
| 出错点 | 列名拼错、变量被覆盖 | 少得多 |

**手写版是「我在实现统计」，pandas 版是「我在描述需求」。**
数据岗的第一工具是 pandas，因为你的时间应该花在「想清楚要什么」，而不是「怎么把循环写对」。

---

## 七、三条要记住的

1. **编号列必须指定成文本**（`dtype={"代码": str}`），否则前导零会丢。
2. **多条件筛选要加括号、用 `&` 不用 `and`。**
3. **路径用 `Path(__file__).parent` 拼**，从哪个目录运行都不怕。
