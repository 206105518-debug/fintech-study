"""探测百度估值接口的历史数据质量。"""

import akshare as ak

code = "600519"

for indicator in ["市盈率(TTM)", "市净率"]:
    print(f"\n===== {indicator} =====")

    data = ak.stock_zh_valuation_baidu(
        symbol=code,
        indicator=indicator,
        period="近三年",
    )

    print("形状：", data.shape)
    print("列名：", data.columns.tolist())
    print("类型：")
    print(data.dtypes)
    print("\n前五行：")
    print(data.head())
    print("\n后五行：")
    print(data.tail())
    print(
        "日期范围：",
        data["date"].min(),
        "到",
        data["date"].max(),
    )
    print("重复日期：", data["date"].duplicated().sum())