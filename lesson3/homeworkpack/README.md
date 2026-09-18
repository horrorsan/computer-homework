# 第 3 次课：线性表与背包

本压缩包只含第 3 次课。教师答案不在这里。

## 文件分工

| 序号 | 文件 | 你要做什么 |
| --- | --- | --- |
| 1 | `00-请先读我.txt` | 先看顺序 |
| 2 | `docs/lesson-03.md` | **阅读** |
| 3 | `src/herodungeon/m1_inventory/inventory.py` | **修改** |
| 4 | `tests/test_inventory-第3课.py` | **不要改** |
| 5 | `src/herodungeon/core/` | **不要改** |

## 验收

需要 Python 3.11+。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/test_inventory-第3课.py
```

Windows 激活环境用 `.venv\Scripts\activate`。
