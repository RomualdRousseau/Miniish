from .locals import *

def effect_env_adsr_on(t):
    return (1 - np.exp(-TWO_PI * t * 8))

def effect_env_adsr_off(t):
    return (1 - np.exp(-TWO_PI * (1 - t) * 8))

def effect_env_adsr(t):
    return (1 - np.exp(-TWO_PI * t * 8)) * (1 - np.exp(-TWO_PI * (1 - t) * 8))

def effect_env_none(t):
    return 1

def effect_env_fade_in(t):
    return 1 / (1 + np.exp(-(t * 20 - 3)))
    # return np.exp(-TWO_PI * (1 - t))

def effect_env_fade_out(t):
    return  1 - 1 / (1 + np.exp(-(t * 20 - 17)))
    # return np.exp(-TWO_PI * t)
