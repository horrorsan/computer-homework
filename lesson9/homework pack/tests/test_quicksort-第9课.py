import random

from herodungeon.core.events import EventRecorder
from herodungeon.m2_equip_search import generate_equipment, quicksort_by


def _powers(items):
    return [item.power for item in items]


def test_ascending_by_power() -> None:
    catalogue = generate_equipment(40)

    result = quicksort_by(catalogue, key=lambda item: item.power)

    assert _powers(result) == sorted(_powers(catalogue))
    assert sorted(item.item_id for item in result) == sorted(item.item_id for item in catalogue)


def test_descending_by_power() -> None:
    catalogue = generate_equipment(40)

    result = quicksort_by(catalogue, key=lambda item: item.power, descending=True)

    assert _powers(result) == sorted(_powers(catalogue), reverse=True)


def test_sorts_a_copy() -> None:
    catalogue = generate_equipment(15)
    before = list(catalogue)

    result = quicksort_by(catalogue, key=lambda item: item.power)

    assert catalogue == before
    assert result is not catalogue


def test_empty_single_and_generic_keys() -> None:
    assert quicksort_by([], key=lambda value: value) == []
    assert quicksort_by([7], key=lambda value: value) == [7]
    assert quicksort_by([3, 1, 2], key=lambda value: -value) == [3, 2, 1]


def test_many_duplicate_keys() -> None:
    catalogue = generate_equipment(300)

    result = quicksort_by(catalogue, key=lambda item: item.rarity)

    assert [item.rarity for item in result] == sorted(item.rarity for item in catalogue)


def test_random_integers_match_reference() -> None:
    rng = random.Random(1)
    values = [rng.randint(0, 50) for _ in range(200)]

    assert quicksort_by(values, key=lambda value: value) == sorted(values)
    assert quicksort_by(values, key=lambda value: value, descending=True) == sorted(values, reverse=True)


def test_emits_partition_pivot_compare_and_place_events() -> None:
    recorder = EventRecorder()

    quicksort_by(generate_equipment(20), key=lambda item: item.power, recorder=recorder)

    types = [event.type for event in recorder.events]
    assert {"partition", "pivot", "compare", "place_pivot"} <= set(types)
    assert types.count("partition") == types.count("place_pivot")
    assert types.count("pivot") == types.count("partition")
    assert all(event.source == "m2.quicksort" for event in recorder.events)


def test_already_sorted_input_does_not_degrade() -> None:
    n = 128
    ordered = list(range(n))
    recorder = EventRecorder()

    result = quicksort_by(ordered, key=lambda value: value, recorder=recorder)

    compares = sum(1 for event in recorder.events if event.type == "compare")
    assert result == ordered
    assert compares < n * n // 4
