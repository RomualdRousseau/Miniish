from miniish.pyco import *
from miniish.widgets import *


class MusicEditor:
    """The Music editor.
    """

    name = "music-editor"

    def __init__(self):
        pass

    #
    # App interface
    #

    def init_ui(self):
        pass

    def update(self):
        c = input()
        if c is not None and c == "escape":
            return False
        return True

    def draw(self):
        print("music", (0, 8))

    #
    # Serialization interface
    #

    def load(self, method):
        pass

    def save(self, method):
        pass
