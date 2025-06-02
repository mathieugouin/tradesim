import numpy as np
import matplotlib.pyplot as plt

import parent_import
import technical_indicators as ti


# To test various indicators
def _main():

    t = np.arange(-5, 5, 1)
    s = ti.step(t)
    r = ti.ramp(t)

    plt.plot(t, s, marker='x', linestyle='None', label='step')
    plt.plot(t, r, marker='o', markerfacecolor='None', linestyle='None', label='ramp')
    plt.legend()
    plt.show()

    t = np.linspace(0, 4 * np.pi, 50)
    s = np.sin(t)
    c = np.cos(t)
    o = ti.cross_over(s, c)
    u = ti.cross_under(s, c)

    fig = plt.figure()
    ax = fig.add_subplot(211)
    ax.plot(t, s, marker='.', label='sin')
    ax.plot(t, c, marker='x', label='cos')
    ax.legend()

    ax2 = fig.add_subplot(212)
    ax2.plot(t, o * 1, marker='^', markerfacecolor='None', linestyle='None', label='cross over')
    ax2.plot(t, u * 1, marker='v', markerfacecolor='None', linestyle='None', label='cross under')
    ax2.legend()
    plt.show()

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

    fig = plt.figure()
    ax = fig.add_subplot(211)
    ax.plot(t, x, 'o', label='raw')
    ax.plot(t, ti.sma(x, 10), label='sma')
    ax.plot(t, ti.ema(x, 10), label='ema')
    ax.plot(t, ti.linear_fit(x, 10), label='linear_fit')
    ax.plot(t, ti.iir_lowpass(x, 1, 10), label='iir_lowpass')
    ax.plot(t, ti.moving_min(x, 10), label='moving_min')
    ax.plot(t, ti.moving_max(x, 10), label='moving_max')
    ax.plot(t, ti.aema(x, 10), label='aema')
    ax.grid(True)
    ax.legend()

    ax2 = fig.add_subplot(212)
    ax2.plot(t, ti.rate_of_change(x, 20), 'x', label='rate_of_change')
    ax2.plot(t, ti.acceleration(x, 20), 'o--', label='acceleration')
    ax2.grid(True)
    ax2.legend()
    plt.show()


if __name__ == '__main__':
    _main()
