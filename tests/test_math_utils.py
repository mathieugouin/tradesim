import pytest
import math_utils as mu


@pytest.mark.parametrize('a,b,result', [
    (0, 0, True),
    (.23, .23, True),
    (.23465498735, .234654987351, True),
    (1e3, 1.001e3, False),
    (1e6, 1.001e6, False),
    (1e9, 1.001e9, False),
    (1e12, 1.001e12, False),
    (1e3, 1, False),
    (1e6, 1, False),
    (1e9, 1, False),
    (1e12, 1, False),
    (-.001, 0, False),
])
def test_calc_commission(a, b, result):
    assert mu.isclose(a, b) == result
