import pytest

from herodungeon.core.events import EventRecorder
from herodungeon.m1_inventory import max_damage_window, window_states

DAMAGE_LOG = [4, 11, 3, 9, 21, 2, 7, 15, 6, 8]


def test_best_window_matches_brute_force() -> None:
    size = 3
    start, total = max_damage_window(DAMAGE_LOG, size)

    brute = max(
        (sum(DAMAGE_LOG[i : i + size]), -i)
        for i in range(len(DAMAGE_LOG) - size + 1)
    )
    assert total == brute[0]
    assert start == -brute[1]


def test_events_cover_every_slide() -> None:
    recorder = EventRecorder()
    size = 4
    max_damage_window(DAMAGE_LOG, size, recorder=recorder)

    slides = [e for e in recorder.events if e.type == "window_slide"]
    assert len(slides) == len(DAMAGE_LOG) - size
    assert recorder.events[0].type == "window_init"
    assert recorder.events[-1].type == "window_best"


def test_ties_keep_earliest_window() -> None:
    start, total = max_damage_window([5, 1, 5, 1, 5, 1], 2)

    assert (start, total) == (0, 6)


def test_window_states_are_renderable() -> None:
    states = window_states(DAMAGE_LOG, 3)

    assert len(states) == len(DAMAGE_LOG) - 2
    assert states[0]["values"] == [4, 11, 3]
    assert states[0]["window_sum"] == 18


@pytest.mark.parametrize("size", [0, -1, len(DAMAGE_LOG) + 1])
def test_invalid_sizes_rejected(size: int) -> None:
    with pytest.raises(ValueError):
        max_damage_window(DAMAGE_LOG, size)
