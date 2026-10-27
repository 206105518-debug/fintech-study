# day25_industry_probe.py ｜ 2026.10.27 周二：行业数据源探测
#
# 运行方式：
#   cd 金融科技学习/代码/week05
#   python3 day25_industry_probe.py
#
# 为什么先探测：
#   行业分类不像行情那样有统一接口。不同数据源给的分类体系也不一样
#   （申万一级、申万二级、东财行业、中信行业……），
#   而且东财在你这个网络下一直被拒。
#   先花 1 分钟看清哪个源能通、返回什么，再决定用哪个，比埋头试强。

import akshare as ak


def try_source(name, fn):
    try:
        d = fn()
        print(f"✅ {name}: {d.shape}")
        print(f"   列：{list(d.columns)[:12]}")
        record = d.head(2).to_dict("records")
        print(f"   示例：{record[0] if record else '空表'}")
    except Exception as e:
        print(f"❌ {name}: {type(e).__name__}: {str(e)[:70]}")
    print()


if __name__ == "__main__":
    tests = {
        "东财行业板块": lambda: ak.stock_board_industry_name_em(),
        "申万一级行业": lambda: ak.sw_index_first_info(),
        "申万二级行业": lambda: ak.sw_index_second_info(),
        "新浪行业板块": lambda: ak.stock_sector_spot(indicator="新浪行业"),
        "东财个股信息(600519)": lambda: ak.stock_individual_info_em(symbol="600519"),
        "雪球个股信息(SH600519)": lambda: ak.stock_individual_basic_info_xq(symbol="SH600519"),
    }

    for name, fn in tests.items():
        try_source(name, fn)
