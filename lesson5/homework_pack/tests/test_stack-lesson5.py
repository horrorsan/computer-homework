import pytest

from src.herodungeon.m1_inventory import StackEmptyError, UndoStack


def test_lifo_order() -> None:
    stack = UndoStack()
    stack.push("move")
    stack.push("attack")

    assert stack.peek() == "attack"
    assert stack.pop() == "attack"
    assert stack.pop() == "move"
    assert stack.is_empty


def test_iteration_is_top_down() -> None:
    stack = UndoStack()
    for operation in ("a", "b", "c"):
        stack.push(operation)

    assert list(stack) == ["c", "b", "a"]
    assert stack.items == ("a", "b", "c")


def test_max_depth_evicts_oldest_operation() -> None:
    stack = UndoStack(max_depth=2)
    stack.push("first")
    stack.push("second")
    stack.push("third")

    assert stack.items == ("second", "third")
    assert any(event.type == "evict" for event in stack.recorder.events)


def test_invalid_depth_and_underflow() -> None:
    with pytest.raises(ValueError):
        UndoStack(max_depth=0)

    stack = UndoStack()
    with pytest.raises(StackEmptyError):
        stack.pop()
    assert stack.recorder.events[-1].type == "underflow"
