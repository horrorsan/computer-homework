"""与课程仓库 herodungeon.core.models 里的 Item 一致。已提供，不要修改。"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Item:
    """一个战利品包：编号、名字、重量（公斤）、里面的金币数。"""

    item_id: str
    name: str
    weight: int
    value: int

    def __post_init__(self) -> None:
        if self.weight <= 0:
            raise ValueError("item weight must be positive")
        if self.value < 0:
            raise ValueError("item value cannot be negative")
