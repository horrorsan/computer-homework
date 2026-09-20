"""M1 lesson 5: implement a LIFO undo stack.

Push/pop the newest operation. If max_depth is set, evict the oldest entry
before pushing a new one that would overflow.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator

from herodungeon.core.events import AlgorithmEvent, EventRecorder

SOURCE = "m1.stack"


class StackEmptyError(IndexError):
    """Raised when popping or peeking an empty stack."""


@dataclass(slots=True)
class UndoStack:
    max_depth: int | None = None
    recorder: EventRecorder = field(default_factory=EventRecorder)
    _buffer: list[Any] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.max_depth is not None and self.max_depth <= 0:
            raise ValueError("max_depth must be positive when provided")

    def __len__(self) -> int:
        return len(self._buffer)

    def __iter__(self) -> Iterator[Any]:
        return reversed(self._buffer)

    @property
    def is_empty(self) -> bool:
        return not self._buffer

    @property
    def items(self) -> tuple[Any, ...]:
        return tuple(self._buffer)

    def push(self, operation: Any) -> AlgorithmEvent:
        """Push to the top; evict the oldest item if max_depth is exceeded."""
        evicted = None
        
        if self.max_depth is not None and len(self._buffer) >= self.max_depth:
            evicted = self._buffer.pop(0)
            self.recorder.emit(
                event_type="evict",
                source=SOURCE,
                evicted=evicted,
                depth=len(self._buffer)
            )

        self._buffer.append(operation)

        push_event = self.recorder.emit(
            event_type="push",
            source=SOURCE,
            operation=operation,
            depth=len(self._buffer),
            evicted=evicted
        )

        return push_event


    def pop(self) -> Any:
        """Remove and return the top operation."""
        # TODO: 空栈时 emit underflow 并抛出 StackEmptyError
        if self.is_empty:
            self.recorder.emit(
                event_type="underflow",
                source=SOURCE,
                action="pop"
            )
            raise StackEmptyError("Cannot pop from an empty stack")
        # TODO: pop 栈顶，emit pop，返回该操作
        operation = self._buffer.pop()

        self.recorder.emit(
            event_type="pop",
            source=SOURCE,
            operation=operation,
            depth=len(self._buffer)
        )
        
        return operation


    def peek(self) -> Any:
        """Return the top operation without removing it."""
        # TODO: 空栈时 emit underflow 并抛出 StackEmptyError
        if self.is_empty:
            self.recorder.emit(
                event_type="underflow",
                source=SOURCE,
                action="peek"
            )
            raise StackEmptyError("Cannot peek an empty stack")
        # TODO: emit peek 并返回栈顶
        operation = self._buffer[-1]
 
        self.recorder.emit(
            event_type="peek",
            source=SOURCE,
            operation=operation,
            depth=len(self._buffer)
        )
        
        return operation