"""C4-1: classify localization / mapping / SLAM from known vs estimate.

Implement ``classify_scenario``. Do not hard-code the classroom scene names;
derive the kind from the two sets only.
"""

from __future__ import annotations

from enum import Enum
from typing import Iterable


class ProblemKind(str, Enum):
    LOCALIZATION = "localization"
    MAPPING = "mapping"
    SLAM = "slam"


_KNOWN_ALIASES = {
    "m": "map",
    "map": "map",
    "地图": "map",
    "x": "pose",
    "pose": "pose",
    "位姿": "pose",
    "轨迹": "pose",
    "z": "obs",
    "obs": "obs",
    "observation": "obs",
    "观测": "obs",
    "激光": "obs",
    "u": "ctrl",
    "ctrl": "ctrl",
    "control": "ctrl",
    "控制": "ctrl",
    "里程计": "ctrl",
}


def _normalize(items: Iterable[str]) -> frozenset[str]:
    out: set[str] = set()
    for raw in items:
        key = _KNOWN_ALIASES.get(str(raw).strip().lower(), str(raw).strip().lower())
        out.add(key)
    return frozenset(out)


def classify_scenario(known: Iterable[str], estimate: Iterable[str]) -> ProblemKind:
    """Return ProblemKind from known inputs and quantities to estimate.

    Rules:
    * localization — known has map, not pose; estimate has pose, not map
    * mapping — known has pose, not map; estimate has map, not pose
    * slam — known has neither map nor pose; estimate has both
    * otherwise raise ValueError
    """
    # TODO: 归一化 known / estimate
    # TODO: 按三问题表判定并返回 ProblemKind
    # TODO: 无法判定时 raise ValueError
    raise NotImplementedError("implement classify_scenario")
