import pytest

from herodungeon.m1_inventory import ActionQueue, QueueEmptyError


def test_fifo_order_and_events() -> None:
    queue = ActionQueue()
    queue.enqueue("a")
    queue.enqueue("b")

    assert queue.dequeue() == "a"
    assert queue.peek() == "b"
    assert len(queue) == 1
    assert "enqueue" in {event.type for event in queue.recorder.events}


def test_drain_preserves_order() -> None:
    queue = ActionQueue()
    for action in ("a", "b", "c"):
        queue.enqueue(action)

    assert queue.drain() == ["a", "b", "c"]
    assert queue.is_empty


def test_buffer_is_compacted_and_stays_correct() -> None:
    queue = ActionQueue()
    for index in range(6):
        queue.enqueue(index)
    for _ in range(3):
        queue.dequeue()

    assert "compact" in {event.type for event in queue.recorder.events}
    assert list(queue.items) == [3, 4, 5]

    queue.enqueue(6)
    assert queue.drain() == [3, 4, 5, 6]


def test_empty_queue_raises_and_emits_underflow() -> None:
    queue = ActionQueue()

    with pytest.raises(QueueEmptyError):
        queue.dequeue()
    with pytest.raises(QueueEmptyError):
        queue.peek()

    assert [event.type for event in queue.recorder.events] == [
        "underflow",
        "underflow",
    ]
