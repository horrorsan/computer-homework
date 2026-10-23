import inspect

from herodungeon.core.events import EventRecorder
from herodungeon.m2_equip_search import (
    bubble_sort_by,
    generate_equipment,
    quicksort_by,
    run_sort_benchmark,
    selection_sort_by,
)

FIELDS = {
    "n",
    "quick_comparisons",
    "bubble_comparisons",
    "selection_comparisons",
    "bubble_over_quick",
}


def _compares(sort, items) -> int:
    recorder = EventRecorder()
    sort(items, key=lambda item: item.power, recorder=recorder)
    return sum(1 for event in recorder.events if event.type == "compare")


def test_rows_have_expected_fields_in_size_order() -> None:
    rows = run_sort_benchmark(sizes=(5, 10, 20))

    assert [row["n"] for row in rows] == [5, 10, 20]
    for row in rows:
        assert set(row) == FIELDS


def test_default_sizes_match_lesson_11_deck() -> None:
    default = inspect.signature(run_sort_benchmark).parameters["sizes"].default

    assert tuple(default) == (100, 200, 400, 800)


def test_teacher_baselines_reproduce_deck_numbers_at_n_100() -> None:
    (row,) = run_sort_benchmark(sizes=(100,), seed=42)

    assert row["bubble_comparisons"] == 4760
    assert row["selection_comparisons"] == 4950


def test_benchmark_is_deterministic() -> None:
    first = run_sort_benchmark(sizes=(10, 40), seed=42)
    second = run_sort_benchmark(sizes=(10, 40), seed=42)

    assert first == second


def test_counts_come_from_generate_equipment_sorted_by_power() -> None:
    n, seed = 30, 7
    catalogue = generate_equipment(n, seed=seed)

    (row,) = run_sort_benchmark(sizes=(n,), seed=seed)

    assert row["quick_comparisons"] == _compares(quicksort_by, catalogue)
    assert row["bubble_comparisons"] == _compares(bubble_sort_by, catalogue)
    assert row["selection_comparisons"] == _compares(selection_sort_by, catalogue)


def test_selection_always_compares_n_choose_2() -> None:
    for row in run_sort_benchmark(sizes=(10, 40)):
        n = row["n"]
        assert row["selection_comparisons"] == n * (n - 1) // 2


def test_ratio_is_bubble_over_quick_rounded() -> None:
    for row in run_sort_benchmark(sizes=(20, 40)):
        expected = round(row["bubble_comparisons"] / row["quick_comparisons"], 2)
        assert row["bubble_over_quick"] == expected


def test_quicksort_wins_and_gap_grows_with_n() -> None:
    small, large = run_sort_benchmark(sizes=(20, 80))

    assert large["quick_comparisons"] < large["bubble_comparisons"]
    assert large["quick_comparisons"] < large["selection_comparisons"]
    assert small["bubble_over_quick"] < large["bubble_over_quick"]


def test_different_seed_changes_catalogue_not_shape() -> None:
    (a,) = run_sort_benchmark(sizes=(40,), seed=1)
    (b,) = run_sort_benchmark(sizes=(40,), seed=2)

    assert set(a) == set(b) == FIELDS
    assert a["selection_comparisons"] == b["selection_comparisons"]
