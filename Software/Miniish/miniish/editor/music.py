from miniish.widgets import *


class MusicEditor:
    """The Music editor."""

    name = "music-editor"

    def __init__(self):
        self.top = 0
        self.pattern_selector = 0
        self.sound_selector = 0
        self.copy_buffer = (0, 0, 0, 0, 1)

    #
    # App interface
    #

    def init_ui(self):
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

    def update(self):
        c = input()
        if c is not None and c == "escape":
            return False
        if c == "down":
            self._move_selector_down()
        elif c == "up":
            self._move_selector_up()
        elif c == " ":
            if not synth.is_playing():
                pattern = sys.get_music()[self.pattern_selector]
                synth.play_sound(tuple([p for p in pattern if p >= 0]), False)
            else:
                synth.play_sound(-1)
        # Update widgets
        self.pattern_up.update()
        self.pattern_down.update()
        for channel_editor in self.channel_editors:
            pattern = sys.get_music()[self.pattern_selector]
            channel_editor.sound = pattern[channel_editor.id]
            channel_editor.note = self.sound_selector
            channel_editor.update(c)
        return True

    def draw(self):
        # Draw pattern selector
        print("pattern", (3, 11), WHITE)
        for i in range(4):
            if self.pattern_selector == self.top + i:
                rectfill((38 + i * 12 - 1, 10, 9, 7), WHITE)
            else:
                rectfill((38 + i * 12 - 1, 10, 9, 7), LIGHT_GRAY)
            print("%02d" % (self.top + i), (38 + i * 12, 11), DARK_GRAY)
        # Draw widgets
        self.pattern_up.draw()
        self.pattern_down.draw()
        for channel_editor in self.channel_editors:
            channel_editor.draw()

    #
    # Serialization interface
    #

    def load(self):
        pass

    def save(self):
        pass

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
