# 第 4 次课：队列调度

本包只含第 4 次课。教师答案不在这里。

## 文件分工

| 序号 | 文件 | 你要做什么 |
| --- | --- | --- |
| 1 | `00-请先读我.txt` | 先看顺序 |
| 2 | `docs/lesson-04.md` | **阅读**：FIFO，禁止 `list.pop(0)` |
| 3 | `src/herodungeon/m1_inventory/queue.py` | **修改** |
| 4 | `tests/test_queue-第4课.py` | **不要改** |
| 5 | `src/herodungeon/core/` | **不要改** |

## 验收

需要 Python 3.11+。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/test_queue-第4课.py
```

Windows：`.venv\Scripts\activate`。
