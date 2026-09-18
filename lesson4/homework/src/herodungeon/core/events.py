"""Unified observable event protocol. Provided as scaffolding; do not change."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Iterable


@dataclass(frozen=True, slots=True)
class AlgorithmEvent:
    type: str
    step: int
    source: str
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class EventRecorder:
    def __init__(self) -> None:
        self._events: list[AlgorithmEvent] = []

    def emit(self, event_type: str, source: str, **payload: Any) -> AlgorithmEvent:
        event = AlgorithmEvent(
            type=event_type,
            step=len(self._events),
            source=source,
            payload=payload,
        )
        self._events.append(event)
        return event

    @property
    def events(self) -> tuple[AlgorithmEvent, ...]:
        return tuple(self._events)

    def extend(self, events: Iterable[AlgorithmEvent]) -> None:
        self._events.extend(events)

    def clear(self) -> None:
        self._events.clear()
