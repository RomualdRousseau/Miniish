from .locals import *

def effect_frq_none(t, f0, f1):
    return f1

def effect_frq_slide(t, f0, f1):
    return (f1 - f0) * t + f0

def effect_frq_vibrato(t, f0, f1):
    return f1 + 1.06 * np.sin(TWO_PI * 6 * t)

def effect_frq_drop(t, f0, f1):
    return f1 * (1 - 0.06 * np.exp(-TWO_PI * (1 - t)))
