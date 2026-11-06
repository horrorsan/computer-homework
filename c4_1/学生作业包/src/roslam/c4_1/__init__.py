"""C4-1 student stubs: three-problem table + 1D LS + GN/LM."""

from .problems import ProblemKind, classify_scenario
from .weighted_ls import weighted_mean_1d
from .nonlinear import gauss_newton_1d, levenberg_marquardt_1d

__all__ = [
    "ProblemKind",
    "classify_scenario",
    "weighted_mean_1d",
    "gauss_newton_1d",
    "levenberg_marquardt_1d",
]
