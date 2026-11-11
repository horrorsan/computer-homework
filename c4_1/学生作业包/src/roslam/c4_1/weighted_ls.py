"""C4-1: 1D weighted least squares (two-radar blackboard example)."""

from __future__ import annotations

from typing import Sequence


def weighted_mean_1d(measurements: Sequence[float], weights: Sequence[float]) -> float:
    """Return x* = argmin_x Σ w_i (z_i - x)^2.

    Requirements:
    * same length; at least one measurement
    * weights ≥ 0; total weight > 0 else ValueError
    """
    if len(measurements) != len(weights):
        raise ValueError("measurements and weights must have the same length")

    if len(measurements) == 0:
        raise ValueError("at least one measurement is required")

    if any(w < 0 for w in weights):
        raise ValueError("weights must be non-negative")

    total_weight = float(sum(weights))
    if total_weight <= 0.0:
        raise ValueError("total weight must be positive")

    weighted_sum = float(
        sum(w * z for w, z in zip(weights, measurements))
    )

    return weighted_sum / total_weight