import pytest
import numpy as np
import pandas as pd
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
def test_isclose(a, b, result):
    assert mu.isclose(a, b) == result


@pytest.mark.smoketest
def test_step():
    t = np.arange(-5, 5, 1)
    x = mu.step(t)
    assert len(x) == len(t)
    assert x.min() == 0
    assert x.max() == 1


@pytest.mark.smoketest
def test_step_series():
    t = pd.Series(np.arange(-5, 5, 1))
    x = mu.step(t)
    assert len(x) == len(t)
    assert x.min() == 0
    assert x.max() == 1


@pytest.mark.smoketest
def test_ramp():
    t = np.arange(-5, 5, 1)
    x = mu.ramp(t)
    assert len(x) == len(t)
    assert x.min() == 0
    assert x.max() == t.max()


@pytest.mark.smoketest
def test_ramp_series():
    t = pd.Series(np.arange(-5, 5, 1))
    x = mu.ramp(t)
    assert len(x) == len(t)
    assert x.min() == 0
    assert x.max() == t.max()
