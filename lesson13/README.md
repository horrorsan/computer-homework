# 第 13 次课发放

更新：2026-10-08（按 v9：第 8 周理论课，0-1 背包 DP 原理；附带手填表作业）
课型：理论（M3-2），主讲苏伯超，教室 B04-07

课堂 PPT：`M3-2_01背包动态规划原理_第13次课课件_10082026.pptx`
（下载后复制进本目录，用 Desktop 提交）

## 学生要做的

只改一个文件：

`src/herodungeon/m3_behavior_tree/dp_basics.py`

实现两个函数：

- `fill_table`：整张 (n+1)×(W+1) 表，每格 = max(不拿, 拿)
- `greedy_by_ratio`：按性价比贪心，用来看它在 A/B/C、W=50 上只拿到 160

穷举 `brute_force_best`、`best_value` 和课件数据已提供，不要改。不要改 `tests/`。事件、反推、装备版选装都是第 16 次课的内容。

截止与计分（建议）：第 16 次课上课前提交；不单独计分，计入「课堂参与 + Git 习惯」，并作为第 16 次课 DP 实现的前置检查。

```bash
cd handouts/第13课
sh pack.sh
```
