# 第 14 次课：行为树基础（Sequence / Selector）

## 目标

把第 12 课画过的那棵怪物树，写成每帧都能 tick 一遍的引擎。所有节点同一个接口：`tick(ctx)`，只回三种状态之一：`SUCCESS` / `FAILURE` / `RUNNING`。

只改一个文件：`src/herodungeon/m3_behavior_tree/behavior_tree.py`，实现两个组合节点。

## 已经提供（不要改）

- `BehaviorStatus`：三种状态。
- `TickContext`：黑板。`ctx.world` 是共享字典（hp、can_see……），节点读它，不互相打听。
- `Condition(name, predicate)`：只读黑板，立刻回 SUCCESS 或 FAILURE。
- `Action(name, effect=None)`：改世界，写 `world["last_action"]`，可以回 RUNNING。
- `_emit(ctx, node, status, kind)`：记录一条 `tick` 事件并返回状态。

## 你要实现

### `Sequence.tick`（AND，排队做事）

1. 先记 `enter` 事件（`node`、`kind="sequence"`）。
2. 从左到右 tick 每个孩子。
3. 某个孩子不是 SUCCESS（FAILURE 或 RUNNING），**立刻**用 `_emit` 记录并把这个状态往上返回，右边的孩子不再问（短路）。
4. 全部成功：`_emit` 记录并返回 SUCCESS。没有孩子时也是 SUCCESS。

### `Selector.tick`（OR，找一条能走的）

和 Sequence 对称，只改一个判断：

1. 先记 `enter`（`kind="selector"`）。
2. 从左到右 tick；某个孩子不是 FAILURE（SUCCESS 或 RUNNING），立刻记录并返回。
3. 全部失败：记录并返回 FAILURE。没有孩子时也是 FAILURE。

### RUNNING

必做：孩子回 RUNNING 时原样往上传，并停下。

选做（不测）：在节点里记 `running_index`，下一帧直接从挂起的孩子继续，SUCCESS / FAILURE 时清掉。

## 课件「最小可跑树」和三组必测黑板

```text
Selector root
├── Sequence flee_seq   → is_hp_low?（hp < 30）, flee
├── Sequence fight_seq  → can_see_hero?, attack
└── patrol
```

| 黑板 | 应该走 |
| --- | --- |
| hp=20, can_see=True | flee |
| hp=80, can_see=True | attack |
| hp=80, can_see=False | patrol |

hp=80、can_see=True 时，`tick` 事件依次是：`is_hp_low` 失败 → `flee_seq` 失败 → `can_see_hero` 成功 → `attack` 成功 → `fight_seq` 成功 → `root` 成功。状态从叶子冒到根。

和第 12 课对照：`enter` 事件的顺序就是走到的组合节点的前序；`tick` 事件像后序：孩子先回结果，父亲最后决定。

## 本课不做

真实怪物叶子（视野距离、血量比例、巡逻移动、`simulate`）是第 15 次课的内容，不要现在写 `monster_ai.py`。

## 机房流程（90 分钟）

1. 接口对齐（10 分钟）：读本文件，看懂 `TickContext`、`Condition`、`Action`、`_emit`。
2. Seq / Sel 图 + 伪代码（25 分钟）：跟着课件把两段 for 循环对上图。
3. 编码（35 分钟）：只写 `Sequence.tick`、`Selector.tick`，先让三组黑板测试变绿。
4. 测试（15 分钟）：跑全部测试；挂了先看 `tick` 事件顺序。
5. 选做 RUNNING（5 分钟）：`running_index`。

## 提交

```bash
pytest tests/test_behavior_tree-第14课.py
```

17 个测试全绿后提交：`git commit -m "feat(m3): behavior tree engine with tick"`，推到自己的仓库。

截止与计分（建议）：

- 截止：当堂完成；没做完的第 15 次课上课前补交（第 15 课的怪物要用这套引擎）。
- 计分：计入小项目 3「行为树引擎」一项，第 16 次课验收时一起看。
