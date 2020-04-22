import numpy as np
import technical_indicators as ti


# TBD super dummy tests


def test_test_indicator():
    assert -5.0 < ti.test_indicator('XBB.TO') < 5.0


def test_1():
    t = np.arange(-5, 5, 1)
    s = ti.step(t)
    assert len(s) == len(t)
    r = ti.ramp(t)
    assert len(r) == len(t)


def test_cross_over_under():
    t = np.linspace(0, 4 * np.pi, 50)
    s = np.sin(t)
    c = np.cos(t)
    o = ti.cross_over(s, c)
    assert min(o) == 0.0
    assert max(o) == 1.0

    u = ti.cross_under(s, c)
    assert min(u) == 0.0
    assert max(u) == 1.0


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
