import numpy as np
import technical_indicators as ti


def _main():
    T = np.arange(-10, 11, 1)
    print T
    print ti.step(T)
    print ti.ramp(T)


if __name__ == '__main__':
    _main()
