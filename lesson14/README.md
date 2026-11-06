# 第 14 次课发放

更新：2026-10-08（按 v9：第 8 周实践课，BehaviorTree 基础结构）
课型：实践（M3-3），主讲苏伯超，机房 C05

课堂 PPT：`M3-3_行为树引擎_第14次课课件_10082026.pptx`（教师仓 `slides/`）
（下载后复制进本目录，用 Desktop 提交）

## 学生要做的

只改一个文件：

`src/herodungeon/m3_behavior_tree/behavior_tree.py`

实现两个组合节点：

- `Sequence.tick`：AND，遇到非 SUCCESS 立刻返回（短路）
- `Selector.tick`：OR，遇到非 FAILURE 立刻返回（短路）

`BehaviorStatus`、`TickContext`、`Condition`、`Action`、`_emit` 已提供，不要改。不要改 `tests/`。RUNNING 原样往上传即可；`running_index` 选做、不测。真实怪物叶子是第 15 次课。

## 机房流程（90 分钟）

| 阶段 | 时长 | 做什么 |
| --- | --- | --- |
| 接口对齐 | 10 | 读 `docs/lesson-14.md`，看懂黑板、Condition、Action、`_emit` |
| Seq / Sel 图 + 伪代码 | 25 | 跟课件把两段 for 循环对上图 |
| 编码 | 35 | 只写两个 `tick`，先让三组黑板测试变绿 |
| 测试 | 15 | 跑全部 17 个测试，挂了先看 `tick` 事件顺序 |
| 选做 RUNNING | 5 | `running_index` |

## 提交

```bash
pytest tests/test_behavior_tree-第14课.py
git commit -m "feat(m3): behavior tree engine with tick"
```

截止与计分（建议）：当堂完成；没做完的第 15 次课上课前补交。计入小项目 3「行为树引擎」一项，第 16 次课验收时一起看。

```bash
cd handouts/第14课
sh pack.sh
```
