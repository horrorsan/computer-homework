# 第 5 次课：栈与撤销

## 目标

实现有限深度的撤销栈：后进先出。超过 `max_depth` 时丢掉最旧的一条记录。

## 必须满足的行为

1. `push` 把新操作放到栈顶，记录 `push`。
2. 若设置了 `max_depth` 且栈已满，先丢掉最旧项并记录 `evict`，再压入新项。
3. `max_depth` 若提供，必须为正数。
4. `pop` / `peek` 在空栈时记录 `underflow` 并抛出 `StackEmptyError`。
5. `items` 自底向顶；迭代 `for x in stack` 自顶向底。

## 提交

```bash
pytest tests/test_stack-第5课.py
```
