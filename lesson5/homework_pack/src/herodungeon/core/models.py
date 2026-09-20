"""Core domain models. Do not change."""

from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Item:
    item_id: str
    name: str
    weight: int
    value: int

    def __post_init__(self) -> None:
        if self.weight <= 0:
            raise ValueError("item weight must be positive")
        if self.value < 0:
            raise ValueError("item value cannot be negative")

@dataclass(slots=True)
class Hero:
    name: str
    hp: int = 100
    x: int = 0
    y: int = 0

    @property
    def alive(self) -> bool:
        return self.hp > 0
