import pytest

from checks import CheckSuite

CHECKS = CheckSuite().checks()


@pytest.mark.parametrize("check", CHECKS, ids=lambda item: f"{item.group}-{item.name}")
def test_lesson15(check) -> None:
    check.run()
