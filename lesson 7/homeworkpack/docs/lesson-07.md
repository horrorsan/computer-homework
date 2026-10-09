# 第 7 次课：M2 导入 1 —— 哈希表与精确查找

本课在教室上，用自己的电脑。先做纸笔三轮，再当场写四个函数。编码不单独计分，算进第 11 次课小项目 2 的验收。代码写不完，纸上过程仍要交。

## 课堂要记住的

- 数组是一排编号的格子。哈希表就是这样的一排柜子。
- ID 是装备的 `item_id`，是字符串，例如 `"sword"`。它不是数字，也不是柜号。
- 本课哈希函数：柜号 = 各字符编码之和 % 柜子数。字符编码用 `ord()`，`a = 97`，后面每个字母加 1。`"sword"` 是 115+119+111+114+100 = 559，559 % 8 = 7。
- 冲突用链地址：同号装备按放入顺序挂在同一个柜子后面。
- 精确查找用哈希。范围、相似留给第 8 次课。

插入排序、归并排序已撤出本课。第 10 次课的哈希索引（多项式哈希、扩容、`EquipmentIndex`）本课不写。

## 纸笔（约 45 分钟，讲完一块做一块）

1. **15 分钟。** 写出 `sword`、`shield`、`bow`、`dagger`、`staff`、`helmet` 的字符编码相加过程，再 % 8。只写柜号不算完。
2. **20 分钟。** 按这个顺序放进 8 个柜子（0 到 7）。画出 `sword` 和 `helmet` 都进 7 号柜的那条链。走一遍 `get("helmet")`：比了几次、先碰到谁。再写一个不存在的 ID 会怎样。
3. **10 分钟。** 算 n=6、M=8 时的负载因子。再写一个坏哈希：不管什么 ID 都进 0 号柜，说明这时为什么又变回一个一个找。

## 当场编码（约 35 分钟）

只改 `src/herodungeon/m2_equip_search/live_hash.py`。四个函数现在都会 `raise NotImplementedError`。不要改测试。仓库里没有答案。

### `bucket_index(item_id, bucket_count) -> int`

各字符的 `ord` 相加，再对 `bucket_count` 取余。

### `put(buckets, item_id) -> None`

`buckets` 是长度等于柜子数的列表，每个柜子是一条链（列表）。先算柜号，再把 `item_id` 接到那条链的末尾。柜子数用 `len(buckets)`。

### `get(buckets, item_id)`

先算柜号，再沿链逐个比。找到就返回这个 ID，没有就返回 `None`。不要抛异常。

### `load_factor(n, bucket_count) -> float`

返回 `n / bucket_count`（普通除法，不要整除）。

当场用这 6 个 ID 检查：`sword` 和 `helmet` 都进 7 号柜，链是 `["sword", "helmet"]`；`get("helmet")` 得到 `"helmet"`；不存在的 ID 得到 `None`；`load_factor(6, 8)` 是 `0.75`。

```bash
pytest tests/test_live_hash-第7课.py
```
