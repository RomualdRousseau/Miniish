from .locals import *
from .oscillators import *
from .envelopes import *
from .modulators import *

import sounddevice as sd

OSCILLATORS = [
        sin,
        triangle,
        square,
        sawtooth,
        ramp,
        noise
        ]

EFFECTS = [
        (effect_frq_none, effect_env_none),             # None
        (effect_frq_none, effect_env_fade_in),          # Fade In
        (effect_frq_none, effect_env_fade_out),         # Fade Out
        (effect_frq_drop, effect_env_none),             # Drop
        (effect_frq_slide, effect_env_none),            # Slide
        (effect_frq_vibrato, effect_env_none)           # Vibrato
        ]

def to_pitch(n):
    return PITCHES[n % 12]


def to_chromatic(p, o):
    return PITCHES.index(p) + 12 * o


def to_freq(n):
    return 65.41 * 2**(n / 12)


def to_pentascale(p):
    o = int(p / 12)
    r = to_chromatic(PENTASCALE[0], o)
    d = abs(r - p)
    for pp in PENTASCALE:
        rr = to_chromatic(pp, o)
        dd = abs(rr - p)
        if dd < d:
            d = dd
            r = rr
    return r


def get_sound(n):
    return PYCO.sounds[n]


def set_sound(n, sound):
    PYCO.sounds[n] = sound


def is_playing():
    return hasattr(SYNTH, "playing") and SYNTH.playing


def get_samples_index():
    if not (hasattr(SYNTH, "sample_one_note") and SYNTH.sample_one_note) and is_playing():
        return max(0, SYNTH.samples_curr - SYNTH.samples_pad)
    else:
        return -1


def get_sample_size(s):
    size = len(s)
    for i in range(len(s)):
        if s[-(i + 1)][2] == 0:
            size -= 1
        else:
            break
    return size 


def play_one_note(note, oscillator, volume, effect, speed):
    stop_sound()

    SYNTH.playing = True
    SYNTH.loop = False
   
    SYNTH.sample_one_note = True
    SYNTH.samples_pad = 0
    SYNTH.samples_size = max(SAMPLE_ONE_NOTE_SIZE / speed, SD_PREBUFFER_SIZE)
    SYNTH.samples_curr = 0

    SYNTH.last_note = 0
    SYNTH.last_l = 0

    def callback(outdata, frames, time, status):
        if SYNTH.samples_curr >= SYNTH.samples_size:
            raise sd.CallbackStop()
        outdata[:] = generate_sample(note, oscillator, volume, effect, speed).reshape(-1, 1)
        SYNTH.samples_curr += 1

    def finished_callback():
        SYNTH.playing = False
    
    try:
        SYNTH.channel = sd.OutputStream(
            device = None,
            channels = 1,
            callback = callback,
            finished_callback = finished_callback,
            samplerate = SAMPLING_RATE,
            blocksize = int(speed * TICK * SAMPLING_RATE))
        SYNTH.channel.start()
    except:
        SYNTH.channel = None


def play_sound(n, loop = False, last_sample = True):
    stop_sound()
    if n == -1:
        return

    if type(n) is tuple:
        channels = len(n)
        sample_size = max([get_sample_size(PYCO.sounds[s]) for s in n])
        speed = PYCO.sounds[n[0]][0][4]
    else:
        channels = 1
        sample_size = get_sample_size(PYCO.sounds[n])
        speed = PYCO.sounds[n][0][4]

    SYNTH.playing = True
    SYNTH.loop = loop
    
    SYNTH.sample_one_note = False
    SYNTH.samples_pad = 0 if loop or not last_sample else SD_PREBUFFER_SIZE
    SYNTH.samples_size = sample_size
    SYNTH.samples_curr = 0

    SYNTH.last_note = 0
    SYNTH.last_l = 0

    def callback(outdata, frames, time, status):
        if SYNTH.samples_curr >= SYNTH.samples_size + SYNTH.samples_pad:
            if not SYNTH.loop:
                raise sd.CallbackStop()
            else:
                SYNTH.samples_curr = 0
        if SYNTH.samples_curr >= SYNTH.samples_size:
            outdata.fill(0)
        elif type(n) is tuple:
            outdata[:] = np.average(
                    [generate_channel(m, SYNTH.samples_curr) for m in n],
                    axis = 0).reshape(-1, 1)
        else:
            outdata[:] = generate_channel(n, SYNTH.samples_curr).reshape(-1, 1)
        SYNTH.samples_curr += 1
        
    def finished_callback():
        SYNTH.playing = False

    try:
        SYNTH.channel = sd.OutputStream(
            device = None,
            channels = 1, #channels,
            callback = callback,
            finished_callback = finished_callback,
            samplerate = SAMPLING_RATE,
            blocksize = int(speed * TICK * SAMPLING_RATE))
        SYNTH.channel.start()
    except:
        SYNTH.channel = None


def stop_sound():
    if is_playing():
        SYNTH.playing = False
    if hasattr(SYNTH, "channel") and SYNTH.channel is not None:
        SYNTH.channel.close()
        SYNTH.channel = None


def generate_sample(note, oscillator, volume, effect, speed, on = False, off = False):
    l = speed * TICK
    if volume == 0:
        SYNTH.last_l = l
        y = np.zeros(int(l * SAMPLING_RATE))
    else:
        t = np.linspace(0, 1, int(l * SAMPLING_RATE), False)
        f = to_freq(note)
        s = OSCILLATORS[oscillator]
        w = lambda t : EFFECTS[effect][0](t, to_freq(SYNTH.last_note), f)
        e = EFFECTS[effect][1]
        v = volume / 7
        if not on and not off:
            x = l * t + SYNTH.last_l
            a = effect_env_none
            SYNTH.last_l += l
        elif on and not off:
            x = l * t
            a = effect_env_adsr_on
            SYNTH.last_l = l
        elif not on and off:
            x = l * t + SYNTH.last_l
            a = effect_env_adsr_off
            SYNTH.last_l = l
        else:
            x = l * t
            a = effect_env_adsr
            SYNTH.last_l = l 
        y = v * a(t) * e(t) * s(TWO_PI * w(t) * x)
    SYNTH.last_note = note
    return y


def generate_channel(n, i):
    sound = PYCO.sounds[n]

    note_on = True
    if SYNTH.samples_curr > 0:
        note_prev = sound[i - 1]
        note_curr = sound[i]
        note_on = note_prev != note_curr
        
    note_off = True
    if SYNTH.samples_curr < SYNTH.samples_size - 1:
        note_next = sound[i + 1]
        note_curr = sound[i]
        note_off = note_next != note_curr

    return generate_sample(*sound[i], note_on, note_off)
