# 第 6 次课：滑动窗口

## 目标

在伤害日志里找出长度为 `k` 的最高伤害区间。要用滑动更新，不要每个窗口都重新求和。

## 必须满足的行为

1. `size <= 0` 或大于日志长度时抛出 `ValueError`。
2. 先计算第一个窗口，记录 `window_init`。
3. 窗口右移时：减去离开的数，加上进入的数，记录 `window_slide`。
4. 只有新窗口和**严格更大**时才更新最优；平局保留更早的窗口。
5. 结束时记录 `window_best`，返回 `(start_index, window_sum)`。
6. `window_states` 给出每一扇窗口的 `start` / `end` / `values` / `window_sum`。

## 提交

```bash
pytest tests/test_sliding_window-第6课.py
```
