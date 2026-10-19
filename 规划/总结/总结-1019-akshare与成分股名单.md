# 10.19 核心代码总结｜akshare 与沪深300成分股名单

> 对应代码：`代码/week04/day19_akshare_intro.py`
> 产出：`代码/week04/data/hs300_constituents.csv`（300 行，代码/名称/交易所）

---

## 一、先体检，再写逻辑

```python
import akshare as ak
df = ak.index_stock_cons_csindex(symbol="000300")
print(df.shape)          # (300, 9)
print(df.columns)        # 日期/指数代码/.../成分券代码/成分券名称/交易所
print(df.head(3))
```

**拿到任何接口，先跑这三行。** 三行就能回答：通不通、多大规模、有哪些列。

---

## 二、看清哪一列是股票代码

这个接口里有两个容易混的列：

| 列名 | 内容 | 特点 |
| --- | --- | --- |
| `指数代码` | `000300` | **300 行全一样**，是沪深300这个指数本身 |
| `成分券代码` | `000001`、`600000`… | 每行不同，才是股票代码 |

**判断方法**：`df["某列"].head()` 看一眼，变化的那列才是你要的。

---

## 三、清洗三件事

```python
名单 = raw[["成分券代码", "成分券名称", "交易所"]].rename(
    columns={"成分券代码": "代码", "成分券名称": "名称"}
).copy()

名单["代码"] = 名单["代码"].astype(str).str.zfill(6)   # 补足 6 位
名单 = 名单.drop_duplicates("代码")                     # 去重
```

代码必须 `zfill(6)`：`000858` 一旦被当成数字就变成 `858`，后面查行情全查不到。

---

## 四、降级：第二个接口要写在第一个的 except 里

```python
try:
    raw = ak.index_stock_cons_csindex(symbol="000300")
    code_col, name_col = "成分券代码", "成分券名称"
except Exception as e:
    print(f"中证接口失败：{type(e).__name__}: {e}，改用新浪接口")
    try:
        raw = ak.index_stock_cons(symbol="000300")
        code_col, name_col = "品种代码", "品种名称"      # 列名不一样
    except Exception as e2:
        print(f"新浪接口也失败：{type(e2).__name__}: {e2}")
        return None
```

**两个 try 写成平级，就不是降级了**——第一个成功也会被第二个覆盖，还多一次请求。
用 `code_col` / `name_col` 记住当前这套列名，后面清洗只写一遍。

---

## 五、落盘与验证

```python
data_dir.mkdir(exist_ok=True)
名单.to_csv(data_dir / "hs300_constituents.csv", index=False, encoding="utf-8-sig")
```

**存完必须回读验证**，我这次的检查清单：

| 检查项 | 正确结果 |
| --- | --- |
| 列名 | 代码 / 名称 / 交易所 |
| 行数 | 300 |
| 代码长度 | 全部 6 位 |
| 交易所分布 | SH 188 / SZ 112 |
| 抽样 600000 | 浦发银行，SH |
| 抽样 000001 | 平安银行，SZ |
| 重复 / 缺失 | 0 / 0 |

**抽样核对是最后一关。** 今天那个 bug（189 只沪市股票被标成 SZ）程序不报错、文件也齐整，只有抽一只 600 开头的才看得出来。

---

## 六、今天踩的四个坑

| 坑 | 表现 | 教训 |
| --- | --- | --- |
| 用错列（`指数代码` vs `成分券代码`） | 300 行全变常数，交易所全错 | 先看列里的值，别只看列名 |
| 两个 try 平级 | 第一个成功也被覆盖，多一次请求 | 降级要嵌套在 except 里 |
| 忘写 f-string 的 f | 打印出 `{len(df)}` 字面量 | 看到花括号原样出现就是忘了 f |
| 改完代码没重跑 | 数据文件还是旧的 9 列 | 改代码 ≠ 改数据，必须重跑验证 |

---

## 七、三条要记住的

1. **接口先体检三行**：shape / columns / head。
2. **代码列必须 `zfill(6)`**，编号不是数量。
3. **存完回读、抽样核对**——不报错不等于对。
