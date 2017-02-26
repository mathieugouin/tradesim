import technical_indicators as ti

%load_ext autoreload
%autoreload 2

# step
N = 10
t = np.arange(N)
X = np.zeros(len(t)/2)
X = np.concatenate((X, X+1))

stem(t, X)

R = random.random(X.size)
R = R * .8
R = R * .8
R = R * .8
std(R)
Xr = X + R

plot(abs(fft.rfft(xn))


xn = Xr
b, a = butter(3, 0.01)
# tbd simple filter


y = filtfilt(b, a, xn)
plot(t,xn,t,y)

p2 = polyfit(t[-150:],xn[-150:],2)
plot(t[-150:], polyval(p2, t)[-150:])
std(xn[-150:] - polyval(p2, t[-150:]))


n = 100
r = np.array([polyfit(t[i-n:i], xn[i-n:i], 1)[0] for i in arange(n, len(t), 1)])
r2 = np.concatenate((zeros(n), r))
plot(t, xn)
twinx()
plot(t, r2, 'r')
plot(t, zeros(len(t)), 'y')

# plot
plot(x, y)
figure(2)
plot(x, y**2)



# filters
N = 200
k = 2.0/(N+1)
b = [1]
a = [1/k, (k-1)/k]



#==================================

def main():
    pass

if __name__ == '__main__':
    main()
