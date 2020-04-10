# To make print working for Python2/3
from __future__ import print_function

import math
import numpy as np
#import scipy as sp
import scipy.signal as signal
import tmxstockquote as tmx


# -------------------------------------
# Utility math functions
# -------------------------------------

def step(t):
    """Returns 1 where t >= 0, else 0."""
    y = np.zeros(len(t))
    y[t >= 0] = 1
    return y


def ramp(t):
    """Returns 0 for negative inputs, output equals input for non-negative inputs."""
    return t * step(t)

# -------------------------------------
# Various technical indicators
# -------------------------------------

def linFit(x, n):
    """Linear regression of 'n' points used to give the smoothed point."""
    if n < 2:
        raise "n must be >= 2"
    t = np.arange(len(x))
    Y = np.array([np.polyval(np.polyfit(t[i-n+1:i+1], x[i - n + 1:i + 1], 1), i) for i in np.arange(n - 1, len(t), 1)])
    # NaN at beginning (invalid value)
    Y = np.concatenate((np.array([np.nan] * (n-1)), Y))
    return Y


def rateOfChange(x, n):
    """Return the Rate Of Change (1st derivative) based on 'n' points linear regression."""
    t = np.arange(len(x))
    Y = np.array([np.polyfit(t[i-n+1:i+1], x[i - n + 1:i + 1], 1)[0] for i in np.arange(n - 1, len(t), 1)])
    # NaN at beginning (invalid value)
    #Y = np.concatenate((np.array([np.nan] * (n-1)), Y))
    # Zero at beginning (invalid value)
    Y = np.concatenate((np.zeros(n-1), Y))
    return Y


def acceleration(X, n):
    """Return the "Acceleration" (2nd derivative) based on 'n' points 2nd order regression."""
    t = np.arange(len(X))
    Y = np.array([np.polyfit(t[i-n+1:i+1], X[i-n+1:i+1], 2)[0]*2 for i in np.arange(n-1, len(t), 1)])
    # NaN at beginning (invalid value)
    #Y = np.concatenate((np.array([np.nan] * (n-1)), Y))
    # Zero at beginning (invalid value)
    Y = np.concatenate((np.zeros(n-1), Y))
    return Y


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
    y, _zf = signal.lfilter(b, a, x, zi=zi * x[0])
    return y


def ema(x, n):
    """Exponential Moving Average."""
    if n < 1:
        raise "n must be >= 1"
    if n >= x.size:
        raise "n too big compared to size of array"

    k = 2.0 / (n + 1)

    y = np.zeros(x.size)
    y[0] = x[0] # init

    for i in range(1, x.size):
        y[i] = k * x[i] + (1 - k) * y[i - 1]

    return y


def aema(x, n):
    """Adaptive EMA (my invention...)."""
    if n < 1:
        raise "n must be >= 1"
    if n >= x.size:
        raise "n too big compared to size of array"
    e = ema(x, n)
    # TBD: tune factor here...
    y = e + 0.5 * ema(x - e, int(n))
    return y


def sma(x, n):
    """Simple Moving Average.  From y[:n-2] is invalid."""
    if n < 2:
        raise "n must be > 1"
    c = np.ones(n) / n
    y = np.convolve(x, c)[:-(n - 1)]
    # invalidate the range
    y[:n-2] = np.nan
    return y


def crossOver(x, y, i):
    """If x just crossed over y at index i."""
    c = False
    if i >= 1:
        if x[i - 1] <= y[i - 1] and x[i] > y[i]:
            c = True
    return c


def crossUnder(x, y, i):
    """If x just crossed under y at index i."""
    c = False
    if i >= 1:
        if x[i - 1] >= y[i - 1] and x[i] < y[i]:
            c = True
    return c


def movingMin(x, n):
    """Moving minimum over the last n elements."""
    if n < 1:
        raise "n must be >= 1"
    return np.array([min(x[max(0, i - n + 1):i + 1]) for i in range(len(x))])


def movingMax(x, n):
    """Moving maximum over the last n elements."""
    if n < 1:
        raise "n must be >= 1"
    return np.array([max(x[max(0, i - n + 1):i + 1]) for i in range(len(x))])


def relative_position(symbol):
    """Based on the 52 week range: min = 0.0, max = 1.0."""
    price = tmx.get_price(symbol)
    pmin = tmx.get_52_week_low(symbol)
    pmax = tmx.get_52_week_high(symbol)
    return (price - pmin) / (pmax - pmin)


def relative_range(symbol):
    """TBD."""
    pmin = tmx.get_52_week_low(symbol)
    pmax = tmx.get_52_week_high(symbol)
    return (pmax - pmin) / pmax


def test_indicator(symbol):
    """TBD."""
    # [-1, 1]
    rps = relative_position(symbol) * 2.0 - 1.0

    # [0, 1]
    rr = relative_range(symbol)

    # reduce the rr influence
    return rps * math.pow(rr, 0.1)


# To test various indicators
def _main():
    import matplotlib.pyplot as plt

    print("test_indicator = {}".format(test_indicator('XBB.TO')))

    t = np.arange(-10, 11, 1)
    plt.stem(t, step(t))
    plt.show()

    plt.stem(t, ramp(t))
    plt.show()

    n = 100
    t = np.arange(n) # [0 .. n-1]

    # triangle
    #x = np.concatenate((np.arange(0,n/2,1), np.arange(n/2,0,-1)))

    # step
    x = step(t - n/2) * 10

    # ramp
    #x = ramp(t - n/2)

    # normalized random
    #x = np.cumsum(np.random.randn(n))

    #x = np.sin(8 * np.pi/n * t) + (.1 * t)

    #x = 20 * np.sin(2 * 2*np.pi/n * t)

    # Add noise:
    x = x + 1.2 * np.random.randn(len(x))

    fig = plt.figure()
    ax = fig.add_subplot(211)
    ax.plot(t, x, 'o', label='raw')
    ax.plot(t, sma(x, 10), label='sma')
    ax.plot(t, ema(x, 10), label='ema')
    ax.plot(t, linFit(x, 10), label='linFit')
    ax.plot(t, iir_lowpass(x, 1, 10), label='iir_lowpass')
    ax.plot(t, movingMin(x, 10), label='movingMin')
    ax.plot(t, movingMax(x, 10), label='movingMax')
    ax.plot(t, aema(x, 10), label='aema')
    ax.grid(True)
    ax.legend()

    ax2 = fig.add_subplot(212)
    ax2.plot(t, rateOfChange(x, 20), 'x', label='rateOfChange')
    ax2.plot(t, acceleration(x, 20), 'o--', label='acceleration')
    ax2.grid(True)
    ax2.legend()
    plt.show()


if __name__ == '__main__':
    _main()
