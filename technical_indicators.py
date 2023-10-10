"""Provides various utility functions and technical indicators."""

# To make print working for Python2/3
from __future__ import print_function

import numpy as np
from scipy import signal


# Error reporting
def _check_input(n, n_min, n_max):
    if n < n_min:
        raise ValueError("n must be >= %d" % n_min)
    if n >= n_max:
        raise ValueError("n too big compared to the size of the input array")


# -------------------------------------
# Various technical indicators
# -------------------------------------

def linear_fit(x, n):
    """Linear regression of 'n' points used to give the smoothed point."""
    _check_input(n, 2, len(x))
    t = np.arange(len(x))
    y = np.array(
        [np.polyval(
            np.polyfit(
                t[i-n+1:i+1], x[i - n + 1:i + 1], 1), i) for i in np.arange(n - 1, len(t), 1)])
    # NaN at beginning (invalid value)
    y = np.concatenate((np.array([np.nan] * (n-1)), y))
    return y


def rate_of_change(x, n):
    """Return the rate of change (1st derivative) based on 'n' points linear regression."""
    _check_input(n, 2, len(x))
    t = np.arange(len(x))
    y = np.array(
        [np.polyfit(
            t[i - n + 1:i + 1],
            x[i - n + 1:i + 1],
            1)[0] for i in np.arange(n - 1, len(t), 1)]
    )
    # NaN at beginning (invalid value)
    # y = np.concatenate((np.array([np.nan] * (n-1)), y))
    # Zero at beginning (invalid value)
    y = np.concatenate((np.zeros(n - 1), y))
    return y


def acceleration(x, n):
    """Return the "acceleration" (2nd derivative) based on 'n' points 2nd order regression."""
    _check_input(n, 3, len(x))
    t = np.arange(len(x))
    y = np.array(
        [np.polyfit(
            t[i - n + 1:i + 1],
            x[i - n + 1:i + 1],
            2)[0] * 2 for i in np.arange(n - 1, len(t), 1)])
    # NaN at beginning (invalid value)
    # y = np.concatenate((np.array([np.nan] * (n-1)), y))
    # Zero at beginning (invalid value)
    y = np.concatenate((np.zeros(n - 1), y))
    return y


def iir_lowpass(x, order, period):
    """Lowpass IIR filter."""
    wn = 2.0/period
    b, a = signal.iirfilter(
        order,
        wn,
        rp=None,
        rs=None,
        btype='lowpass',
        analog=False,
        ftype='butter',
        output='ba'
    )
    zi = signal.lfilter_zi(b, a)
    y, _ = signal.lfilter(b, a, x, zi=zi * x[0])
    return y


def ema(x, n):
    """Exponential Moving Average."""
    _check_input(n, 1, len(x))

    k = 2.0 / (n + 1)

    y = np.zeros(x.size)
    y[0] = x[0]  # init

    for i in range(1, x.size):
        y[i] = k * x[i] + (1 - k) * y[i - 1]

    return y


def aema(x, n):
    """Adaptive EMA (my invention...)."""
    _check_input(n, 1, len(x))
    e = ema(x, n)
    # TBD: tune factor here...
    y = e + 0.5 * ema(x - e, n)
    return y


def sma(x, n):
    """Simple Moving Average.  From y[:n-2] is invalid."""
    _check_input(n, 2, len(x))
    c = np.ones(n) / n
    y = np.convolve(x, c)[:-(n - 1)]
    # invalidate the range
    y[:n-2] = np.nan
    return y


def cross_over(x1, x2):
    """If x1 just crossed over x2, in numeric form (0, 1)."""
    return np.concatenate((np.zeros(1), np.diff((x1 > x2) * 1.0))) > 0.5


def cross_under(x1, x2):
    """If x1 just crossed under x2, in numeric form (0, 1)."""
    return np.concatenate((np.zeros(1), np.diff((x1 < x2) * 1.0))) > 0.5


def moving_min(x, n):
    """Moving minimum over the last n elements."""
    _check_input(n, 1, len(x))
    return np.array([min(x[max(0, i - n + 1):i + 1]) for i in range(len(x))])


def moving_max(x, n):
    """Moving maximum over the last n elements."""
    _check_input(n, 1, len(x))
    return np.array([max(x[max(0, i - n + 1):i + 1]) for i in range(len(x))])
