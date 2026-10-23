# 第 12 次课发放

更新：2026-10-08（按 v9：第 7 周理论课，树 + 行为树 + 小项目 3 讲解；附带遍历作业）
课型：理论（M3-1），主讲金洁，教室 B04-07

课堂 PPT：`M3-1_树行为树与小项目3讲解_第12次课课件_10082026.pptx`
（下载后复制进本目录，用 Desktop 提交）

## 学生要做的

只改一个文件：

`src/herodungeon/m3_behavior_tree/tree.py`

实现四个函数：

- `traverse_preorder`
- `traverse_inorder`
- `traverse_postorder`
- `traverse_bfs`

`TreeNode`、`build_dungeon_rooms()`、`build_monster_tree_shape()` 已提供，不要改。不要改 `tests/`。不要提前写 `behavior_tree.py`（第 14 次课）。

怪物树形状只是普通树，用来练遍历、为第 14 次课的行为树铺垫；本课不写 tick。

截止与计分（建议）：第 14 次课上课前提交；不单独计分，计入「课堂参与 + Git 习惯」，并作为小项目 3 的前置检查。

```bash
cd handouts/第12课
sh pack.sh
```
