# day27_finance_probe.py ｜ 2026.10.29 周四：财务数据源探测
#
# 运行方式：
#   cd 金融科技学习/代码/week05
#   python3 day27_finance_probe.py

import akshare as ak


def try_source(name, fn):
    try:
        d = fn()
        print(f"✅ {name}: {d.shape}")
        print(f"   列：{list(d.columns)[:15]}")
        print(f"   前两行：{d.head(2).to_dict('records')}")
    except Exception as e:
        print(f"❌ {name}: {type(e).__name__}: {str(e)[:70]}")
    print()


if __name__ == "__main__":
    tests = {
        "新浪财务指标": lambda: ak.stock_financial_analysis_indicator(
            symbol="600519", start_year="2024"),
        "同花顺财务摘要": lambda: ak.stock_financial_abstract(symbol="600519"),
        "同花顺指标(按报告期)": lambda: ak.stock_financial_abstract_ths(
            symbol="600519", indicator="按报告期"),
        "新浪利润表": lambda: ak.stock_financial_report_sina(
            stock="sh600519", symbol="利润表"),
    }

    for name, fn in tests.items():
        try_source(name, fn)
