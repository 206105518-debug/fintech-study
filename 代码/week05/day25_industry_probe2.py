# day25_industry_probe2.py ｜ 第二层探测：能不能拿到「行业 → 成分股」
#
# 运行方式：
#   cd 金融科技学习/代码/week05
#   python3 day25_industry_probe2.py

import akshare as ak


def try_source(name, fn):
    try:
        d = fn()
        print(f"✅ {name}: {d.shape}")
        print(f"   列：{list(d.columns)}")
        print(f"   前两行：{d.head(2).to_dict('records')}")
    except Exception as e:
        print(f"❌ {name}: {type(e).__name__}: {str(e)[:70]}")
    print()


if __name__ == "__main__":
    tests = {
        # 新浪：某个行业板块的成分股（new_blhy = 玻璃行业）
        "新浪板块成分股": lambda: ak.stock_sector_detail(sector="new_blhy"),
        # 申万：某个指数的成分股（801010 = 农林牧渔）
        "申万指数成分股": lambda: ak.index_component_sw(symbol="801010"),
        # 申万三级行业列表
        "申万三级行业": lambda: ak.sw_index_third_info(),
    }

    for name, fn in tests.items():
        try_source(name, fn)
