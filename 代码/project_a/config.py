"""项目 A 的共享路径配置。"""

from pathlib import Path

BASE_DIR = Path(__file__).parent
SOURCE_DATA_DIR = BASE_DIR.parent / "week04" / "data"
OUTPUT_DIR = BASE_DIR / "data"

OUTPUT_DIR.mkdir(exist_ok=True)

HISTORICAL_DAILY_PATH = OUTPUT_DIR / "historical_daily.csv"

SIGNAL_START = "2025-01-01"
SIGNAL_END = "2025-10-17"
