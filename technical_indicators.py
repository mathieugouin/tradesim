import numpy as np
#import scipy as sp
import scipy.signal as signal

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

def linFit(X, n):
    if n < 2:
        raise "n must be >= 2"
    t = np.arange(len(X))
    Y = np.array([np.polyval(np.polyfit(t[i-n+1:i+1], X[i-n+1:i+1], 1), i) for i in np.arange(n-1, len(t), 1)])
    Y = np.concatenate((np.array([np.nan] * (n-1)), Y))
    return Y

def linFitROC(X, n):
    t = np.arange(len(X))
    Y = np.array([np.polyfit(t[i-n+1:i+1], X[i-n+1:i+1], 1)[0] for i in np.arange(n-1, len(t), 1)])
    # NaN at beginning (invalid value)
    #Y = np.concatenate((np.array([np.nan] * (n-1)), Y))
    # Zero at beginning (invalid value)
    Y = np.concatenate((np.array([0] * (n-1)), Y))
    return Y

def linFitROC2(X, n):
    t = np.arange(len(X))
    Y = np.array([np.polyfit(t[i-n+1:i+1], X[i-n+1:i+1], 2)[0]*2 for i in np.arange(n-1, len(t), 1)])
    # NaN at beginning (invalid value)
    #Y = np.concatenate((np.array([np.nan] * (n-1)), Y))
    # Zero at beginning (invalid value)
    Y = np.concatenate((np.array([0] * (n-1)), Y))
    return Y

# Filter Design
def iir(X, order, period):
    wn = 2.0/period
    b, a = signal.iirfilter(order, wn, rp = None, rs = None,
                            btype = 'lowpass', analog = 0,
                            ftype = 'butter', output = 'ba')
    zi = signal.lfilter_zi(b, a)
    Y, zf = signal.lfilter(b, a, X, zi = zi * X[0])
    return Y

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

# Adaptive EMA
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

# Moving minimum
def mmin(X, n):
    if n < 1:
        raise "n must be >= 1"
    return np.array([min(X[max(0, i-n+1):i+1]) for i in xrange(len(X))])

# Moving maximum
def mmax(X, n):
    if n < 1:
        raise "n must be >= 1"
    return np.array([max(X[max(0, i-n+1):i+1]) for i in xrange(len(X))])

# To test various indicators
def _main():
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    N = 100
    T = np.arange(N)

    # triangle
    #X = np.concatenate((np.arange(0,N/2,1), np.arange(N/2,0,-1)))
    # step
    X = step(T - N/2) * 10
    # ramp
    #X = ramp(T - N/2)

    #X = np.cumsum(np.random.randn(N))

    #X = np.sin(8 * np.pi/N * t) + (.1 * t)

    #X = 20 * np.sin(2 * 2*np.pi/N * T)

    # Add noise:
    #X = X + 2.0 * np.random.randn(len(X))

    #Y = ema(X, 3)
    #Y = iir(X, 3, 20)
    #Y = linFitROC(X, 2)
    #Y = linFit(X, 5)
    #print Y

    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax.stem(t, X, 'g')
    #fig.hold()
    ax.plot(
        T, X, 'o',
        T, sma(X, 10),
        T, ema(X, 10),
        #T, linFit(X, 10),
        #T, iir(X, 1, 20),
        #T, mmin(X, 10),
        #T, mmax(X, 10)
        T, aema(X, 10)
        )
    ax.grid(True)
    #ax2 = fig.add_subplot(212)
    #ax2.plot(
    #    T, linFitROC2(X, 10), 'o--'
    #    )
    #ax2.grid(True)
    plt.show()

if __name__ == '__main__':
    _main()

