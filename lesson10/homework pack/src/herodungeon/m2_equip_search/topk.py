"""M2 lesson 10: distance helpers + top_k_by_value are provided; you implement top_k_similar.

Similarity uses Euclidean distance after min-max normalizing each field of
``to_vector()`` by ``FIELD_RANGES`` into ``[0, 1]``. A size-K max-heap of
distances (``heapq`` with negated distance) keeps the nearest K candidates;
the target itself (same ``item_id``) is excluded.
"""

from __future__ import annotations

import heapq
import math
from typing import Sequence

from herodungeon.core.events import EventRecorder
from herodungeon.core.models import Item
from herodungeon.m2_equip_search.equipment import FIELD_RANGES, VECTOR_FIELDS, Equipment

SOURCE = "m2.topk"
SOURCE_SIMILAR = "m2.topk_similar"


def normalized_vector(equipment: Equipment) -> tuple[float, ...]:
    """Scale ``to_vector()`` into ``[0, 1]`` per ``FIELD_RANGES`` (min-max)."""
    return tuple(
        (value - low) / (high - low)
        for value, (low, high) in zip(
            equipment.to_vector(), (FIELD_RANGES[name] for name in VECTOR_FIELDS), strict=True
        )
    )


def distance(a: Equipment, b: Equipment) -> float:
    """Normalized Euclidean distance between two pieces of equipment."""
    return math.dist(normalized_vector(a), normalized_vector(b))


def top_k_by_value(
    items: Sequence[Item], k: int, recorder: EventRecorder | None = None
) -> list[Item]:
    """Return the ``k`` highest-value items, highest first.

    Ties keep the item seen earliest, which keeps classroom output stable.
    Kept for older demos and TG-11; lesson 10 uses ``top_k_similar``.
    """
    if k <= 0:
        raise ValueError("k must be positive")
    recorder = recorder or EventRecorder()

    heap: list[tuple[int, int, Item]] = []
    for index, item in enumerate(items):
        if len(heap) < k:
            heapq.heappush(heap, (item.value, -index, item))
            recorder.emit(
                "push", SOURCE, item_id=item.item_id, value=item.value, heap_size=len(heap)
            )
        elif item.value > heap[0][0]:
            evicted = heapq.heapreplace(heap, (item.value, -index, item))
            recorder.emit(
                "replace",
                SOURCE,
                item_id=item.item_id,
                value=item.value,
                evicted=evicted[2].item_id,
            )
        else:
            recorder.emit("skip", SOURCE, item_id=item.item_id, value=item.value)

    ordered = sorted(heap, key=lambda entry: (entry[0], entry[1]), reverse=True)
    result = [entry[2] for entry in ordered]
    recorder.emit("final", SOURCE, top_k=[item.item_id for item in result])
    return result


def top_k_similar(
    items: Sequence[Equipment],
    target: Equipment,
    k: int,
    recorder: EventRecorder | None = None,
) -> list[Equipment]:
    """Return the ``k`` nearest equipment to ``target``, nearest first.

    Rules (lesson 10 / D5):

    * exclude any candidate with the same ``item_id`` as ``target``;
    * ``k <= 0`` raises ``ValueError``;
    * if ``k`` exceeds the candidate count, return every candidate;
    * equal distance → smaller ``item_id`` wins (stable, unique order);
    * size-K max-heap of distances via ``heapq`` + negated distance.
    """
    if k <= 0:
        raise ValueError("k must be positive")
    recorder = recorder or EventRecorder()
    # TODO: 跳过与 target 相同 item_id 的候选（可 emit skip reason=self）
    # TODO: 用 distance(target, item) 算归一化欧氏距离
    # TODO: 容量为 k 的大根堆：heapq 存 (-distance, item_id, item)
    # TODO: 堆未满 heappush + emit push；更近则 heapreplace + emit replace；否则 emit skip
    # TODO: 禁止用 sorted() / heapq.nsmallest 做 Top-K
    # TODO: 最终按 (distance, item_id) 由近到远返回，emit final
    raise NotImplementedError("implement top_k_similar")
