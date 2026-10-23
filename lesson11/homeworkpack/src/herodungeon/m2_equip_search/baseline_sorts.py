"""M2 contrast baselines: bubble sort and selection sort (教师下发，仅作对照).

The course standard says "冒泡/选择仅对照": students do not write or get
graded on these. They exist so lesson 8 can show O(n^2) next to quicksort and
lesson 11 can count comparisons side by side. Both share the
``key``/``descending`` contract of ``quicksort_by`` and sort a copy.

* bubble sort: adjacent compare-and-swap, stops early after a pass with no
  swap; stable.
* selection sort: each pass selects the smallest (largest when descending)
  remaining key and swaps it to the front; not stable.
"""

from __future__ import annotations

from typing import Any, Callable, Sequence, TypeVar

from herodungeon.core.events import EventRecorder

T = TypeVar("T")

SOURCE_BUBBLE = "m2.bubble_sort"
SOURCE_SELECTION = "m2.selection_sort"


def bubble_sort_by(
    items: Sequence[T],
    key: Callable[[T], Any],
    recorder: EventRecorder | None = None,
    descending: bool = False,
) -> list[T]:
    """Sort a copy of ``items`` by ``key`` using bubble sort.

    Events: ``compare`` (index), ``swap`` (left, right), ``pass_done`` (pass, swapped).
    """
    recorder = recorder or EventRecorder()
    result = list(items)
    n = len(result)

    for pass_index in range(n - 1):
        swapped = False
        for j in range(n - 1 - pass_index):
            left_key, right_key = key(result[j]), key(result[j + 1])
            out_of_order = left_key < right_key if descending else left_key > right_key
            recorder.emit("compare", SOURCE_BUBBLE, index=j, out_of_order=out_of_order)
            if out_of_order:
                result[j], result[j + 1] = result[j + 1], result[j]
                recorder.emit("swap", SOURCE_BUBBLE, left=j, right=j + 1)
                swapped = True
        recorder.emit("pass_done", SOURCE_BUBBLE, pass_index=pass_index, swapped=swapped)
        if not swapped:
            break

    return result


def selection_sort_by(
    items: Sequence[T],
    key: Callable[[T], Any],
    recorder: EventRecorder | None = None,
    descending: bool = False,
) -> list[T]:
    """Sort a copy of ``items`` by ``key`` using selection sort.

    Events: ``compare`` (index, best), ``select`` (position, index), ``swap`` (left, right).
    """
    recorder = recorder or EventRecorder()
    result = list(items)
    n = len(result)

    for position in range(n - 1):
        best = position
        for index in range(position + 1, n):
            candidate, current = key(result[index]), key(result[best])
            better = candidate > current if descending else candidate < current
            recorder.emit("compare", SOURCE_SELECTION, index=index, best=best, better=better)
            if better:
                best = index
        recorder.emit("select", SOURCE_SELECTION, position=position, index=best)
        if best != position:
            result[position], result[best] = result[best], result[position]
            recorder.emit("swap", SOURCE_SELECTION, left=position, right=best)

    return result
