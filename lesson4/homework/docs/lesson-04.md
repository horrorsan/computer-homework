# 第 4 次课：队列调度

## 目标

实现英雄/怪物行动的 FIFO 队列。不要用 `list.pop(0)` 做出队，那是 O(n)。

## 必须满足的行为

1. `enqueue` 把动作放到队尾，记录 `enqueue`。
2. `dequeue` 取出队首；空队列时记录 `underflow` 并抛出 `QueueEmptyError`。
3. 用 `_head` 指向队首，出队后 `_head += 1`，不要每次挪动后面所有元素。
4. 当 `_head > 0` 且 `_head * 2 >= len(_buffer)` 时压缩缓冲区，记录 `compact`。
5. `peek` 只看队首，不删除。
6. `drain` 按 FIFO 顺序清空队列。

## 提交

```bash
pytest tests/test_queue-第4课.py
```
