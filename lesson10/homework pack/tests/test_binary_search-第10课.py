import math

import pytest

from herodungeon.core.events import EventRecorder
from herodungeon.core.models import Item
from herodungeon.m2_equip_search import (
    binary_search_by,
    generate_equipment,
    lower_bound_by,
    quicksort_by,
)

ITEMS = [Item(f"i{i}", f"I{i}", 1, value) for i, value in enumerate([10, 20, 30, 40, 50])]


def test_found_returns_correct_index() -> None:
    index = binary_search_by(ITEMS, target_key=30, key=lambda it: it.value)

    assert index == 2


def test_not_found_returns_negative_one_and_emits_event() -> None:
    recorder = EventRecorder()
    index = binary_search_by(
        ITEMS, target_key=25, key=lambda it: it.value, recorder=recorder
    )

    assert index == -1
    assert recorder.events[-1].type == "not_found"


def test_descending_sorted_input() -> None:
    descending_items = list(reversed(ITEMS))
    index = binary_search_by(
        descending_items, target_key=40, key=lambda it: it.value, descending=True
    )

    assert descending_items[index].value == 40


def test_probe_count_is_logarithmic() -> None:
    recorder = EventRecorder()
    items = [Item(f"i{i}", "I", 1, i) for i in range(100)]

    binary_search_by(items, target_key=77, key=lambda it: it.value, recorder=recorder)

    probes = [event for event in recorder.events if event.type == "probe"]
    assert len(probes) <= math.ceil(math.log2(100)) + 1


def test_duplicate_keys_return_first_match() -> None:
    """Doc said 'first'; the old impl only guaranteed 'some' — D2 locks first."""
    catalogue = quicksort_by(generate_equipment(11), key=lambda item: item.rarity)
    keys = [item.rarity for item in catalogue]
    assert keys == [1, 2, 2, 2, 3, 3, 3, 3, 5, 5, 5]

    index = binary_search_by(catalogue, 3, key=lambda item: item.rarity)

    assert index == 4
    assert keys[index] == 3
    assert index == lower_bound_by(catalogue, 3, key=lambda item: item.rarity)


def test_lower_bound_matches_bisect_left() -> None:
    import bisect

    powers = [81, 90, 105, 197, 239, 271, 430, 715, 760, 876]
    items = [Item(f"i{i}", "I", 1, power) for i, power in enumerate(powers)]

    assert lower_bound_by(items, 200, key=lambda it: it.value) == bisect.bisect_left(powers, 200) == 4
    assert lower_bound_by(items, 501, key=lambda it: it.value) == bisect.bisect_left(powers, 501) == 7
    assert lower_bound_by(items, 900, key=lambda it: it.value) == len(powers)
    assert lower_bound_by(items, 0, key=lambda it: it.value) == 0
    assert lower_bound_by([], 1, key=lambda it: it.value) == 0


def test_lower_bound_emits_probe_and_bound() -> None:
    recorder = EventRecorder()
    index = lower_bound_by(ITEMS, 25, key=lambda it: it.value, recorder=recorder)

    assert index == 2
    assert {event.type for event in recorder.events} >= {"probe", "bound"}
    assert recorder.events[-1].type == "bound"
    assert recorder.events[-1].payload["index"] == 2
    assert any(event.payload.get("go_left") is True for event in recorder.events if event.type == "probe")


def test_range_query_via_two_lower_bounds() -> None:
    powers = [81, 90, 105, 197, 239, 271, 430, 715, 760, 876]
    items = [Item(f"i{i}", "I", 1, power) for i, power in enumerate(powers)]
    left = lower_bound_by(items, 200, key=lambda it: it.value)
    right = lower_bound_by(items, 501, key=lambda it: it.value)

    assert [item.value for item in items[left:right]] == [239, 271, 430]
