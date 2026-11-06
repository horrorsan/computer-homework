import math

import pytest

from roslam.c4_1.nonlinear import gauss_newton_1d, levenberg_marquardt_1d


def _square_residual(z: float):
    return lambda x: z - x * x


def _square_jacobian(_z: float):
    return lambda x: -2.0 * x


def test_gauss_newton_finds_sqrt() -> None:
    trace = gauss_newton_1d(1.0, _square_residual(9.0), _square_jacobian(9.0))
    assert trace.xs[0] == pytest.approx(1.0)
    assert trace.xs[-1] == pytest.approx(3.0, abs=1e-6)
    assert trace.costs[-1] < trace.costs[0]
    assert len(trace.deltas) == len(trace.xs) - 1


def test_lm_finds_sqrt() -> None:
    trace = levenberg_marquardt_1d(
        0.5, _square_residual(9.0), _square_jacobian(9.0), lambda0=10.0
    )
    assert trace.xs[-1] == pytest.approx(3.0, abs=1e-4)
    assert math.isfinite(trace.costs[-1])
    assert len(trace.xs) == len(trace.costs)
