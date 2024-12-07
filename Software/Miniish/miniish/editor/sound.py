
import pyco
import pyco.sys
import pyco.synth

from miniish.editor.widgets.component import Component
from miniish.editor.widgets.widgets import Button, ButtonGroup, TextSpinner
from miniish.editor.widgets.pitch_picker import PitchPicker
from miniish.editor.widgets.volume_picker import VolumePicker

class SoundEditor(Component):
    """The Sound editor."""

    def __init__(self) -> None:
        self.sound = 0
        self.oscillator = 0

    def init_ui(self) -> None:
        self.sound_up = Button(0, (0, 9), (61, 61), self._switch_sound)
        self.sound_down = Button(1, (21, 9), (62, 62), self._switch_sound)
        self.speed_picker = TextSpinner(-1, (46, 10), (9, 7), 1, 99, self._update_speed)
        self.oscillator_picker = ButtonGroup(
            -1,
            (45, 18),
            [
                Button(0, (1, 0), (60, 59), self._switch_oscillator),
                Button(1, (1, 0), (46, 45), self._switch_oscillator),
                Button(2, (1, 0), (52, 51), self._switch_oscillator),
                Button(3, (1, 0), (48, 47), self._switch_oscillator),
                Button(4, (1, 0), (50, 49), self._switch_oscillator),
                Button(5, (1, 0), (58, 57), self._switch_oscillator),
            ],
            False,
            [0],
        )
        self.pitch_picker = PitchPicker(-1, (0, 28), (128, 64))
        self.pitch_picker.parent = self # type: ignore
        self.volume_picker = VolumePicker(-1, (0, 100), (128, 19))
        self.volume_picker.parent = self # type: ignore

    def update_ui(self) -> None:
        (_, _, _, _, s) = pyco.synth.get_sound(self.sound)[0]
        self.speed_picker.set_value(s)

    def update(self) -> bool:
        # Handle keyboard inputs
        c = pyco.input()
        if c is not None:
            if c == "escape":
                return False
            elif c == " ":
                if not pyco.synth.is_playing():
                    pyco.synth.play_sound(self.sound, False)
                else:
                    pyco.synth.play_sound(-1)
        # Update widgets
        self.sound_down.update()
        self.sound_up.update()
        self.speed_picker.update()
        self.oscillator_picker.update()
        self.volume_picker.update()
        self.pitch_picker.update()
        return True

    def draw(self) -> None:
        pyco.print("spd", (32, 11), pyco.LIGHT_GRAY)
        pyco.print("%02d" % (self.sound), (11, 11), pyco.WHITE)
        self.sound_down.draw()
        self.sound_up.draw()
        self.speed_picker.draw()
        self.oscillator_picker.draw()
        self.volume_picker.draw()
        self.pitch_picker.draw()

    def load(self) -> None:
        self.update_ui()

    #
    # Privates
    #

    def _update_speed(self, b):
        sound = pyco.synth.get_sound(self.sound)
        for i in range(len(sound)):
            (p, wa, v, e, _) = sound[i]
            s = b.get_value()
            sound[i] = (p, wa, v, e, s)
        # synth.set_sound(self.sound, sound)

    def _switch_sound(self, b):
        if b.id == 0:
            self.sound = max(0, self.sound - 1)
        elif b.id == 1:
            self.sound = min(self.sound + 1, 63)
        self.update_ui()

    def _switch_oscillator(self, b):
        self.oscillator = b.id
        if pyco.mmod() & pyco.pg.KMOD_SHIFT:
            sound = pyco.synth.get_sound(self.sound)
            for i in range(len(sound)):
                (p, _, v, e, s) = sound[i]
                wa = self.oscillator
                sound[i] = (p, wa, v, e, s)
