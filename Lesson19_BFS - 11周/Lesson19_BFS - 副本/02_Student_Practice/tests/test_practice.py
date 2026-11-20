import pytest
from checks import CHECKS
@pytest.mark.parametrize('name,fn',CHECKS,ids=[x[0] for x in CHECKS])
def test_rule(name,fn):fn()
