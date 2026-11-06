import random

import pytest

from herodungeon.core.models import Item
from herodungeon.m3_behavior_tree import (
    GREEDY_TRAP_CAPACITY,
    GREEDY_TRAP_ITEMS,
    HAND_FILL_CAPACITY,
    HAND_FILL_ITEMS,
    HOMEWORK_ITEM_C,
    best_value,
    brute_force_best,
    fill_table,
    greedy_by_ratio,
)


def _small_instances() -> list[tuple[list[Item], int]]:
    rng = random.Random(13)
    cases: list[tuple[list[Item], int]] = []
    for case in range(30):
        n = rng.randint(1, 7)
        items = [
            Item(f"i{case}_{k}", f"I{k}", rng.randint(1, 9), rng.randint(0, 30))
            for k in range(n)
        ]
        cases.append((items, rng.randint(0, 20)))
    return cases


# --- the table the deck fills by hand -------------------------------------------


def test_hand_fill_table_matches_the_slides() -> None:
    assert fill_table(HAND_FILL_ITEMS, HAND_FILL_CAPACITY) == [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 3, 3, 3, 3],
        [0, 0, 3, 4, 4, 7],
    ]


def test_homework_row_for_item_c() -> None:
    table = fill_table([*HAND_FILL_ITEMS, HOMEWORK_ITEM_C], HAND_FILL_CAPACITY)

    assert table[3] == [0, 0, 3, 5, 5, 8]


def test_table_has_extra_row_and_column_of_zeros() -> None:
    table = fill_table(GREEDY_TRAP_ITEMS, 7)

    assert len(table) == len(GREEDY_TRAP_ITEMS) + 1
    assert all(len(row) == 8 for row in table)
    assert table[0] == [0] * 8
    assert [row[0] for row in table] == [0] * len(table)


def test_every_cell_is_max_of_skip_and_take() -> None:
    items = [*HAND_FILL_ITEMS, HOMEWORK_ITEM_C, Item("D", "D", 4, 6)]
    table = fill_table(items, 9)

    for i in range(1, len(items) + 1):
        item = items[i - 1]
        for w in range(10):
            skip = table[i - 1][w]
            take = table[i - 1][w - item.weight] + item.value if w >= item.weight else skip
            assert table[i][w] == max(skip, take)


def test_best_value_is_bottom_right_cell() -> None:
    assert best_value(HAND_FILL_ITEMS, HAND_FILL_CAPACITY) == 7


# --- greedy trap: 160 vs 220 ------------------------------------------------------


def test_greedy_takes_a_then_b_for_160() -> None:
    chosen = greedy_by_ratio(GREEDY_TRAP_ITEMS, GREEDY_TRAP_CAPACITY)

    assert [item.item_id for item in chosen] == ["A", "B"]
    assert sum(item.weight for item in chosen) == 30
    assert sum(item.value for item in chosen) == 160


def test_dp_finds_220_on_the_greedy_trap() -> None:
    table = fill_table(GREEDY_TRAP_ITEMS, GREEDY_TRAP_CAPACITY)

    assert table[3][50] == 220
    assert best_value(GREEDY_TRAP_ITEMS, GREEDY_TRAP_CAPACITY) == 220
    assert brute_force_best(GREEDY_TRAP_ITEMS, GREEDY_TRAP_CAPACITY) == 220


def test_greedy_ties_keep_input_order_and_skip_what_does_not_fit() -> None:
    items = [Item("x", "X", 4, 8), Item("y", "Y", 2, 4), Item("z", "Z", 5, 5)]

    assert [item.item_id for item in greedy_by_ratio(items, 6)] == ["x", "y"]
    assert greedy_by_ratio(items, 1) == []


# --- DP vs brute force vs greedy ----------------------------------------------


def test_dp_matches_brute_force_on_small_instances() -> None:
    for items, capacity in _small_instances():
        assert best_value(items, capacity) == brute_force_best(items, capacity)


def test_greedy_is_feasible_and_never_beats_dp() -> None:
    worse = 0
    for items, capacity in _small_instances():
        chosen = greedy_by_ratio(items, capacity)
        total = sum(item.value for item in chosen)
        assert sum(item.weight for item in chosen) <= capacity
        assert total <= best_value(items, capacity)
        worse += total < best_value(items, capacity)
    assert worse > 0


# --- edges ------------------------------------------------------------------------


def test_zero_capacity_and_no_items() -> None:
    assert fill_table(HAND_FILL_ITEMS, 0) == [[0], [0], [0]]
    assert fill_table([], 4) == [[0, 0, 0, 0, 0]]
    assert greedy_by_ratio([], 4) == []


def test_item_heavier_than_bag_is_never_taken() -> None:
    heavy = [Item("h", "Heavy", 9, 100)]

    assert best_value(heavy, 8) == 0
    assert greedy_by_ratio(heavy, 8) == []


def test_negative_capacity_rejected() -> None:
    with pytest.raises(ValueError):
        fill_table(HAND_FILL_ITEMS, -1)


def test_inputs_are_not_modified() -> None:
    items = list(GREEDY_TRAP_ITEMS)
    fill_table(items, GREEDY_TRAP_CAPACITY)
    greedy_by_ratio(items, GREEDY_TRAP_CAPACITY)

    assert items == list(GREEDY_TRAP_ITEMS)
