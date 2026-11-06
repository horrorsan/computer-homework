"""C4-1: 1D weighted least squares (two-radar blackboard example)."""

from __future__ import annotations

from typing import Sequence


def weighted_mean_1d(measurements: Sequence[float], weights: Sequence[float]) -> float:
    """Return x* = argmin_x Σ w_i (z_i - x)^2.

    Requirements:
    * same length; at least one measurement
    * weights ≥ 0; total weight > 0 else ValueError
    """
    # TODO: 校验长度与空输入
    # TODO: 累加 Σ w、Σ w z，返回加权平均
    raise NotImplementedError("implement weighted_mean_1d")
