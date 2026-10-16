import pytest

from herodungeon.core.models import Item
from herodungeon.m2_equip_search import Equipment, EquipmentIndex, generate_equipment


def test_put_and_get_roundtrip() -> None:
    index = EquipmentIndex(bucket_count=4)
    sword = Item("sword", "Sword", 5, 120)

    index.put(sword)

    assert index.get("sword") is sword


def test_accepts_equipment() -> None:
    index = EquipmentIndex(bucket_count=8)
    catalogue = generate_equipment(8)

    for item in catalogue:
        index.put(item)

    assert index.get(catalogue[3].item_id) is catalogue[3]
    assert isinstance(index.get(catalogue[3].item_id), Equipment)


def test_missing_key_raises_and_emits_miss() -> None:
    index = EquipmentIndex(bucket_count=4)

    with pytest.raises(KeyError):
        index.get("ghost")

    assert index.recorder.events[-1].type == "miss"


def test_update_existing_key_does_not_grow_size() -> None:
    index = EquipmentIndex(bucket_count=4)
    index.put(Item("sword", "Sword", 5, 120))

    index.put(Item("sword", "Sword v2", 5, 150))

    assert index.get("sword").value == 150
    assert index.size == 1


def test_collisions_are_observable() -> None:
    # bucket_count=4: load factor hits the expand threshold only after the 4th insert,
    # so two colliding keys below that still share a chain.
    index = EquipmentIndex(bucket_count=4)
    first, second = Item("id-0", "A", 1, 1), Item("id-4", "B", 1, 1)
    assert index._hash(first.item_id) == index._hash(second.item_id)

    index.put(first)
    index.put(second)

    collision_events = [
        event
        for event in index.recorder.events
        if event.type == "insert" and event.payload.get("collision")
    ]
    assert collision_events
    assert index.bucket_count == 4  # no rehash yet


def test_load_factor_and_bucket_sizes() -> None:
    index = EquipmentIndex(bucket_count=4)
    for i in range(2):
        index.put(Item(f"i{i}", "I", 1, 1))

    assert index.load_factor() == 0.5
    assert sum(index.bucket_sizes()) == 2


def test_invalid_bucket_count_rejected() -> None:
    with pytest.raises(ValueError):
        EquipmentIndex(bucket_count=0)


def test_polynomial_hash_spreads_eq_ids() -> None:
    """×31 uses far more buckets than character-sum on EQ-xxxxxx ids."""
    catalogue = generate_equipment(5000)
    index = EquipmentIndex(bucket_count=1024)
    used = {index._hash(item.item_id) for item in catalogue}
    assert len(used) > 200


def test_rehashes_when_load_factor_exceeds_limit() -> None:
    index = EquipmentIndex(bucket_count=4)
    items = [Item(f"id-{i}", "I", 1, i) for i in range(5)]

    for item in items:
        index.put(item)

    assert index.bucket_count >= 8
    assert index.size == 5
    assert any(event.type == "rehash" for event in index.recorder.events)
    for item in items:
        assert index.get(item.item_id) is item
