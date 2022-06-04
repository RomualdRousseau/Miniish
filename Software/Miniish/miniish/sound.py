from miniish.pyco import *
from miniish.pyco import synth
from miniish.widgets import *

class SoundEditor:
    """The SIund editor.
    """

    name = "sound-editor"

    def __init__(self):
        self.sound = 1
        self.oscillator = 0
        
    #
    # App interface
    #

    def init_ui(self):
        self.sound_up = Button(0, (0, 9), (61, 61), self._switch_sound)
        self.sound_down = Button(1, (21, 9), (62, 62), self._switch_sound)
        self.speed_picker = TextSpinner(-1, (46, 10), (11, 7), 1, 16)
        self.oscillator_picker = ButtonGroup(-1, (45, 18), [
            Button(0, (1, 0), (46, 45), self._switch_oscillator),
            Button(1, (1, 0), (48, 47), self._switch_oscillator),
            Button(2, (1, 0), (50, 49), self._switch_oscillator),
            Button(3, (1, 0), (52, 51), self._switch_oscillator),
            Button(4, (1, 0), (58, 57), self._switch_oscillator),
            Button(5, (1, 0), (60, 59), self._switch_oscillator)
            ], False, [0])
        self.pitch_picker = PitchPicker(-1, (0, 28), (128, 64))
        self.pitch_picker.parent = self
        self.volume_picker = VolumePicker(-1, (0, 100), (128, 19))
        self.volume_picker.parent = self

    def update(self):
        # Handle keyboard inputs
        c = input()
        if c is not None:
            if c == "escape":
                return False
            elif c == " ":
                if not synth.is_playing():
                    synth.play_sound(self.sound - 1, False)
                else:
                    synth.play_sound(-1)
        # Update widgets
        self.sound_down.update()
        self.sound_up.update()
        self.speed_picker.update()
        self.oscillator_picker.update()
        self.volume_picker.update()
        self.pitch_picker.update()
        self._update_speed()
        return True

    def draw(self):
        print("spd", (32, 11), LIGHT_GRAY)
        print("%02d"%(self.sound), (11, 11), WHITE)
        self.sound_down.draw()
        self.sound_up.draw()
        self.speed_picker.draw()
        self.oscillator_picker.draw()
        self.volume_picker.draw()
        self.pitch_picker.draw()

    #
    # Serialization interface
    #

    def load(self, method):
        pass

    def save(self, method):
        pass

    #
    # Privates
    #

    def _update_speed(self):
        sound = synth.get_sound(self.sound - 1)
        for i in range(len(sound)):
            (p, wa, v, e, _) = sound[i]
            s = self.speed_picker.get_value()
            sound[i] = (p, wa, v, e, s)
        synth.set_sound(self.sound - 1, sound)

    def _switch_sound(self, b):
        if b.id == 0:
            self.sound = max(1, self.sound - 1)
        elif b.id == 1:
            self.sound = min(self.sound + 1, 64)
        (_, _, _, _, s) = synth.get_sound(self.sound - 1)[0]
        self.speed_picker.set_value(s)

    def _switch_oscillator(self, b):
        self.oscillator = b.id
