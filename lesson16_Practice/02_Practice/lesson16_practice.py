"""第16课练习：从填好的表里，找出勇者带走了哪几个包（回溯）。

你的任务（30分钟）：只完成 reconstruct_items 这一个函数。
表已经填好（第13课你写过填表），放在 lesson_data.py 里，不用自己再算。

表的含义：table[i][w] = 只用前 i 个包、最多背 w 公斤时，最多能带走的金币数。
第 i 行对应 items[i - 1]（第1行对应第一个包）。

做法：从最后一行 i = len(items)、还能背的公斤数 = capacity 开始，一行一行往上看：
    把当前格 table[i][w] 和上一行同一列 table[i - 1][w] 比一比：
      相同 → 不拿这个包。记录 skip_item，公斤数不变，去上一行。
      不同 → 拿这个包。记录 choose，公斤数减去它的重量，去上一行（限重变了，就看新的那一列）。
走到最上面一行就结束。最后记录 chosen，并返回带走的包的清单（顺序不限）。

记录事件：recorder.emit(类型, SOURCE, 字段名=值, ...)
    choose     item_id=被拿的包的编号，remaining=拿了它以后还剩几公斤
    skip_item  item_id=被跳过的包的编号，remaining=现在还剩几公斤
    chosen     item_ids=清单里所有包的编号（列表）

只读表，不要修改 table。recorder 是 None 时，自己新建一个 EventRecorder。
"""
from __future__ import annotations

from collections.abc import Sequence

from events import EventRecorder
from models import Item

SOURCE = "m3.dp"


# ---------------------------------------------------------------------------
# 你要完成的函数
# ---------------------------------------------------------------------------
def reconstruct_items(
    items: Sequence[Item],
    table: list[list[int]],
    capacity: int,
    recorder: EventRecorder | None = None,
) -> list[Item]:
    """从填好的表里，回溯出带走的包。规则见文件开头的说明。"""
    
    if recorder is None:
        recorder = EventRecorder()

    chosen: list[Item] = []
    i = len(items)
    w = capacity

    while i > 0:
        item = items[i - 1]

        if table[i][w] == table[i - 1][w]:

            recorder.emit("skip_item", SOURCE, item_id=item.id, remaining=w)
        else:
            chosen.append(item)
            w -= item.weight
            recorder.emit("choose", SOURCE, item_id=item.id, remaining=w)

        i -= 1

        chosen.reverse()
    recorder.emit("chosen", SOURCE, item_ids=[item.id for item in chosen])

    return chosen


# ---------------------------------------------------------------------------
# 下面是已经写好的部分
# ---------------------------------------------------------------------------
def total_weight(chosen: Sequence[Item]) -> int:
    """（已提供）清单里所有包的总重量。"""
    return sum(item.weight for item in chosen)


def total_value(chosen: Sequence[Item]) -> int:
    """（已提供）清单里所有包的金币总数。"""
    return sum(item.value for item in chosen)


def describe_choice(chosen: Sequence[Item]) -> str:
    """（已提供）把清单写成一句话。"""
    if not chosen:
        return "什么也没带走"
    names = "、".join(item.name for item in chosen)
    return f"带走 {names}：共 {total_weight(chosen)} 公斤、{total_value(chosen)} 枚金币"
