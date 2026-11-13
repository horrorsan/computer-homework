"""可选的pytest入口；期望和规则只保存在checks.py。"""
import pytest
from checks import CHECKS, EXTRA_CHECKS, run_check
from provided import load_target


@pytest.mark.parametrize("case", CHECKS + EXTRA_CHECKS, ids=lambda c: c.code)
def test_practice(case):
    status, message = run_check(load_target(), case)
    if status == "pending":
        pytest.skip(message)
    assert status == "pass", message
