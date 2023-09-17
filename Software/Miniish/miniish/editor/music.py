import pyco
import pyco.sys
import pyco.synth

from miniish.editor.widgets.channel_editor import ChannelEditor
from miniish.editor.widgets.component import Component
from miniish.editor.widgets.widgets import Button


class MusicEditor(Component):
    """The Music editor."""

    def __init__(self) -> None:
        self.top = 0
        self.pattern_selector = 0
        self.sound_selector = 0
        self.copy_buffer = (0, 0, 0, 0, 1)

    def init_ui(self) -> None:
        self.pattern_up = Button(0, (28, 9), (61, 61), self._switch_pattern)
        self.pattern_down = Button(1, (83, 9), (62, 62), self._switch_pattern)
        self.channel_editors = [
            ChannelEditor(0, (2, 27), (28, 91)),
            ChannelEditor(1, (34, 27), (28, 91)),
            ChannelEditor(2, (66, 27), (28, 91)),
            ChannelEditor(3, (98, 27), (28, 91)),
        ]
        for channel_editor in self.channel_editors:
            channel_editor.parent = self

    def update(self) -> bool:
        c = pyco.input()
        if c is not None and c == "escape":
            return False
        if c == "down":
            self._move_selector_down()
        elif c == "up":
            self._move_selector_up()
        elif c == " ":
            if not pyco.synth.is_playing():
                pattern = pyco.sys.get_music()[self.pattern_selector]
                pyco.synth.play_sound(tuple([p for p in pattern if p >= 0]), False)
            else:
                pyco.synth.play_sound(-1)
        # Update widgets
        self.pattern_up.update()
        self.pattern_down.update()
        for channel_editor in self.channel_editors:
            pattern = pyco.sys.get_music()[self.pattern_selector]
            channel_editor.sound = pattern[channel_editor.id]
            channel_editor.note = self.sound_selector
            channel_editor.update(c)
        return True

    def draw(self) -> None:
        # Draw pattern selector
        pyco.print("pattern", (3, 11), pyco.WHITE)
        for i in range(4):
            if self.pattern_selector == self.top + i:
                pyco.rectfill((38 + i * 12 - 1, 10, 9, 7), pyco.WHITE)
            else:
                pyco.rectfill((38 + i * 12 - 1, 10, 9, 7), pyco.LIGHT_GRAY)
            pyco.print("%02d" % (self.top + i), (38 + i * 12, 11), pyco.DARK_GRAY)
        # Draw widgets
        self.pattern_up.draw()
        self.pattern_down.draw()
        for channel_editor in self.channel_editors:
            channel_editor.draw()

    #
    # Privates
    #

    def _switch_pattern(self, b):
        if b.id == 0:
            self.pattern_selector -= 1
            if self.pattern_selector < 0:
                self.pattern_selector = 0
            if self.pattern_selector < self.top:
                self.top = self.pattern_selector
        elif b.id == 1:
            self.pattern_selector += 1
            if self.pattern_selector > 63:
                self.pattern_selector = 63
            if self.pattern_selector > self.top + 3:
                self.top = self.pattern_selector - 3

    def _move_selector_down(self):
        self.sound_selector += 1
        if self.sound_selector > 31:
            self.sound_selector = 31

    def _move_selector_up(self):
        self.sound_selector -= 1
        if self.sound_selector < 0:
            self.sound_selector = 0
