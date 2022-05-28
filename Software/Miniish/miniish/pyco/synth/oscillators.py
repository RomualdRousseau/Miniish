from .locals import *

def sin(x):
    return np.sin(x)

def square(x):
    return np.copysign(1, np.sin(x))

def sawtooth(x):
    return 2 * (x / TWO_PI - np.floor(x / TWO_PI + 0.5))

def ramp(x):
    return -sawtooth(x + ONE_PI)

def triangle(x):
    return 2 * np.abs(sawtooth(x + HALF_PI)) - 1

def noise(x):
    return 0.1 * sin(x) + np.random.uniform(-1, 1, x.shape)
