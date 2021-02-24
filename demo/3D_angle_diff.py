# Demo of 3D plot using the angle diff

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import cm


def oat(tat, mach):
    return (tat+273.15)/(1+0.2*0.855*mach**2)-273.15


def normalize_deg(x):
    if x > 180:
        x = x - 360
    if x < -180:
        x = x + 360
    return x


vf = np.vectorize(normalize_deg)


def angle_diff(x, y):
    return np.abs(vf(x - y))


def _main():
    fig = plt.figure()
    ax = Axes3D(fig)

    NN = 200

    X = np.linspace(-180, 180, NN)
    Y = np.linspace(-180, 180, NN)
    XX, YY = np.meshgrid(X, Y)
    ZZ = angle_diff(XX, YY)

    ax.set_xlabel('DTK')
    ax.set_ylabel('TRK')
    ax.set_zlabel('Diff')

    ax.plot_surface(XX, YY, ZZ, cmap=cm.coolwarm, linewidth=0, antialiased=True)

    plt.show()
    pass


if __name__ == '__main__':
    _main()
