# 第 11 次课：性能对比报告 + 小项目 2 验收

| 序号 | 文件 | 做什么 |
| --- | --- | --- |
| 1 | `docs/lesson-11.md` | 阅读 |
| 2 | `src/herodungeon/m2_equip_search/quicksort.py` | 贴入第 9 课实现 |
| 3 | `src/herodungeon/m2_equip_search/benchmark.py` | 实现 `count_comparisons`、`run_sort_benchmark` |
| 4 | `src/herodungeon/m2_equip_search/baseline_sorts.py` | 老师给的冒泡/选择对照，勿改 |
| 5 | `tests/test_benchmark-第11课.py` | 勿改 |

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/test_benchmark-第11课.py
```
