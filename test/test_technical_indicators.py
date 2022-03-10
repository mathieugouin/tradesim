import numpy as np
import technical_indicators as ti
import pytest


# TBD super dummy tests


@pytest.mark.webtest
def test_test_indicator():
    assert -5.0 < ti.test_indicator('XBB.TO') < 5.0


def test_step():
    t = np.arange(-5, 5, 1)
    s = ti.step(t)
    assert len(s) == len(t)


def test_ramp():
    t = np.arange(-5, 5, 1)
    r = ti.ramp(t)
    assert len(r) == len(t)


# TBD: not very robust test
def test_cross_over():
    t = np.linspace(0, 4 * np.pi, 50)
    s = np.sin(t)
    c = np.cos(t)
    x = ti.cross_over(s, c)
    assert x.min() == False
    assert x.max() == True


# TBD: not very robust test
def test_cross_under():
    t = np.linspace(0, 4 * np.pi, 50)
    s = np.sin(t)
    c = np.cos(t)
    x = ti.cross_under(s, c)
    assert x.min() == False
    assert x.max() == True


def test_data():
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

    # x = np.sin(8 * np.pi/n * t) + (.1 * t)

    # x = 20 * np.sin(2 * 2*np.pi/n * t)

    # Add noise:
    x = x + 1.2 * np.random.randn(len(x))

    assert len(ti.sma(x, 10)) == len(x)
    assert len(ti.ema(x, 10)) == len(x)
    assert len(ti.linear_fit(x, 10)) == len(x)
    assert len(ti.iir_lowpass(x, 2, 10)) == len(x)
    assert len(ti.moving_min(x, 10)) == len(x)
    assert len(ti.moving_max(x, 10)) == len(x)
    assert len(ti.aema(x, 10)) == len(x)

    assert len(ti.rate_of_change(x, 20)) == len(x)
    assert len(ti.acceleration(x, 20)) == len(x)
