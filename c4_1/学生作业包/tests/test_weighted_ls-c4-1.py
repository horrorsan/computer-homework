import pytest

from roslam.c4_1.weighted_ls import weighted_mean_1d


def test_blackboard_equal_and_biased() -> None:
    assert weighted_mean_1d([1.0, 1.2], [1.0, 1.0]) == pytest.approx(1.1)
    assert weighted_mean_1d([1.0, 1.2], [1.0, 4.0]) == pytest.approx(1.16)


def test_single_measurement() -> None:
    assert weighted_mean_1d([3.5], [2.0]) == pytest.approx(3.5)


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        weighted_mean_1d([], [])
    with pytest.raises(ValueError):
        weighted_mean_1d([1.0], [1.0, 2.0])
    with pytest.raises(ValueError):
        weighted_mean_1d([1.0, 2.0], [0.0, 0.0])
    with pytest.raises(ValueError):
        weighted_mean_1d([1.0], [-1.0])
