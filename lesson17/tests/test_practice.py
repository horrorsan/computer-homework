"""期望全部来自checks.py，没有另一套答案。"""
import os
import pytest
from checks import CASES, EXTRA_CASES, run_case
from provided import load_implementation


@pytest.mark.parametrize("case", CASES + EXTRA_CASES, ids=lambda case: case[0])
def test_case(case):
    module = load_implementation(os.environ.get("LESSON17_IMPLEMENTATION"))
    result = run_case(module, case)
    if result["status"] == "pending":
        pytest.skip(result["message"])
    assert result["status"] == "pass", result["message"]
