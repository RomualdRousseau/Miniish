from miniish.pyco import *
from miniish.widgets import *


class MusicEditor:
    """The Music editor.
    """

    name = "music-editor"

    def __init__(self):
        self.top = 0
        self.selector = 0

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
                ChannelEditor(3, (98, 27), (28, 91))
                ]
        for channel_editor in self.channel_editors:
            channel_editor.parent = self

    def update(self):
        c = input()
        if c is not None and c == "escape":
            return False
        # Update widgets
        self.pattern_up.update()
        self.pattern_down.update()
        for channel_editor in self.channel_editors:
            channel_editor.update(c)
            channel_editor.update_ui()
        return True

    def draw(self):
        print("pattern", (3, 11), WHITE)
        for i in range(4):
            if self.selector == self.top + i:
                rectfill((38 + i * 12 - 1, 10, 9, 7), WHITE)
            else:
                rectfill((38 + i * 12 - 1, 10, 9, 7), LIGHT_GRAY)
            print("%02d"%(self.top + i), (38 + i * 12, 11), DARK_GRAY)
        # Draw widgets
        self.pattern_up.draw()
        self.pattern_down.draw()
        for channel_editor in self.channel_editors:
            channel_editor.draw()

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

    def _switch_pattern(self, b):
        if b.id == 0:
            self.selector -= 1
            if self.selector < 0:
                self.selector = 0
            if self.selector < self.top:
                self.top = self.selector
        elif b.id == 1:
            self.selector += 1
            if self.selector > 63:
                self.selector = 63
            if self.selector > self.top + 3:
                self.top = self.selector - 3
        for channel_editor in self.channel_editors:
            channel_editor.update_ui()
