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
    known_set = _normalize(known)
    estimate_set = _normalize(estimate)

    known_map = "map" in known_set
    known_pose = "pose" in known_set

    estimate_map = "map" in estimate_set
    estimate_pose = "pose" in estimate_set

    if known_map and not known_pose and estimate_pose and not estimate_map:
        return ProblemKind.LOCALIZATION

    if known_pose and not known_map and estimate_map and not estimate_pose:
        return ProblemKind.MAPPING

    if (
        not known_map
        and not known_pose
        and estimate_map
        and estimate_pose
    ):
        return ProblemKind.SLAM

    raise ValueError("cannot classify scenario")
