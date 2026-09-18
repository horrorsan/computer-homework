import pytest

from herodungeon.core import Item
from herodungeon.m1_inventory import Inventory, InventoryFullError, ItemNotFoundError


def test_add_remove_emits_observable_steps() -> None:
    inventory = Inventory(capacity=2)
    potion = Item("potion", "Potion", 1, 12)
    key = Item("key", "Key", 1, 30)

    inventory.add(potion)
    inventory.add(key)
    removed = inventory.remove("potion")

    assert removed == potion
    assert inventory.items == (key,)
    assert [event.type for event in inventory.recorder.events] == [
        "insert",
        "insert",
        "compare",
        "remove",
    ]


def test_capacity_failure_is_visible() -> None:
    inventory = Inventory(capacity=1)
    inventory.add(Item("potion", "Potion", 1, 12))

    with pytest.raises(InventoryFullError):
        inventory.add(Item("key", "Key", 1, 30))

    assert inventory.recorder.events[-1].type == "reject"


def test_missing_item_raises_and_emits_miss() -> None:
    inventory = Inventory(capacity=2)

    with pytest.raises(ItemNotFoundError):
        inventory.remove("unknown")

    assert inventory.recorder.events[-1].type == "miss"


def test_total_value_sums_current_items() -> None:
    inventory = Inventory(capacity=3)
    inventory.add(Item("potion", "Potion", 1, 12))
    inventory.add(Item("key", "Key", 1, 30))

    assert inventory.total_value() == 42
