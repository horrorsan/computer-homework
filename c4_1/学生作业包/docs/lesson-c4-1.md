# C4-1：定位 / 建图 / SLAM 形式化 + 最小二乘速览

## 目标

课后能独立完成三件事（与课堂板书一致）：

1. 根据「已知什么 / 估计什么」判定定位、建图还是 SLAM。
2. 用加权最小二乘算出 1D 两雷达算例。
3. 看懂并实现标量 Gauss-Newton / LM 的一次迭代逻辑。

## 任务 1：`classify_scenario`（`problems.py`）

输入两列字符串集合：`known`、`estimate`。别名需识别：

| 别名 | 归一化 |
| --- | --- |
| `m` / `map` / `地图` | map |
| `x` / `pose` / `位姿` / `轨迹` | pose |
| `z` / `obs` / `观测` / `激光` | obs |
| `u` / `ctrl` / `控制` / `里程计` | ctrl |

判定规则：

- **localization**：已知含 map、不含 pose；估计含 pose、不含 map
- **mapping**：已知含 pose、不含 map；估计含 map、不含 pose
- **slam**：已知不含 map 也不含 pose；估计同时含 pose 与 map
- 其它组合：抛 `ValueError`

返回值用 `ProblemKind` 枚举（已提供）。

## 任务 2：`weighted_mean_1d`（`weighted_ls.py`）

最小化 \(\sum_i w_i (z_i - x)^2\)，闭式解为加权平均。

- `measurements` 与 `weights` 等长、非空
- 权重非负，总权重必须 > 0，否则 `ValueError`
- 黑板对照：`[1.0, 1.2]` + 等权 → `1.1`；第二路权 4 倍 → `1.16`

## 任务 3：标量 GN / LM（`nonlinear.py`）

残差与雅可比由调用方传入（测试用 \(e(x)=z-x^2\)，\(J=-2x\)）。

**Gauss-Newton**

1. \(H = J^\top J\)，\(b = J^\top e\)（标量即 \(H=J^2\)，\(b=J\cdot e\)）
2. \(\Delta x = -b / H\)（\(H=0\) 时停止）
3. \(x \leftarrow x + \Delta x\)，记录轨迹；\(|\Delta x|<\mathrm{tol}\) 停止

**Levenberg-Marquardt**

1. 用 \((H+\lambda)\Delta x=-b\)
2. **只接受使代价下降的步**；成功则 \(\lambda\leftarrow\lambda/10\)，失败则 \(\lambda\leftarrow 10\lambda\) 且本步 \(\Delta=0\)（位置不变）
3. 返回的 `SolveTrace` 含每次尝试后的 `xs` / `costs` / `deltas`

## 验收

```bash
pytest
```

全部绿灯即可。不要提交教师仓里的参考实现。

## 与后序作业关系

- C4-2/3 → `assignments/p_filter`（粒子滤波）
- C4-4/5 → `assignments/p_graph`
- C4-8 → `assignments/p_nav`（需 Noetic）
