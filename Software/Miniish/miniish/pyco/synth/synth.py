from .locals import *
from .oscillators import *
from .envelopes import *
from .modulators import *

import sounddevice as sd

OSCILLATORS = [
        triangle,
        ramp,
        sawtooth,
        square,
        noise,
        sin
        ]

EFFECTS = [
        (effect_frq_none, effect_env_none),             # None
        (effect_frq_slide, effect_env_none),            # Slide
        (effect_frq_vibrato, effect_env_none),          # Vibrato
        (effect_frq_drop, effect_env_none),             # Drop
        (effect_frq_none, effect_env_fade_in),          # Fade In
        (effect_frq_none, effect_env_fade_out),         # Fade Out
        (effect_frq_none, effect_env_none),             # Arpegio Fast
        (effect_frq_none, effect_env_none)              # Arpegio Slow
        ]


def to_pitch(n):
    return PITCHES[n % 12]


def to_chromatic(p, o):
    return PITCHES.index(p) + 12 * o


def to_freq(n):
    return 65.41 * 2**(n / 12)


def generate_sample(note, oscillator, volume, effect, speed, on, off):
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
            x = l * t
            a = effect_env_adsr_off
            SYNTH.last_l = l
        else:
            x = l * t
            a = effect_env_adsr
            SYNTH.last_l = l 
        y = v * a(t) * e(t) * s(TWO_PI * w(t) * x)
    SYNTH.last_note = note
    return y.reshape(-1, 1)


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


def get_sound(n):
    return PYCO.sounds[n]


def set_sound(n, sound):
    PYCO.sounds[n] = sound


def play_one_note(note, oscillator, volume, effect, speed):
    if is_playing():
        SYNTH.playing = False
        if SYNTH.channel is not None:
            SYNTH.channel.close()
            SYNTH.channel = None

    SYNTH.playing = True
    SYNTH.loop = False
   
    SYNTH.sample_one_note = True
    SYNTH.samples_size = max(SAMPLE_ONE_NOTE_SIZE / speed, 1)
    SYNTH.samples_curr = 0

    SYNTH.last_note = 0
    SYNTH.last_l = 0

    def callback(outdata, frames, time, status):
        outdata[:] = generate_sample(note, oscillator, volume, effect, speed, False, False) 

        SYNTH.samples_curr += 1
        if SYNTH.samples_curr >= SYNTH.samples_size:
            SYNTH.samples_curr = 0
            SYNTH.playing = False
            raise sd.CallbackStop()

    try:
        SYNTH.channel = sd.OutputStream(
            device = None,
            channels = 1,
            callback = callback,
            samplerate = SAMPLING_RATE,
            blocksize = int(speed * TICK * SAMPLING_RATE))
        SYNTH.channel.start()
    except:
        SYNTH.channel = None


def play_sound(n, loop = False):
    if is_playing():
        SYNTH.playing = False
        if SYNTH.channel is not None:
            SYNTH.channel.close()
            SYNTH.channel = None
        if n == -1:
            return

    first = n[0] if type(n) is tuple else n
    len_n = len(n) if type(n) is tuple else 1
    speed = PYCO.sounds[first][0][4]
    
    SYNTH.playing = True
    SYNTH.loop = loop
    
    SYNTH.sample_one_note = False
    SYNTH.samples_size = len(PYCO.sounds[first])
    SYNTH.samples_curr = 0

    SYNTH.last_note = 0
    SYNTH.last_l = 0

    def callback(outdata, frames, time, status):
        if type(n) is tuple:
            channels = []
            for m in n:
                channels.append(generate_channel(m, SYNTH.samples_curr))
            outdata[:] = np.array(channels).reshape(-1, len_n)
        else:
            outdata[:] = generate_channel(n, SYNTH.samples_curr) 
        
        SYNTH.samples_curr += 1
        if SYNTH.samples_curr >= SYNTH.samples_size:
            SYNTH.samples_curr = 0
            if not SYNTH.loop:
                SYNTH.playing = False
                raise sd.CallbackStop()

    try:
        SYNTH.channel = sd.OutputStream(
            device = None,
            channels = len_n,
            callback = callback,
            samplerate = SAMPLING_RATE,
            blocksize = int(speed * TICK * SAMPLING_RATE))
        SYNTH.channel.start()
    except:
        SYNTH.channel = None


def stop_sound():
    if is_playing():
        SYNTH.playing = False
        if SYNTH.channel is not None:
            SYNTH.channel.close()
            SYNTH.channel = None


def get_samples_index():
    return SYNTH.samples_curr if not (hasattr(SYNTH, "sample_one_note") and SYNTH.sample_one_note) and is_playing() else -1


def is_playing():
    return hasattr(SYNTH, "playing") and SYNTH.playing
