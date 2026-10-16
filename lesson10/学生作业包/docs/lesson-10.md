# 第 10 次课：二分 + 哈希索引 + 相似 Top-K

## 目标

1. 写出左边界 `lower_bound_by`，并用它实现真正返回「第一个匹配」的 `binary_search_by`。
2. 完成哈希索引的 `EquipmentIndex.get`（`put`、多项式哈希、扩容已提供）。
3. 用老师给的距离函数，手写容量为 K 的堆，实现 `top_k_similar`。

## Round 1：二分 + 左边界

### `lower_bound_by(sorted_items, target_key, key, recorder=None) -> int`

- 只支持**升序**；返回第一个 `key >= target_key` 的下标，范围是 `0..n`。
- 写法：闭区间 `lo..hi` + `ans`（初值 `n`），第 8 次课只做精确匹配（找不到返回 -1），左边界这一课才写。
- 事件：`probe`（带 `go_left`）、最后 `bound(index=...)`。

### `binary_search_by(...)`

- 升序：先 `lower_bound_by`，再看那一格是否等于目标；等于返回下标，否则 `-1`。
- 这样有重复键时一定返回**第一个**；找不到仍是 `-1`。
- `descending=True` 为选做。

## Round 2：哈希检索 + 相似 Top-K

### `EquipmentIndex.get`

- `put`、`_hash`（×31 多项式）、负载因子 `> 0.75` 时扩容已提供，不要改。
- 你只写 `get`：沿链 `chain_scan`，命中 `hit`，找不到 `miss` + `KeyError`。

### 距离（已提供，勿改）

- `normalized_vector` / `distance`：按 `FIELD_RANGES` 把五维缩放到 0–1，再算欧氏距离。

### `top_k_similar(items, target, k, recorder=None)`

1. 排除与 `target` 相同 `item_id` 的候选。
2. `k <= 0` 抛 `ValueError`；`k` 大于候选数时返回全部。
3. 容量为 K 的大根堆（`heapq` 存负距离）；由近到远返回。
4. 距离相同按 `item_id` 升序。
5. **禁止**用 `sorted()` / `heapq.nsmallest` 做 Top-K。
6. 事件：`push` / `replace` / `skip` / `final`。

`top_k_by_value` 由老师提供完整实现（不计分，仅脚手架）；本课计分的是 `top_k_similar`。

## 提交

```bash
pytest tests/test_binary_search-第10课.py \
       tests/test_hashing-第10课.py \
       tests/test_topk-第10课.py
```
