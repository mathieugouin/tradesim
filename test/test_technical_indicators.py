import numpy as np
import pandas as pd
import pytest
import technical_indicators as ti


@pytest.mark.smoketest
def test_step():
    t = np.arange(-5, 5, 1)
    x = ti.step(t)
    assert len(x) == len(t)
    assert x.min() == 0
    assert x.max() == 1


@pytest.mark.smoketest
def test_step_series():
    t = pd.Series(np.arange(-5, 5, 1))
    x = ti.step(t)
    assert len(x) == len(t)
    assert x.min() == 0
    assert x.max() == 1


@pytest.mark.smoketest
def test_ramp():
    t = np.arange(-5, 5, 1)
    x = ti.ramp(t)
    assert len(x) == len(t)
    assert x.min() == 0
    assert x.max() == t.max()


@pytest.mark.smoketest
def test_ramp_series():
    t = pd.Series(np.arange(-5, 5, 1))
    x = ti.ramp(t)
    assert len(x) == len(t)
    assert x.min() == 0
    assert x.max() == t.max()


@pytest.mark.toimprove
@pytest.mark.smoketest
def test_cross_over():
    t = np.linspace(0, 4 * np.pi, 50)
    s = np.sin(t)
    c = np.cos(t)
    x = ti.cross_over(s, c)
    assert x.min() == False
    assert x.max() == True


@pytest.mark.toimprove
@pytest.mark.smoketest
def test_cross_under():
    t = np.linspace(0, 4 * np.pi, 50)
    s = np.sin(t)
    c = np.cos(t)
    x = ti.cross_under(s, c)
    assert x.min() == False
    assert x.max() == True


@pytest.mark.toimprove
@pytest.mark.smoketest
def test_indicators():
    n = 100
    t = np.arange(n)  # [0 .. n-1]

    # triangle
    # x = np.concatenate((np.arange(0,n/2,1), np.arange(n/2,0,-1)))

    # step
    x = ti.step(t - n/2) * 10

    # ramp
    # x = ramp(t - n/2)

    # normalized random
    # x = np.cumsum(np.random.randn(n))

    # Add noise:
    x = x + 1.2 * np.random.randn(len(x))

    # TBD very dummy tests...
    assert len(ti.sma(x, 10)) == len(x)
    assert len(ti.ema(x, 10)) == len(x)
    assert len(ti.linear_fit(x, 10)) == len(x)
    assert len(ti.iir_lowpass(x, 2, 10)) == len(x)
    assert len(ti.moving_min(x, 10)) == len(x)
    assert len(ti.moving_max(x, 10)) == len(x)
    assert len(ti.aema(x, 10)) == len(x)

    assert len(ti.rate_of_change(x, 20)) == len(x)
    assert len(ti.acceleration(x, 20)) == len(x)


@pytest.mark.smoketest
@pytest.mark.parametrize("indicator", [
        'linear_fit',
        'rate_of_change',
        'acceleration',
        # 'iir_lowpass',
        'ema',
        'aema',
        'sma',
        'moving_min',
        'moving_max',
    ])
@pytest.mark.parametrize("offset", [0, 1, 10])
def test_common_indicator_n_too_big(indicator, offset):
    n = 100
    x = np.arange(n)
    with pytest.raises(ValueError):
        _ = getattr(ti, indicator)(x, n + offset)
    _ = getattr(ti, indicator)(x, n - 1)


@pytest.mark.smoketest
@pytest.mark.parametrize("indicator, min_valid_n", [
        ('linear_fit', 2),
        ('rate_of_change', 2),
        ('acceleration', 3),
        ('ema', 1),  # TBD 2?
        ('aema', 1),  # TBD 2?
        ('sma', 2),
        ('moving_min', 1),  # TBD 2?
        ('moving_max', 1),  # TBD 2?
    ])
def test_common_indicator_n_too_small(indicator, min_valid_n):
    x = np.arange(100)
    for n in range(-5, min_valid_n, 1):  # end loop is excluded
        with pytest.raises(ValueError):
            _ = getattr(ti, indicator)(x, n)
    _ = getattr(ti, indicator)(x, min_valid_n)  # no exception
