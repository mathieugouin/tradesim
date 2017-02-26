# IPython log file

import technical_indicators as ti
get_ipython().magic(u'load_ext autoreload')
get_ipython().magic(u'autoreload 2')
get_ipython().magic(u'load_ext autoreload')
get_ipython().magic(u'autoreload 2')
N = 10
t = np.arange(N)
X = np.zeros(len(t)/2)
X = np.concatenate((X, X+1))
plot(t, X)
plot(t, X, linestyle='steps--')
stemÉ
get_ipython().magic(u'pinfo stem')
t
X
stem(t, X)
plot(t, ti.mmmax(t, 3))
plot(t, ti.mmax(t, 3))
plot(t, ti.mmax(X, 3))
np.range
get_ipython().magic(u'cls ')
get_ipython().magic(u'pinfo linspace')
arange(0,10,1)
arange(10,0,-1)
concatenate((arange(0,10,1), arange(10,0,-1)))
plot(concatenate((arange(0,10,1), arange(10,0,-1))))
stem((concatenate((arange(0,10,1), arange(10,0,-1))))
)
concatenate((arange(0,10,1), arange(10,0,-1)))
x = concatenate((arange(0,10,1), arange(10,0,-1)))
t = range(len(x))
stem(t, x)
plot(t, ti.mmax(x, 3))
stem(t, x)
plot(t, ti.mmax(x, 3), 'r')
stem(t, x)
plot(t, ti.mmax(x, 3), 'g')
grid()
N = 100
 t = np.arange(N)
t = np.arange(N)
X = np.concatenate((np.arange(0,N/2,1), np.arange(N/2,0,-1)))
range(len(X))
X
t
plot(x, X)
np.arange(len(X))
t = np.arange(len(X))
plot(t, X)
stem(t, X)
grid()
i = 52
n = 3
max(X[max(0, i-n-1):i+1])
i
i = 53
max(X[max(0, i-n-1):i+1])
X[50:51
]
X[50:51
]
X[50:51]
max(_)
plot(t, ti.mmax(x, 3), 'g')
plot(t, ti.mmax(X, 3), 'g')
    if n < 1:
            raise "n must be >= 1"
get_ipython().magic(u'hist')
get_ipython().magic(u'cls ')
get_ipython().magic(u'logstart')
quit()
