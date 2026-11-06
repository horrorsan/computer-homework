"""第16课自测：每一项都对应课件里的一个预测或一张表。

不需要修改这个文件。运行 python self_check.py 查看结果。
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable

import lesson16_practice as practice
from events import EventRecorder
from lesson_data import ITEMS, ITEMS_WITH_D, TABLE, TABLE_WITH_D
from models import Item


@dataclass(frozen=True)
class Check:
    group: str
    name: str
    run: Callable[[], None]


def expect(actual: Any, expected: Any, hint: str) -> None:
    if actual != expected:
        raise AssertionError(f"{hint}：应该是 {expected!r}，你的结果是 {actual!r}")


def ids(chosen: Any) -> list[str]:
    return sorted(item.item_id for item in chosen)


class CheckSuite:
    """把所有自测集中在一起，终端脚本和 pytest 共用同一份。"""

    GROUP_A = "回溯：带走哪些包"
    GROUP_B = "回溯：规则和记录"

    def checks(self) -> list[Check]:
        return [
            Check(self.GROUP_A, "限重5：带走A和B", self.capacity_5),
            Check(self.GROUP_A, "限重4：带走C", self.capacity_4),
            Check(self.GROUP_A, "限重3：带走B", self.capacity_3),
            Check(self.GROUP_A, "限重0：什么也不带", self.capacity_0),
            Check(self.GROUP_A, "再加包D：带走D", self.with_d),
            Check(self.GROUP_B, "没超重，金币等于表里的最大值", self.feasible_and_best),
            Check(self.GROUP_B, "同一个包不会带两次", self.no_repeat),
            Check(self.GROUP_B, "金币一样的包，带走其中一个即可", self.tie),
            Check(self.GROUP_B, "只读表，不改表", self.read_only),
            Check(self.GROUP_B, "记录：跳过、选中、最后的清单", self.events),
        ]

    @staticmethod
    def _run(capacity: int, items: Any = ITEMS, table: Any = TABLE) -> list[Item]:
        return practice.reconstruct_items(items, deepcopy(table), capacity)

    def capacity_5(self) -> None:
        expect(ids(self._run(5)), ["a", "b"], "限重5公斤带走的包")

    def capacity_4(self) -> None:
        expect(ids(self._run(4)), ["c"], "限重4公斤带走的包")

    def capacity_3(self) -> None:
        expect(ids(self._run(3)), ["b"], "限重3公斤带走的包")

    def capacity_0(self) -> None:
        expect(ids(self._run(0)), [], "限重0公斤带走的包")
        expect(ids(practice.reconstruct_items((), [[0, 0, 0]], 2)), [], "没有任何包时")

    def with_d(self) -> None:
        expect(ids(self._run(5, ITEMS_WITH_D, TABLE_WITH_D)), ["d"], "加入包D后限重5公斤带走的包")

    def feasible_and_best(self) -> None:
        for capacity in range(6):
            chosen = self._run(capacity)
            weight = sum(item.weight for item in chosen)
            value = sum(item.value for item in chosen)
            if weight > capacity:
                raise AssertionError(f"限重{capacity}公斤：带走的包共{weight}公斤，超重了")
            expect(value, TABLE[-1][capacity], f"限重{capacity}公斤时带走的金币数")

    def no_repeat(self) -> None:
        items = (Item("a", "A", 2, 3),)
        chosen = practice.reconstruct_items(items, [[0, 0, 0, 0, 0], [0, 0, 3, 3, 3]], 4)
        expect(len(chosen), 1, "只有一个包A时，限重4公斤带走几个包")

    def tie(self) -> None:
        items = (Item("a", "A", 2, 3), Item("b", "B", 2, 3))
        chosen = practice.reconstruct_items(items, [[0, 0, 0], [0, 0, 3], [0, 0, 3]], 2)
        expect(len(chosen), 1, "两个一样的包，限重2公斤带走几个")
        expect(sum(item.value for item in chosen), 3, "带走的金币数")

    def read_only(self) -> None:
        table = deepcopy(TABLE)
        practice.reconstruct_items(ITEMS, table, 5)
        expect(table, TABLE, "回溯之后，表应该和原来完全一样")

    def events(self) -> None:
        recorder = EventRecorder()
        chosen = practice.reconstruct_items(ITEMS, deepcopy(TABLE), 5, recorder)
        expect(ids(chosen), ["a", "b"], "带走的包")
        records = [(event.type, event.payload) for event in recorder.events]
        expect([kind for kind, _ in records], ["skip_item", "choose", "choose", "chosen"], "事件的顺序")
        expect(records[0][1], {"item_id": "c", "remaining": 5}, "第1条事件（跳过C）的内容")
        expect(records[1][1], {"item_id": "b", "remaining": 2}, "第2条事件（拿B）的内容")
        expect(records[2][1], {"item_id": "a", "remaining": 0}, "第3条事件（拿A）的内容")
        expect(sorted(records[3][1].get("item_ids", [])), ["a", "b"], "最后一条事件里的清单")
