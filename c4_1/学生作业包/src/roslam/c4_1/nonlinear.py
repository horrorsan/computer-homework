"""C4-1: scalar Gauss-Newton and Levenberg-Marquardt.

``residual(x)`` and ``jacobian(x)`` are callables provided by the caller.
Return a ``SolveTrace`` with the full iteration history.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence


ResidualFn = Callable[[float], float]
JacobianFn = Callable[[float], float]


@dataclass(frozen=True)
class SolveTrace:
    xs: tuple[float, ...]
    costs: tuple[float, ...]
    deltas: tuple[float, ...]


def _cost(residuals: Sequence[float]) -> float:
    return float(sum(r * r for r in residuals))


def gauss_newton_1d(
    x0: float,
    residual: ResidualFn,
    jacobian: JacobianFn,
    *,
    max_iters: int = 20,
    tol: float = 1e-10,
) -> SolveTrace:
    """Scalar GN: H=J², b=J·e, Δx=-b/H, x←x+Δx until |Δx|<tol or max_iters."""
    x = float(x0)
    xs = [x]
    costs = [_cost([residual(x)])]
    deltas: list[float] = []

    for _ in range(max_iters):
        e = residual(x)
        J = jacobian(x)
        H = J * J
        b = J * e

        if H == 0.0:
            break

        delta = -b / H
        x = x + delta

        deltas.append(float(delta))
        xs.append(float(x))
        costs.append(_cost([residual(x)]))

        if abs(delta) < tol:
            break

    return SolveTrace(tuple(xs), tuple(costs), tuple(deltas))


def levenberg_marquardt_1d(
    x0: float,
    residual: ResidualFn,
    jacobian: JacobianFn,
    *,
    max_iters: int = 30,
    tol: float = 1e-10,
    lambda0: float = 1e-3,
) -> SolveTrace:
    """Scalar LM: (H+λ)Δx=-b; accept only cost-decreasing steps.

    On success: λ ← max(λ/10, 1e-12). On failure: λ ← min(λ*10, 1e12),
    record delta=0 and keep x unchanged (still append to xs/costs).
    """
    x = float(x0)
    lam = float(lambda0)

    xs = [x]
    costs = [_cost([residual(x)])]
    deltas: list[float] = []

    for _ in range(max_iters):
        e = residual(x)
        J = jacobian(x)
        H = J * J
        b = J * e

        current_cost = _cost([e])
        denom = H + lam

        if denom == 0.0:
            break

        delta = -b / denom
        x_trial = x + delta
        trial_cost = _cost([residual(x_trial)])

        if trial_cost < current_cost:
            x = x_trial

            deltas.append(float(delta))
            xs.append(float(x))
            costs.append(float(trial_cost))

            lam = max(lam / 10.0, 1e-12)

            if abs(delta) < tol:
                break
        else:
            deltas.append(0.0)
            xs.append(float(x))
            costs.append(float(current_cost))

            lam = min(lam * 10.0, 1e12)

    return SolveTrace(tuple(xs), tuple(costs), tuple(deltas))
