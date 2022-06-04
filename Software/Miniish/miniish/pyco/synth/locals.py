import numpy as np
from pygame.locals import *
from ..globals import *

ONE_PI = np.pi
TWO_PI = 2 * np.pi
HALF_PI = np.pi / 2

NEEDSAMPLE = USEREVENT + 1
BUFFERS_COUNT = 3
TICK = 60 / (16 * BPM)

SAMPLE_ONE_NOTE_SIZE = 50

PITCHES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

class SYNTH: pass
