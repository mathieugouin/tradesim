# To make print working for Python2/3
from __future__ import print_function

import math
import numpy as np
#import scipy as sp
import scipy.signal as signal
import tmxstockquote as tmx


#-------------------------------------
# Utility math functions
#-------------------------------------

def step(T):
    Y = np.zeros(len(T))
    Y[T >= 0] = 1
    return Y


def ramp(T):
    return T * step(T)

#-------------------------------------
# Various technical indicators
#-------------------------------------


# Linear regression of 'n' points used to give the smoothed point
def linFit(X, n):
    if n < 2:
        raise "n must be >= 2"
    t = np.arange(len(X))
    Y = np.array([np.polyval(np.polyfit(t[i-n+1:i+1], X[i-n+1:i+1], 1), i) for i in np.arange(n-1, len(t), 1)])
    # NaN at beginning (invalid value)
    Y = np.concatenate((np.array([np.nan] * (n-1)), Y))
    return Y


# Return the Rate Of Change (1st derivative) based on 'n' points linear regression
def rateOfChange(X, n):
    t = np.arange(len(X))
    Y = np.array([np.polyfit(t[i-n+1:i+1], X[i-n+1:i+1], 1)[0] for i in np.arange(n-1, len(t), 1)])
    # NaN at beginning (invalid value)
    #Y = np.concatenate((np.array([np.nan] * (n-1)), Y))
    # Zero at beginning (invalid value)
    Y = np.concatenate((np.zeros(n-1), Y))
    return Y


# Return the "Acceleration" (2nd derivative) based on 'n' points 2nd order regression
def acceleration(X, n):
    t = np.arange(len(X))
    Y = np.array([np.polyfit(t[i-n+1:i+1], X[i-n+1:i+1], 2)[0]*2 for i in np.arange(n-1, len(t), 1)])
    # NaN at beginning (invalid value)
    #Y = np.concatenate((np.array([np.nan] * (n-1)), Y))
    # Zero at beginning (invalid value)
    Y = np.concatenate((np.zeros(n-1), Y))
    return Y


# Filter Design
def iir(x, order, period):
    wn = 2.0/period
    b, a = signal.iirfilter(
        order,
        wn,
        rp = None,
        rs = None,
        btype = 'lowpass',
        analog = False,
        ftype = 'butter',
        output = 'ba'
    )
    zi = signal.lfilter_zi(b, a)
    y, _zf = signal.lfilter(b, a, x, zi=zi * x[0])
    return y


# Exponential Moving Average
def ema(X, n):
    if n < 1:
        raise "n must be >= 1"
    if n >= X.size:
        raise "n too big compared to size of array"

    k = 2.0 / (n + 1)

    Y = np.zeros(X.size)
    Y[0] = X[0] # init

    for i in range(1, X.size):
        Y[i] = k * X[i] + (1 - k) * Y[i - 1]

    return Y


# Adaptive EMA (my invention...)
def aema(X, n):
    if n < 1:
        raise "n must be >= 1"
    if n >= X.size:
        raise "n too big compared to size of array"
    E = ema(X, n)
    # TBD: tune factor here...
    Y = E + 0.5 * ema(X - E, int(n))
    return Y


# Simple Moving Average
# from Y[:n-2] is invalid
def sma(X, n):
    if n < 2:
        raise "n must be > 1"
    C = np.ones(n) / n
    Y = np.convolve(X, C)[:-(n-1)]
    # invalidate the range
    Y[:n-2] = np.nan
    return Y


# If X just crossed over Y at bar index i
def crossOver(X, Y, i):
    c = False
    if i >= 1:
        if X[i - 1] <= Y[i - 1] and X[i] > Y[i]:
            c = True
    return c


# If X just crossed under Y at bar index i
def crossUnder(X, Y, i):
    c = False
    if i >= 1:
        if X[i - 1] >= Y[i - 1] and X[i] < Y[i]:
            c = True
    return c


# Moving minimum over the last n element
def movingMin(X, n):
    if n < 1:
        raise "n must be >= 1"
    return np.array([min(X[max(0, i-n+1):i+1]) for i in xrange(len(X))])


# Moving maximum over the last n element
def movingMax(X, n):
    if n < 1:
        raise "n must be >= 1"
    return np.array([max(X[max(0, i-n+1):i+1]) for i in xrange(len(X))])


def relative_position(symbol):
    price = tmx.get_price(symbol)
    pmin = tmx.get_52_week_low(symbol)
    pmax = tmx.get_52_week_high(symbol)
    return (price - pmin) / (pmax - pmin)


def relative_range(symbol):
    pmin = tmx.get_52_week_low(symbol)
    pmax = tmx.get_52_week_high(symbol)
    return (pmax - pmin) / pmax


def test_indicator(symbol):
    # [-1, 1]
    rps = relative_position(symbol) * 2.0 - 1.0

    # [0, 1]
    rr = relative_range(symbol)

    # reduce the rr influence
    return rps * math.pow(rr, 0.1)


# To test various indicators
def _main():
    import matplotlib.pyplot as plt

    print(test_indicator('XBB.TO'))

    N = 100
    T = np.arange(N) # [0 .. N-1]

    # triangle
    #X = np.concatenate((np.arange(0,N/2,1), np.arange(N/2,0,-1)))

    # step
    X = step(T - N/2) * 10

    # ramp
    #X = ramp(T - N/2)

    # normalized random
    #X = np.cumsum(np.random.randn(N))

    #X = np.sin(8 * np.pi/N * t) + (.1 * t)

    #X = 20 * np.sin(2 * 2*np.pi/N * T)

    # Add noise:
    #X = X + 0.2 * np.random.randn(len(X))

    #Y = ema(X, 3)
    #Y = iir(X, 3, 20)
    #Y = rateOfChange(X, 2)
    #Y = linFit(X, 5)
    #print(Y)

    fig = plt.figure()
    ax = fig.add_subplot(211)
    #ax.stem(t, X, 'g')
    #fig.hold()
    ax.plot(
        T, X, 'o',
        T, sma(X, 10),
        T, ema(X, 10),
        #T, linFit(X, 10),
        #T, rateOfChange(X, 10),
        #T, acceleration(X, 10),
        #T, iir(X, 1, 10),
        #T, movingMin(X, 10),
        #T, movingMax(X, 10)
        #T, aema(X, 10)
        )
    ax.grid(True)

    ax2 = fig.add_subplot(212)
    ax2.plot(
        T, rateOfChange(X, 20), 'x',
        T, acceleration(X, 20), 'o--'
        )
    ax2.grid(True)
    plt.show()


if __name__ == '__main__':
    _main()
