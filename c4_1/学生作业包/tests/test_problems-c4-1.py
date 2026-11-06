import pytest

from roslam.c4_1.problems import ProblemKind, classify_scenario


def test_localization_aliases() -> None:
    assert classify_scenario(["地图", "观测", "控制"], ["位姿"]) is ProblemKind.LOCALIZATION
    assert classify_scenario(["map", "z", "u"], ["x"]) is ProblemKind.LOCALIZATION


def test_mapping() -> None:
    assert classify_scenario(["pose", "z"], ["map"]) is ProblemKind.MAPPING
    assert classify_scenario(["轨迹", "激光"], ["地图"]) is ProblemKind.MAPPING


def test_slam() -> None:
    assert classify_scenario(["z", "u"], ["pose", "map"]) is ProblemKind.SLAM
    assert classify_scenario(["观测", "里程计"], ["位姿", "地图"]) is ProblemKind.SLAM


def test_ambiguous_raises() -> None:
    with pytest.raises(ValueError):
        classify_scenario(["map", "pose"], ["pose"])
    with pytest.raises(ValueError):
        classify_scenario(["z"], ["pose"])
