# 第 9 次课：装备类 + 入库 + 快速排序

## 目标

用统一的装备类 `Equipment` 把原始记录“入库”，再自己实现快速排序，按任意属性给装备排序。

## 统一装备字段（已提供，勿改）

| 字段 | 含义 | 类型与范围 |
| --- | --- | --- |
| `item_id` | 装备编号 | 非空字符串，同一批内唯一 |
| `name` | 名称 | 非空字符串 |
| `power` | 战力 | 整数 1–1000 |
| `speed` | 攻速 | 整数 1–100 |
| `weight` | 重量 | 整数 1–50 |
| `durability` | 耐久 | 整数 1–100 |
| `rarity` | 稀有度 | 整数 1–5 |

`to_vector()` 返回五维向量 `(power, speed, weight, durability, rarity)`，第 10 次课做相似度 Top-K 时会用到。
`generate_equipment(n, seed=42)` 生成可复现的装备目录，同一个 seed 在任何电脑上结果都一样。

## 任务 1：`load_equipment`（`equipment.py`）

1. 按输入顺序把每条记录（dict）变成 `Equipment`，返回列表；输入可能是生成器，只能遍历一次。
2. 缺字段、多出未知字段（例如把 `power` 写成 `attack`）、`item_id` 重复：抛出 `ValueError`。
3. 类型和范围交给 `Equipment` 自己检查。
4. 每接受一条记录发出 `ingest` 事件（`index`、`item_id`），最后发出 `ingest_done` 事件（`count`）。
5. 不要修改传进来的记录。

## 任务 2：`quicksort_by`（`quicksort.py`）

1. 返回新列表，不改原列表；`descending=True` 时降序。
2. 不准用 `sorted()`、`list.sort()` 或任何库排序。
3. 枢轴规则必须在已经排好序的输入上不退化，推荐**三数取中**（`low`、`mid`、`high` 三个位置的中位数），并把你的规则写进文件开头的说明。
4. 事件：`partition`（本轮区间）、`pivot`（选中的枢轴）、`compare`（每次与枢轴比较）、`swap`（交换两个不同位置）、`place_pivot`（枢轴归位）；`source` 用文件里的 `SOURCE`。
5. 快排不稳定，相同键的先后顺序不作要求。

冒泡排序、选择排序只作课堂对照，由老师给出完整代码，不计分，这次不用写。

## 提交

```bash
pytest tests/test_equipment-第9课.py tests/test_quicksort-第9课.py
```
