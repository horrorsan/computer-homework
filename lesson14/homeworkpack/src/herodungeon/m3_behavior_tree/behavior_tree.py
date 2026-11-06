"""M3 lesson 14: a tiny behavior-tree runtime -- tick, Sequence, Selector.

Provided: BehaviorStatus, TickContext (the blackboard), Condition, Action, _emit.
Implement Sequence.tick (AND) and Selector.tick (OR) so status bubbles from the
leaves to the root. RUNNING is passed straight up and stops the loop;
remembering the running child (running_index) is optional and not tested.
Real monster leaves (sight range, HP, patrol) are lesson 15.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Protocol

from herodungeon.core.events import EventRecorder

SOURCE = "m3.behavior_tree"


class BehaviorStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    RUNNING = "running"


@dataclass(slots=True)
class TickContext:
    """Blackboard shared by every node during one decision tick."""

    world: dict[str, Any]
    recorder: EventRecorder = field(default_factory=EventRecorder)
    log: list[str] = field(default_factory=list)

    def note(self, message: str) -> None:
        self.log.append(message)


class BehaviorNode(Protocol):
    name: str

    def tick(self, ctx: TickContext) -> BehaviorStatus: ...


def _emit(
    ctx: TickContext, node: BehaviorNode, status: BehaviorStatus, kind: str
) -> BehaviorStatus:
    ctx.recorder.emit(
        "tick",
        SOURCE,
        node=node.name,
        kind=kind,
        status=status.value,
    )
    return status


@dataclass(slots=True)
class Condition:
    name: str
    predicate: Callable[[dict[str, Any]], bool]

    def tick(self, ctx: TickContext) -> BehaviorStatus:
        passed = bool(self.predicate(ctx.world))
        status = BehaviorStatus.SUCCESS if passed else BehaviorStatus.FAILURE
        ctx.note(f"condition:{self.name}={'yes' if passed else 'no'}")
        return _emit(ctx, self, status, "condition")


@dataclass(slots=True)
class Action:
    name: str
    effect: Callable[[dict[str, Any]], BehaviorStatus] | None = None

    def tick(self, ctx: TickContext) -> BehaviorStatus:
        if self.effect is None:
            status = BehaviorStatus.SUCCESS
        else:
            status = self.effect(ctx.world)
        ctx.note(f"action:{self.name}={status.value}")
        ctx.world["last_action"] = self.name
        return _emit(ctx, self, status, "action")


@dataclass(slots=True)
class Sequence:
    """AND: tick children left-to-right until one fails or all succeed."""

    name: str
    children: list[BehaviorNode] = field(default_factory=list)

    def tick(self, ctx: TickContext) -> BehaviorStatus:
        _emit(ctx, self, BehaviorStatus.RUNNING, "sequence")

        for child in self.children:
            status = child.tick(ctx)
            if status != BehaviorStatus.SUCCESS:
                return _emit(ctx, self, status, "sequence")

        return _emit(ctx, self, BehaviorStatus.SUCCESS, "sequence")


@dataclass(slots=True)
class Selector:
    """OR: tick children left-to-right until one succeeds."""

    name: str
    children: list[BehaviorNode] = field(default_factory=list)

    def tick(self, ctx: TickContext) -> BehaviorStatus:
        _emit(ctx, self, BehaviorStatus.RUNNING, "selector")

        for child in self.children:
            status = child.tick(ctx)
            if status != BehaviorStatus.FAILURE:
                return _emit(ctx, self, status, "selector")

        return _emit(ctx, self, BehaviorStatus.FAILURE, "selector")
