import numpy as np
from pygame.locals import *
from ..globals import *

ONE_PI = np.pi
TWO_PI = 2 * np.pi
HALF_PI = np.pi / 2

TICK = 60 / (16 * BPM)

SAMPLE_ONE_NOTE_SIZE = 50

SD_PREBUFFER_SIZE = 3

PITCHES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

PENTASCALE = ["C", "D", "E", "G", "A"]

class SYNTH: pass
