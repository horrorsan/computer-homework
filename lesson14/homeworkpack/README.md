# 第 14 次课：行为树基础（Sequence / Selector）

| 序号 | 文件 | 做什么 |
| --- | --- | --- |
| 1 | `docs/lesson-14.md` | 阅读（含机房流程） |
| 2 | `src/herodungeon/m3_behavior_tree/behavior_tree.py` | 只改 `Sequence.tick`、`Selector.tick`（叶子和黑板已提供） |
| 3 | `tests/test_behavior_tree-第14课.py` | 勿改 |

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/test_behavior_tree-第14课.py
git commit -am "feat(m3): behavior tree engine with tick"
```
