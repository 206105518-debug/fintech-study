"""数据质量报告生成与刷新。"""

import pandas as pd

from pipeline_config import KEYS, data_dir
from pipeline_state import log


def quality_report(tables):
    """计算各表的行数、列数、主键重复数和有缺失的列数。"""
    rows = []

    for name, df in tables.items():
        missing_columns = int((df.isna().sum() > 0).sum())
        rows.append({
            "表名": name,
            "行数": len(df),
            "列数": df.shape[1],
            "主键重复数": int(df.duplicated(subset=KEYS[name]).sum()),
            "有缺失的列数": missing_columns,
        })

    return pd.DataFrame(rows)


def refresh_quality_report():
    """根据当前磁盘文件重新生成数据质量报告。"""
    paths = {
        "名单": data_dir / "constituents_with_industry.csv",
        "日线": data_dir / "clean_daily.csv",
        "估值": data_dir / "clean_valuation.csv",
        "财务": data_dir / "clean_financial.csv",
    }

    if not all(path.exists() for path in paths.values()):
        log("部分结果文件不存在，无法刷新质量报告")
        return False

    tables = {
        "名单": pd.read_csv(paths["名单"], dtype={"代码": str}),
        "日线": pd.read_csv(paths["日线"], dtype={"股票代码": str}),
        "估值": pd.read_csv(paths["估值"], dtype={"代码": str}),
        "财务": pd.read_csv(paths["财务"], dtype={"股票代码": str}),
    }

    report = quality_report(tables)
    report.to_csv(
        data_dir / "data_quality_report.csv",
        index=False,
        encoding="utf-8-sig",
    )
    print(report.to_string(index=False))
    log("数据质量报告已刷新")
    return True