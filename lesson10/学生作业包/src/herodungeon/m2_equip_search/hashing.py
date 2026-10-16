"""M2 lesson 10: a small hash table with chaining, built for teaching collisions.

We deliberately avoid Python's built-in ``dict`` so every collision and
chain scan is visible. The hash is a polynomial rolling hash (×31); when the
load factor exceeds 0.75 the table doubles and rehashes. Character-sum hashing
stays on the lesson-7 whiteboard only — it collapses EQ-xxxxxx ids onto ~41
buckets.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from herodungeon.core.events import EventRecorder

SOURCE = "m2.hashing"
LOAD_FACTOR_LIMIT = 0.75


class HasItemId(Protocol):
    """Anything addressable by ``item_id`` (``Item`` or ``Equipment``)."""

    item_id: str


@dataclass(slots=True)
class EquipmentIndex:
    """O(1)-average lookup of equipment by ``item_id`` via chained hashing."""

    bucket_count: int = 8
    recorder: EventRecorder = field(default_factory=EventRecorder)
    _buckets: list[list[tuple[str, HasItemId]]] = field(init=False, repr=False)
    _size: int = field(default=0, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.bucket_count <= 0:
            raise ValueError("bucket_count must be positive")
        self._buckets = [[] for _ in range(self.bucket_count)]

    def _hash(self, item_id: str) -> int:
        """Polynomial hash ``h = h·31 + ord(c)`` (mod bucket count)."""
        value = 0
        for character in item_id:
            value = (value * 31 + ord(character)) % self.bucket_count
        return value

    @property
    def size(self) -> int:
        return self._size

    def load_factor(self) -> float:
        return self._size / self.bucket_count

    def _rehash(self, new_bucket_count: int) -> None:
        old_buckets = self._buckets
        old_count = self.bucket_count
        self.bucket_count = new_bucket_count
        self._buckets = [[] for _ in range(new_bucket_count)]
        for bucket in old_buckets:
            for item_id, item in bucket:
                self._buckets[self._hash(item_id)].append((item_id, item))
        self.recorder.emit(
            "rehash", SOURCE, old_buckets=old_count, new_buckets=new_bucket_count, size=self._size
        )

    def put(self, item: HasItemId) -> None:
        bucket_index = self._hash(item.item_id)
        bucket = self._buckets[bucket_index]
        for slot, (existing_id, _existing_item) in enumerate(bucket):
            if existing_id == item.item_id:
                bucket[slot] = (item.item_id, item)
                self.recorder.emit(
                    "update", SOURCE, bucket=bucket_index, item_id=item.item_id
                )
                return
        collision = len(bucket) > 0
        bucket.append((item.item_id, item))
        self._size += 1
        self.recorder.emit(
            "insert",
            SOURCE,
            bucket=bucket_index,
            item_id=item.item_id,
            collision=collision,
            chain_length=len(bucket),
        )
        if self.load_factor() > LOAD_FACTOR_LIMIT:
            self._rehash(self.bucket_count * 2)

    def get(self, item_id: str) -> HasItemId:
        """Look up by item_id. Scan the chain and emit each comparison."""
        # TODO: 用 _hash(item_id) 找到桶
        # TODO: 沿链逐个 emit chain_scan
        # TODO: 命中 emit hit 并返回该对象
        # TODO: 找不到 emit miss 并抛出 KeyError
        raise NotImplementedError("implement EquipmentIndex.get")

    def bucket_sizes(self) -> list[int]:
        """Chain length per bucket — useful for a load-factor visualization."""
        return [len(bucket) for bucket in self._buckets]
