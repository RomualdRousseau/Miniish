from .locals import *

noise_buffer = np.random.uniform(-1, 1, int(SAMPLING_RATE / 8))
noise_buffer_x = np.linspace(0, TWO_PI, noise_buffer.shape[0], False)

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
    xx = np.linspace(0, x.shape[0], noise_buffer.shape[0], False)
    return np.interp(x, xx, noise_buffer) 
