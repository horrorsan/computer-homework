"""第 8 次课当场检查。空函数应当失败。不要改这个文件。"""

from herodungeon.m2_equip_search.live_sort import (
    binary_search,
    count_at_least,
    partition,
    quicksort,
)

DECK = [70, 30, 90, 10, 50, 80, 40]
SORTED = [10, 30, 40, 50, 70, 80, 90]


def test_partition_takes_the_first_element_as_pivot() -> None:
    assert partition(DECK) == ([30, 10, 50, 40], 70, [90, 80])


def test_partition_sends_equals_to_the_right_in_encounter_order() -> None:
    assert partition([5, 1, 5, 9, 3]) == ([1, 3], 5, [5, 9])


def test_quicksort_sorts_the_deck() -> None:
    assert quicksort(DECK) == SORTED
    assert quicksort([40]) == [40]
    assert quicksort([]) == []


def test_binary_search_exact_match_only() -> None:
    assert binary_search(SORTED, 70) == 4
    assert binary_search(SORTED, 60) == -1
    assert binary_search(SORTED, 10) == 0
    assert binary_search(SORTED, 90) == 6


def test_count_at_least_scans_from_the_first_that_qualifies() -> None:
    assert count_at_least(SORTED, 50) == 4
    assert count_at_least(SORTED, 10) == 7
    assert count_at_least(SORTED, 80) == 2
    assert count_at_least(SORTED, 91) == 0
