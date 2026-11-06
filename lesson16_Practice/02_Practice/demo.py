"""运行方式：python demo.py

看同一张表，限重不同时，勇者带走哪几个包。需要先完成 reconstruct_items。
"""
from __future__ import annotations

from copy import deepcopy

from events import EventRecorder
from lesson16_practice import describe_choice, reconstruct_items
from lesson_data import ITEMS, TABLE


class BacktrackDemo:
    """对一个限重做一次回溯，并打印每一步和结果。"""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity

    def run(self) -> None:
        recorder = EventRecorder()
        chosen = reconstruct_items(ITEMS, deepcopy(TABLE), self.capacity, recorder)
        print(f"\n限重 {self.capacity} 公斤（表里最后一行、这一列的格子是 {TABLE[-1][self.capacity]}）")
        for event in recorder.events:
            payload = event.payload
            if event.type == "skip_item":
                print(f"  跳过 {payload['item_id'].upper()}：还剩 {payload['remaining']} 公斤")
            elif event.type == "choose":
                print(f"  拿走 {payload['item_id'].upper()}：拿了以后还剩 {payload['remaining']} 公斤")
        print("  结果：", describe_choice(chosen))


def main() -> None:
    try:
        for capacity in (5, 4, 3):
            BacktrackDemo(capacity).run()
    except NotImplementedError as error:
        print(f"还有函数没写完：{error}")


if __name__ == "__main__":
    main()
