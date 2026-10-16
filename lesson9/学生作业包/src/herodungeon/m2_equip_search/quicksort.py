"""M2 lesson 9: quicksort for equipment.

Implement ``quicksort_by`` yourself. Do not call ``sorted()``, ``list.sort()``
or any library sort.

Requirements:

* return a **new** list; never modify ``items``;
* ascending by ``key(item)``; ``descending=True`` gives the reverse order;
* pick the pivot with a rule that does **not** degrade on already-sorted input
  (median-of-three recommended: the median of ``low`` / ``mid`` / ``high``),
  and write your pivot rule in this docstring;
* quicksort is not stable; equal keys may come out in any order.

Events (``source=SOURCE``), one round of partitioning emits, in this order:

* ``partition``    the range being split (e.g. ``low``, ``high``, ``depth``)
* ``pivot``        the chosen pivot (e.g. ``pivot_index``, ``pivot_key``)
* ``compare``      every element compared against the pivot
* ``swap``         every exchange of two different positions
* ``place_pivot``  where the pivot finally lands

Pivot rule: TODO 写下你的枢轴规则
"""

from __future__ import annotations

from typing import Any, Callable, Sequence, TypeVar

from herodungeon.core.events import EventRecorder

T = TypeVar("T")
SOURCE = "m2.quicksort"


def quicksort_by(
    items: Sequence[T],
    key: Callable[[T], Any],
    recorder: EventRecorder | None = None,
    descending: bool = False,
) -> list[T]:
    """Return a new list sorted by ``key`` using quicksort."""
    if recorder is None:
        recorder = EventRecorder()
    arr = list(items)                       

    def sort_range(low, high, depth):       
        if low >= high:
            return

        recorder.emit("partition", SOURCE, low=low, high=high, depth=depth)

        mid = (low + high) // 2
        ka, kb, kc = key(arr[low]), key(arr[mid]), key(arr[high])
        if (ka <= kb <= kc) or (kc <= kb <= ka):
            pi = mid
        elif (kb <= ka <= kc) or (kc <= ka <= kb):
            pi = low
        else:
            pi = high
        pk = key(arr[pi])
        recorder.emit("pivot", SOURCE, pivot_index=pi, pivot_key=pk)

        if pi != high:
            arr[pi], arr[high] = arr[high], arr[pi]
            recorder.emit("swap", SOURCE, i=pi, j=high)

        i = low
        for j in range(low, high):
            recorder.emit("compare", SOURCE, index=j, pivot_key=pk)
            kj = key(arr[j])
            
            ok = (kj > pk) if descending else (kj < pk)
            if ok:
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    recorder.emit("swap", SOURCE, i=i, j=j)
                i += 1

        if i != high:
            arr[i], arr[high] = arr[high], arr[i]
        recorder.emit("place_pivot", SOURCE, index=i)
        sort_range(low, i - 1, depth + 1)
        sort_range(i + 1, high, depth + 1)

    sort_range(0, len(arr) - 1, 0)
    return arr

