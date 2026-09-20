"""M1 lesson 6: sliding window over the recent combat damage log.

Do not recompute each window from scratch. Slide by subtracting the leaving
value and adding the entering value so the whole scan is O(n).
"""

from __future__ import annotations

from typing import Any, Sequence

from herodungeon.core.events import EventRecorder

SOURCE = "m1.sliding_window"


def _validate(damage_log: Sequence[int], size: int) -> None:
    if size <= 0:
        raise ValueError("window size must be positive")
    if size > len(damage_log):
        raise ValueError(
            f"window size {size} exceeds damage log length {len(damage_log)}"
        )


def max_damage_window(
    damage_log: Sequence[int],
    size: int,
    recorder: EventRecorder | None = None,
) -> tuple[int, int]:
    """Return ``(start_index, window_sum)`` of the highest-damage window.

    Ties must keep the earliest window.
    """
    _validate(damage_log, size)
    recorder = recorder or EventRecorder()
    # TODO: 先算第一个窗口的和，emit window_init
    current_sum = sum(damage_log[:size])

    best_sum = current_sum
    best_start = 0

    recorder.emit(
        event_type="window_init",
        source=SOURCE,
        start=0,
        end=size,
        window_sum=current_sum
    )
    # TODO: 每次窗口右移：减去离开的数，加上进入的数，emit window_slide
    for i in range(size, len(damage_log)):
        start = i - size + 1
        end = i + 1

        start = i - size + 1
        end = i + 1

        current_sum = current_sum - damage_log[i - size] + damage_log[i]

        recorder.emit(
            event_type="window_slide",
            source=SOURCE,
            start=start,
            end=end,
            window_sum=current_sum
        )
    # TODO: 只有新窗口和严格更大时才更新最优；平局保留更早的窗口
        if current_sum > best_sum:
            best_sum = current_sum
            best_start = start
    # TODO: 最后 emit window_best，返回 (best_start, best_sum)
    recorder.emit(
        event_type="window_best",
        source=SOURCE,
        start=best_start,
        end=best_start + size,
        window_sum=best_sum
    )

    return best_start, best_sum

def window_states(
    damage_log: Sequence[int], size: int
) -> list[dict[str, Any]]:
    """Return every window as {start, end, values, window_sum}."""
    _validate(damage_log, size)
    # TODO: 生成每一个窗口的 start/end/values/window_sum
    states = []
    current_sum = sum(damage_log[:size])  # 第一个窗口的和
    
    for i in range(len(damage_log) - size + 1):
        start = i
        end = i + size
        
        if i > 0:
            current_sum = current_sum - damage_log[i - 1] + damage_log[i + size - 1]
            
        states.append({
            "start": start,
            "end": end,
            "values": list(damage_log[start:end]),
            "window_sum": current_sum
        })
        
    return states

