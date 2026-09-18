"""M1 lesson 4: implement a FIFO action queue.

Do not use ``list.pop(0)`` as your dequeue. Keep an explicit head index and
compact the consumed prefix when it wastes at least half of the buffer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator

from herodungeon.core.events import AlgorithmEvent, EventRecorder

SOURCE = "m1.queue"


class QueueEmptyError(IndexError):
    """Raised when dequeuing or peeking an empty queue."""


@dataclass(slots=True)
class ActionQueue:
    recorder: EventRecorder = field(default_factory=EventRecorder)
    _buffer: list[Any] = field(default_factory=list, init=False, repr=False)
    _head: int = field(default=0, init=False, repr=False)

    def __len__(self) -> int:
        return len(self._buffer) - self._head

    def __iter__(self) -> Iterator[Any]:
        return iter(self._buffer[self._head :])

    @property
    def is_empty(self) -> bool:
        return len(self) == 0

    @property
    def items(self) -> tuple[Any, ...]:
        return tuple(self._buffer[self._head :])

    def enqueue(self, action: Any) -> AlgorithmEvent:
        """Append to the tail and emit enqueue."""
        self._buffer.append(action)
        return self.recorder.emit(
            "enqueue", 
            SOURCE, 
            size=len(self), 
            tail_index=len(self._buffer) - 1
        )

    def dequeue(self) -> Any:
        """Remove the front item in O(1) amortized time."""
        if self.is_empty:
            self.recorder.emit("underflow", SOURCE)
            raise QueueEmptyError("Cannot dequeue from an empty queue")

        item = self._buffer[self._head]
        self._head += 1
        
        self.recorder.emit("dequeue", SOURCE, item=item, size=len(self))
        self._compact_if_needed()
        return item

    def peek(self) -> Any:
        """Return the front item without removing it."""
        if self.is_empty:
            self.recorder.emit("underflow", SOURCE)
            raise QueueEmptyError("Cannot peek an empty queue")

        item = self._buffer[self._head]
        self.recorder.emit("peek", SOURCE, item=item)
        return item

    def drain(self) -> list[Any]:
        """Dequeue everything in FIFO order."""
        result = []
        current_length = len(self)
        for _ in range(current_length):
            result.append(self.dequeue())
        return result

    def _compact_if_needed(self) -> None:
        """Drop the consumed prefix when it is at least half of the buffer."""
        if self._head > 0 and self._head * 2 >= len(self._buffer):
            reclaimed = self._head
            self._buffer = self._buffer[self._head:]
            self._head = 0
            
            self.recorder.emit(
                "compact", 
                SOURCE, 
                reclaimed=reclaimed, 
                size=len(self._buffer)
            )
