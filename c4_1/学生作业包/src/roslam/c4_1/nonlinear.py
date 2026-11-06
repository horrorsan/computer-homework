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
    # TODO: 初始化 xs/costs（含 x0）
    # TODO: 迭代计算 e, J, H, b, delta；H==0 时停止
    # TODO: 更新 x 并记录；|delta|<tol 停止
    raise NotImplementedError("implement gauss_newton_1d")


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
    # TODO: 初始化 x、λ、轨迹
    # TODO: 试探步；代价下降才接受并减小 λ，否则增大 λ
    raise NotImplementedError("implement levenberg_marquardt_1d")
