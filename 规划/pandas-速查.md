# pandas 速查表（自己填）

> 用途：忘了写法时翻这一页。
> **填法**：先把右边一列盖住，凭记忆写左边；写完再对照代码里的实际用法。
> 自己写一遍，比看十遍别人整理的表格有用。
> 来源：`代码/week03/day12` – `day17`。

---

## 一、读与写

| 要做什么 | 写法（自己填） |
| --- | --- |
| 读 CSV，并让「代码」列保持文本 | `pd.read_csv(path, encoding="utf-8", dtype={"代码": str})` |
| 存 CSV，不要行号、Excel 打开不乱码 | `df.to_csv("x.csv", index=False, encoding="utf-8-sig")` |
| 让路径跟着脚本走，不怕运行目录 | `BASE = Path(__file__).parent` |

## 二、看数据（六个命令）

| 要做什么 | 写法 |
| --- | --- |
| 前 5 行 | df.head(5)|
| 多少行多少列 | df.shape|
| 有哪些列 | df.columns|
| 每列什么类型 | df.dtypes |
| 一次看全（行列、类型、非空个数） | df.info|
| 数值列统计摘要 | df.describe|

## 三、选列

| 要做什么 | 写法 |
| --- | --- |
| 选一列（得到 Series） | df["收盘价"]|
| 选多列（得到 DataFrame） |df[["代码","收盘价","市盈率"]] |
| 只看某几列，用变量存列名列表 | cols=["代码","名称","收盘价"] df[cols]|

## 四、筛选

| 要做什么 | 写法 |
| --- | --- |
| 单条件筛选 | df[df["涨跌幅"]>0] |
| 两个条件同时满足 | df[(df["市盈率"]<30)&(df["涨跌幅"]>0)]|
| 满足任一条件 | df[(df["市盈率"]<30) | (df["涨跌幅"]>0)] |
| 取反 | df[~(df["名称"]=="贵州茅台")] |
| 值在某个名单里 | df[df["名称"].isin(["贵州茅台","比亚迪","五粮液"])]|

## 五、排序与取前几名

| 要做什么 | 写法 |
| --- | --- |
| 按一列排序 | df.sort_values("收盘价",ascending=True)|
| 按多列排序（方向不同） | df.sort_values(["行业","收盘价"], ascending=[True,False])|
| 取最大的 3 行 / 最小的 3 行 | df.nlargest(3,"成交额")/df.nsmallest(3,"市盈率")|

## 六、loc 与 iloc

| 要做什么 | 写法 |
| --- | --- |
| 按标签取一行 | df.loc[3] |
| 按位置取一行 | df.iloc[3] |
| 切片时含右端 / 不含右端 | df.loc[0:2] /df.iloc[0:2]|
| 按「代码」直接取行 | df.set_index("代码").loc["567899"]|
| 取某个格子 | df.loc[0,"名称"]/df.iloc[0,1]|

## 七、缺失值

| 要做什么 | 写法 |
| --- | --- |
| 每列缺几个 | df,isna(),sum()|
| 每列缺失比例 | (df.isna().mean()*100).round(2)|
| 找出某列缺失的行 | df[df["某列"].isna()]|
| 删掉某列缺失的行 | df.dropna(subset=["某列"])|
| 填中位数 | df["某列"].fillna(df["某列"].median())|
| 用上一个值填 | df["某列"].ffill()|

## 八、分组聚合

| 要做什么 | 写法 |
| --- | --- |
| 按行业求平均 | df.groupby("行业").mean(numeric_only=True)|
| 一列算多个统计量 | df.groupby("行业")["市盈率"].agg(["mean","max","count"])|
| 不同列用不同函数 | df.groupby("行业").agg({"市盈率":"mean","涨跌幅":"std","成交额":"sum"})|
| 每组几行 |df.groupby("行业").size() |
| 只看某一组 | df.groupby("行业").get_group("非银金融")|
| 结果铺回原表（每行一个组内统计量） | df["行业中位市盈率"]=df.groupby("行业")["市盈率"].transform("median")|
| 按固定阈值分档 / 按数量分档 |pd.cut(df["市盈率"], bins=[0，15，30，100], labels=["低估值","中估值","高估值"])  / pd.qcut(df["市盈率"], q=3)|

## 九、合并与拼接

| 要做什么 | 写法 |
| --- | --- |
| 按代码横向合并两张表（以左表为准） | pd.merge(表1,表2, on="代码", how="left")|
| 只保留两边都有的 |pd.merge(表1,表2, on="代码", how="inner") |
| 上下拼接两张结构相同的表 | pd.concat([上半,下半], ignore_index=True)|
| 指定重名列的后缀 | pd.merge(表1,表2, on="代码", suffixes=("_名单","_行情"))|

## 十、时间序列（周日填）

| 要做什么 | 写法 |
| --- | --- |
| 把字符串日期转成时间类型 | pd.to_datetime(df["日期"])|
| 用日期当行索引 | df.set_index("日期")|
| 按月重采样求均值 | df.resample("ME").mean()|

---

## 我踩过的坑（从易错点清单里挑 pandas 相关的抄过来）

- 编号列不指定 dtype → 前导零丢失（000858 变 858）
- sort_values 不接返回值 → 排序没生效
- 从原表切出来的副本改了不影响原表（pandas 3 的 copy-on-write），且不报警告
- merge 两边连接键类型不一致 → ValueError
- sum() 把全是 NaN 的组算成 0 → 看起来像「零涨跌」
- 多条件筛选忘了加括号 / 用了 and
