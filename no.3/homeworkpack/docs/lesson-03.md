# 第 3 次课：线性表与背包

## 目标

用列表实现英雄背包：能放入物品、按编号取出，并在满包时失败。

## 必须满足的行为

1. `capacity` 必须为正数。
2. `add` 在未满时把物品放到末尾，并记录一次 `insert` 事件。
3. 背包已满时 `add` 先记录 `reject`，再抛出 `InventoryFullError`。
4. 相同 `item_id` 不能重复放入。
5. `remove` 按 `item_id` 从头查找；每比较一次记录 `compare`。
6. 找到后删除，记录 `remove`，后面的元素前移。
7. 找不到时记录 `miss`，并抛出 `ItemNotFoundError`。
8. `items` 返回当前物品的只读快照。
9. `total_value` 返回所有物品价值之和。

## 提交

```bash
pytest tests/test_inventory-第3课.py
```
