# Demo of 3D plot using the OAT formula

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D


def oat(tat, mach):
    return (tat+273.15)/(1+0.2*0.855*mach**2)-273.15


def _main():
    fig = plt.figure()
    ax = Axes3D(fig)

    mmax = 4.0959375
    NN = 25

    T = np.linspace(-512, 512, NN)
    M = np.linspace(0, mmax, NN)
    TT, MM = np.meshgrid(T, M)
    OO = oat(TT, MM)

    ax.plot_wireframe(TT, MM, OO)

    N = 50

    t = np.concatenate((
        np.linspace(-512, 288.25, N),
        np.linspace(288.25, 511.75, N),
        np.linspace(511.75, 511.75, N)))
    m = np.concatenate((
        np.linspace(0, mmax, N),
        np.linspace(mmax, 2.36525, N),
        np.linspace(2.36525,0,N)))
    o = oat(t, m)

    ax.scatter(t, m, o, c='r')

    ax.set_xlabel('TAT')
    ax.set_ylabel('Mach')
    ax.set_zlabel('OAT')

    plt.show()


if __name__ == '__main__':
    _main()
