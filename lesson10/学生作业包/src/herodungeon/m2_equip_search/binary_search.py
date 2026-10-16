"""M2 lesson 10: binary search and lower-bound over already-sorted equipment.

The input must already be sorted by ``key``. Ascending ``binary_search_by``
should be implemented via ``lower_bound_by`` so duplicate keys return the
*first* match. Do not scan from left to right.
"""

from __future__ import annotations

from typing import Any, Callable, Sequence, TypeVar

from herodungeon.core.events import EventRecorder

T = TypeVar("T")

SOURCE = "m2.binary_search"
SOURCE_LOWER = "m2.lower_bound"


def lower_bound_by(
    sorted_items: Sequence[T],
    target_key: Any,
    key: Callable[[T], Any],
    recorder: EventRecorder | None = None,
) -> int:
    """Return the first index whose key is ``>= target_key`` (ascending only).

    Returns ``0..n``. Use a closed interval ``lo..hi`` and an ``ans`` slot
    (same as lesson 8). Emit ``probe`` (with ``go_left``) and a final ``bound``.
    """
    recorder = recorder or EventRecorder()
    # TODO: ans 初值为 n；while lo <= hi
    # TODO: mid；若 key(mid) >= target 则 ans=mid、往左，否则往右
    # TODO: 每次 emit probe（带 go_left）；结束 emit bound(index=ans)
    raise NotImplementedError("implement lower_bound_by")


def binary_search_by(
    sorted_items: Sequence[T],
    target_key: Any,
    key: Callable[[T], Any],
    recorder: EventRecorder | None = None,
    descending: bool = False,
) -> int:
    """Return the index of the first item whose key equals ``target_key``.

    Ascending (default): call ``lower_bound_by``, then check that cell.
    Return ``-1`` when no match exists. ``descending=True`` is optional.
    """
    recorder = recorder or EventRecorder()
    # TODO: 升序：i = lower_bound_by(...)；若 i < n 且 key 相等 → found，否则 not_found / -1
    # TODO: 降序（选做）：闭区间探查，相等返回 mid
    raise NotImplementedError("implement binary_search_by")
