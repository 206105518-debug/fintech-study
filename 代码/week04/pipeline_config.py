"""沪深300数据管道的统一配置。"""

from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent
data_dir = BASE / "data"
data_dir.mkdir(exist_ok=True)

LOG_DIR = BASE / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"pipeline_{datetime.now():%Y%m%d}.log"

INDICATORS = {
    "总市值": "总市值",
    "市盈率(TTM)": "市盈率TTM",
    "市净率": "市净率",
}

CONFIG = {
    "start": "20250101",
    "end": "20251017",
    "max_stocks": None,
    "sleep_sec": 0.3,
}

KEYS = {
    "名单": ["代码"],
    "日线": ["股票代码", "日期"],
    "估值": ["代码"],
    "财务": ["股票代码", "报告期"],
}

MANIFEST_FILE = data_dir / "pipeline_manifest.json"
DAILY_COVERAGE_FILE = data_dir / "daily_coverage.json"
ADJUST = "qfq"

REQUIRED_OUTPUTS = [
    data_dir / "constituents_with_industry.csv",
    data_dir / "clean_daily.csv",
    data_dir / "clean_valuation.csv",
    data_dir / "clean_financial.csv",
    data_dir / "data_quality_report.csv",
]