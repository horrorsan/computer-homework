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
    # TODO: 复制一份 items，在副本上原地排序
    # TODO: 选枢轴（推荐三数取中），emit partition / pivot
    # TODO: 划分：每次与枢轴比较 emit compare，交换 emit swap
    # TODO: 枢轴归位 emit place_pivot，再分别处理左右两段
    # TODO: descending=True 时把比较方向反过来
    raise NotImplementedError("implement quicksort_by")
