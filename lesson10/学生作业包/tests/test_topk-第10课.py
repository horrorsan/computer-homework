import math

import pytest

from herodungeon.core.events import EventRecorder
from herodungeon.core.models import Item
from herodungeon.m2_equip_search import (
    distance,
    generate_equipment,
    normalized_vector,
    top_k_by_value,
    top_k_similar,
)

ITEMS = [
    Item("a", "A", 1, 10),
    Item("b", "B", 1, 50),
    Item("c", "C", 1, 30),
    Item("d", "D", 1, 80),
    Item("e", "E", 1, 20),
]


def test_top_k_returns_highest_values_sorted_desc() -> None:
    top = top_k_by_value(ITEMS, 2)

    assert [it.item_id for it in top] == ["d", "b"]


def test_top_k_larger_than_input_returns_all() -> None:
    top = top_k_by_value(ITEMS, 10)

    assert len(top) == len(ITEMS)


def test_events_include_push_and_replace_or_skip() -> None:
    recorder = EventRecorder()
    top_k_by_value(ITEMS, 2, recorder=recorder)

    types = {event.type for event in recorder.events}
    assert "push" in types
    assert "replace" in types or "skip" in types
    assert "final" in types


def test_invalid_k_rejected() -> None:
    with pytest.raises(ValueError):
        top_k_by_value(ITEMS, 0)


def test_distance_matches_normalized_euclidean() -> None:
    catalogue = generate_equipment(10)
    target, other = catalogue[0], catalogue[4]
    expected = math.dist(normalized_vector(target), normalized_vector(other))

    assert distance(target, other) == pytest.approx(expected)
    assert round(distance(target, other), 2) == 0.24


def test_top_k_similar_near_to_far_excludes_self() -> None:
    catalogue = generate_equipment(10)
    target = catalogue[0]

    top = top_k_similar(catalogue, target, 3)

    assert [item.item_id for item in top] == ["EQ-000004", "EQ-000009", "EQ-000003"]
    assert target.item_id not in {item.item_id for item in top}
    distances = [distance(target, item) for item in top]
    assert distances == sorted(distances)


def test_top_k_similar_k_larger_than_candidates() -> None:
    catalogue = generate_equipment(5)
    target = catalogue[0]

    top = top_k_similar(catalogue, target, 10)

    assert len(top) == 4
    assert target.item_id not in {item.item_id for item in top}


def test_top_k_similar_rejects_non_positive_k() -> None:
    catalogue = generate_equipment(3)
    with pytest.raises(ValueError):
        top_k_similar(catalogue, catalogue[0], 0)
    with pytest.raises(ValueError):
        top_k_similar(catalogue, catalogue[0], -1)


def test_top_k_similar_tie_breaks_by_item_id() -> None:
    catalogue = generate_equipment(30)
    target = catalogue[0]
    # Force a wide k so several near-equal distances appear; order must be unique.
    top = top_k_similar(catalogue, target, 5)
    pairs = [(distance(target, item), item.item_id) for item in top]
    assert pairs == sorted(pairs)


def test_top_k_similar_emits_heap_events() -> None:
    recorder = EventRecorder()
    catalogue = generate_equipment(10)

    top_k_similar(catalogue, catalogue[0], 3, recorder=recorder)

    types = {event.type for event in recorder.events}
    assert "push" in types
    assert "final" in types
    assert "replace" in types or "skip" in types
