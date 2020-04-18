import numpy as np
import scipy as sp
# import scipy.fftpack as spf
import scipy.signal as sps
import matplotlib.pyplot as plt
# import pandas as pd

# import technical_indicators as ti
# import stock_db_mgr as sdm


#   %load_ext autoreload
#   %autoreload 2

# step
N = 10
t = np.arange(N)
X = np.zeros(len(t)/2)
X = np.concatenate((X, X+1))

plt.stem(t, X)

R = np.random.random(X.size)
R = R * .8
R = R * .8
R = R * .8
sp.std(R)
Xr = X + R

xn = Xr
plt.plot(abs(np.fft.rfft(xn)))


b, a = sps.butter(3, 0.01)

y = sps.filtfilt(b, a, xn)
plt.plot(t, xn, t, y)

p2 = np.polyfit(t[-150:], xn[-150:], 2)
plt.plot(t[-150:], np.polyval(p2, t)[-150:])
sp.std(xn[-150:] - np.polyval(p2, t[-150:]))


n = 100
r = np.array([np.polyfit(t[i-n:i], xn[i-n:i], 1)[0] for i in np.arange(n, len(t), 1)])
r2 = np.concatenate((np.zeros(n), r))
plt.plot(t, xn)
plt.twinx()
plt.plot(t, r2, 'r')
plt.plot(t, np.zeros(len(t)), 'y')

# plot
x = np.arange(10)
y = 2 * x + 3
plt.plot(x, y)
plt.figure(2)
plt.plot(x, y**2)

# filters
N = 200
k = 2.0/(N+1)
b = [1]
a = [1/k, (k-1)/k]


