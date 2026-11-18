# 项目 A：动量与质量因子原型

本目录使用当前沪深 300 成分股，构造 12-1 动量和 point-in-time ROE，
完成横截面标准化、Q1–Q5 分组和初版收益统计。

## 数据依赖

输入来自 `代码/week04/data/`：

- `clean_financial.csv`
- `clean_valuation.csv`

历史行情由本项目单独下载到：

- `data/historical_daily.csv`

## 运行顺序

```bash
cd 代码/project_a

python3 fetch_historical_daily.py
python3 build_trade_calendar.py
python3 build_monthly_returns.py
python3 build_factor_panel.py
python3 build_roe_panel.py
python3 run_backtest.py
```

生成数据保存在 `data/`，属于可重复生成的本地文件，不提交 Git。

## 文件职责

| 文件 | 作用 |
| --- | --- |
| `config.py` | 统一输入、输出路径 |
| `fetch_historical_daily.py` | 下载项目 A 所需的长期历史日线 |
| `build_trade_calendar.py` | 生成月末信号日、建仓日和平仓日 |
| `build_monthly_returns.py` | 使用下一交易日开盘价计算持有期收益 |
| `build_factor_panel.py` | 计算 12-1 动量并合并未来收益 |
| `compare_momentum.py` | 比较 6-1 与 12-1 动量的覆盖和相关性 |
| `build_roe_panel.py` | 按可用日匹配 ROE，生成标准化得分和五分组 |
| `run_backtest.py` | 构造 Q5 等权组合，计算换手、交易成本和扣费后收益 |

## 当前约束

- 只有当前沪深 300 名单，存在幸存者偏差。
- 当前估值只有快照，价值因子尚未实现。
- 历史行情覆盖 2023–2025 年，因子使用标准 12-1 动量。
- 当前有 8 个有效因子收益截面，仍不能据此判断因子长期有效。
