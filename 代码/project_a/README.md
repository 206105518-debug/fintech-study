# 项目 A：动量与质量因子原型

本目录使用当前沪深 300 成分股，构造 6-1 动量和 point-in-time ROE，
完成横截面标准化、Q1–Q5 分组和初版收益统计。

## 数据依赖

输入来自 `代码/week04/data/`：

- `clean_daily.csv`
- `clean_financial.csv`
- `clean_valuation.csv`

## 运行顺序

```bash
cd 代码/project_a

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
| `build_trade_calendar.py` | 生成月末信号日、建仓日和平仓日 |
| `build_monthly_returns.py` | 使用下一交易日开盘价计算持有期收益 |
| `build_factor_panel.py` | 计算 6-1 动量并合并未来收益 |
| `build_roe_panel.py` | 按可用日匹配 ROE，生成标准化得分和五分组 |
| `run_backtest.py` | 构造 Q5 等权组合，计算换手、交易成本和扣费后收益 |

## 当前约束

- 只有当前沪深 300 名单，存在幸存者偏差。
- 当前估值只有快照，价值因子尚未实现。
- 日线仅覆盖 2025 年，当前使用 6-1 动量替代标准 12-1。
- 最终只有两个有效因子收益截面，不能据此判断因子长期有效。
