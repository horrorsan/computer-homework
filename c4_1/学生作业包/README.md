# C4-1：三问题分类 + 1D 最小二乘 + GN/LM 步进

| 序号 | 文件 | 做什么 |
| --- | --- | --- |
| 1 | `docs/lesson-c4-1.md` | 阅读 |
| 2 | `src/roslam/c4_1/problems.py` | 实现 `classify_scenario` |
| 3 | `src/roslam/c4_1/weighted_ls.py` | 实现 `weighted_mean_1d` |
| 4 | `src/roslam/c4_1/nonlinear.py` | 实现 `gauss_newton_1d`、`levenberg_marquardt_1d` |
| 5 | `tests/test_*-c4-1.py` | 勿改 |

**边界**：本课不跑 Ubuntu/Noetic 实车；P-Filter / P-Graph / P-Nav 从后续课次开始。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```
