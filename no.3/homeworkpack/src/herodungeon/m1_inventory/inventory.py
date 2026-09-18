"""M1 lesson 3: implement the list-based inventory.

Replace every `NotImplementedError` below. Do not change the public method
names or the exception types — the tests depend on them.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from herodungeon.core.events import AlgorithmEvent, EventRecorder
from herodungeon.core.models import Item


class InventoryFullError(ValueError):
    pass


class ItemNotFoundError(KeyError):
    pass


@dataclass(slots=True)
class Inventory:
    capacity: int
    recorder: EventRecorder = field(default_factory=EventRecorder)
    _items: list[Item] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ValueError("capacity must be positive")

    @property
    def items(self) -> tuple[Item, ...]:
        return tuple(self._items)

    def add(self, item: Item) -> AlgorithmEvent:
        """Append `item` if there is room; otherwise reject and raise."""
        if len(self._items) >= self.capacity:
           self.recorder.emit("reject", "inventory",item=item)
           raise InventoryFullError("Inventory is full")
        for existing_item in self._items:
            if existing_item.item_id == item.item_id:
                raise ValueError(f"Item with id {item.item_id} already exists")
        self._items.append(item)
        return self.recorder.emit("insert",  "inventory",item=item)

        

    def remove(self, item_id: str) -> Item:
        """Find `item_id` from the front, emit compare/remove/miss, and return it."""
        for index, existing_item in enumerate(self._items):
            self.recorder.emit("compare",  "inventory",item=existing_item)
            if existing_item.item_id == item_id:
                 self.recorder.emit("remove", "inventory", item=existing_item)
                 return self._items.pop(index)

        self.recorder.emit("miss",  "inventory",item_id=item_id)
        raise ItemNotFoundError(f"Item with id {item_id} not found")

    def total_value(self) -> int:
        """Return the sum of item values currently in the bag."""
        return sum(item.value for item in self._items)
       
