# 第 12 次课：树遍历（理论课附带作业）

## 目标

第 12 次课是理论课：树 + 行为树 + 小项目 3 讲解。课后作业只有一件事：同一棵树，用四种顺序走一遍。

`TreeNode` 用 `children` 列表存孩子（树的存储）。你只写四个遍历函数。

## 已经提供（不要改）

- `TreeNode`、`_emit_visit`
- `build_dungeon_rooms()`：地牢房间树
- `build_monster_tree_shape()`：课件「完整怪物树」的**形状**。它只是普通 `TreeNode`，没有 tick，也没有成功/失败状态；行为树第 14 次课才写。

## 你要实现：`tree.py` 里四个函数

示例树：

```text
A
├── B
│   ├── D
│   └── E
└── C
```

1. 前序 `traverse_preorder`：先根，再从左到右走子树。结果 `A B D E C`。
2. 后序 `traverse_postorder`：先走完全部子树，最后才是根。结果 `D E B C A`。
3. 中序 `traverse_inorder`：先走第一个孩子的子树，再根，再其余孩子。结果 `D B E A C`。
   - 二叉树上就是「左 → 根 → 右」，二叉搜索树会得到从小到大的顺序。
   - 三个及以上孩子时，中序没有统一标准，本课按上面的约定。
4. 层序 `traverse_bfs`：用队列，一层走完再走下一层。结果 `A B C D E`。

## 事件

- 每访问一个节点，用 `_emit_visit` 记一个 `visit`，`order` 填 `preorder` / `inorder` / `postorder` / `bfs`，`depth` 是层深（根为 0）。
- BFS：每个节点出队后，先记 `enqueue_level`（`node`、`depth`、`frontier`），再记 `visit`。`frontier` 是刚出队之后、还没把它的孩子放进队列时的队列长度。
- 遍历不能改动树本身。

## 地牢里的两棵树

房间树：

```text
entrance
├── hall
│   ├── armory
│   └── crypt
│       └── boss
└── garden
```

- 前序：`entrance hall armory crypt boss garden`（进门就登记）
- 后序：`armory boss crypt hall garden entrance`（从最里面的房间往外清）
- 层序：`entrance hall garden armory crypt boss`（离入口一样远的房间一起走）

怪物树形状（为第 14 次课铺垫）：

```text
root (Selector)
├── flee_seq (Seq 逃跑)   → is_hp_low?, flee
├── fight_seq (Seq 战斗)  → can_see_hero?, attack
└── patrol (Patrol)       → wander, wait
```

- 前序就是行为树「从上往下、从左到右问孩子」的顺序。
- 后序是「孩子先回结果，父亲最后决定」。
- 层序按层是 1 / 3 / 6 个节点：根、组合节点、叶子（条件或动作）。

## 截止与计分（建议）

- 截止：第 14 次课上课前推送到自己的仓库。
- 不单独计分：计入「课堂参与 + Git 习惯」，同时作为小项目 3 的前置检查（第 14 次课开始前老师跑一次 `pytest tests/test_tree-第12课.py`）。

## 提交

```bash
pytest tests/test_tree-第12课.py
```

15 个测试全绿即可。不要改 `tests/`，不要提前写 `behavior_tree.py`（第 14 次课）。
