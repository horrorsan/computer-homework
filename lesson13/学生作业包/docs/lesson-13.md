# 第 13 次课：0-1 背包 DP 原理（理论课附带作业）

## 目标

第 13 次课是理论课：把 0-1 背包的表填明白。课后作业把课上手填的表写成代码，并亲手看到贪心为什么会选错。

只改一个文件：`src/herodungeon/m3_behavior_tree/dp_basics.py`。

## 已经提供（不要改）

- `Item(item_id, name, weight, value)`：`value` 就是课件里的「战力」。
- `brute_force_best(items, capacity)`：穷举全部 2ⁿ 种拿法，作为对照答案。
- `best_value(items, capacity)`：取你那张表右下角的格子。
- 课件数据：
  - `HAND_FILL_ITEMS`：A(重量 2, 战力 3)、B(3, 4)，`HAND_FILL_CAPACITY = 5`
  - `HOMEWORK_ITEM_C`：C(3, 5)（课件课后题：加一件 C，把第 3 行填完）
  - `GREEDY_TRAP_ITEMS`：A(10, 60)、B(20, 100)、C(30, 120)，`GREEDY_TRAP_CAPACITY = 50`

## 你要实现

### `fill_table(items, capacity)`

返回整张表 `dp`：`n + 1` 行、`capacity + 1` 列。

- `dp[i][w]` = 只用前 `i` 件、背包还能装重量 `w` 时，最多能拿到的战力。
- 第 0 行、第 0 列全是 0（多开的一行一列放边界）。
- 第 `i` 行对应 `items[i-1]`。
- 每一格只比较两件事：
  - 不拿：抄上面一格 `dp[i-1][w]`；
  - 拿（装得下才行）：`dp[i-1][w - 重量] + 战力`。
- `capacity < 0` 抛 `ValueError`。

课上那张表应该是：

| i \ w | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- | --- |
| 0 件 | 0 | 0 | 0 | 0 | 0 | 0 |
| A(2,3) | 0 | 0 | 3 | 3 | 3 | 3 |
| B(3,4) | 0 | 0 | 3 | 4 | 4 | 7 |

加上 C(3,5) 之后的第 3 行，先自己在纸上填，再让测试检查。

### `greedy_by_ratio(items, capacity)`

贪心：按「战力 ÷ 重量」从大到小排（一样大时保持原来的顺序），依次看，装得下就拿。返回拿到的装备列表（按拿的先后）。

在 A/B/C、W=50 这组数上：贪心拿 A + B，战力 160；DP 是 B + C，战力 220。这就是贪心选错的反例。

## 本课不做

- 不记录事件，不反推「选了哪几件」，不用装备（`Equipment`）数据。这些在第 16 次课写 `dp.py` 时再做。
- 不要改 `dp.py`。

## 截止与计分（建议）

- 截止：第 16 次课上课前推送到自己的仓库。
- 不单独计分：计入「课堂参与 + Git 习惯」，同时作为第 16 次课 DP 实现的前置检查（第 16 次课前老师跑一次 `pytest tests/test_dp_basics-第13课.py`）。

## 提交

```bash
pytest tests/test_dp_basics-第13课.py
```

14 个测试全绿即可。不要改 `tests/`。
