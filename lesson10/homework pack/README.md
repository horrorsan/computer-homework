# 第 10 次课：二分 + 哈希索引 + 相似 Top-K

| 序号 | 文件 | 做什么 |
| --- | --- | --- |
| 1 | `docs/lesson-10.md` | 阅读 |
| 2 | `src/herodungeon/m2_equip_search/binary_search.py` | `lower_bound_by` + `binary_search_by` |
| 3 | `src/herodungeon/m2_equip_search/hashing.py` | 只改 `get` |
| 4 | `src/herodungeon/m2_equip_search/topk.py` | 只改 `top_k_similar` |
| 5 | 三组 `tests/test_*-第10课.py` | 勿改 |

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/test_binary_search-第10课.py tests/test_hashing-第10课.py tests/test_topk-第10课.py
```
