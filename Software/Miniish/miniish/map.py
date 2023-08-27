from miniish.widgets import *


class MapEditor:
    """The Map editor."""

    name = "map-editor"

    def __init__(self):
        pass

    #
    # App interface
    #

    def init_ui(self):
        self.sprite_picker = SpritePicker(1, (0, 87), (128, 34))
        self.map_board = MapBoard(2, (0, 8), (128, 69))
        self.map_board.sprite_picker = self.sprite_picker
        pass

    def update(self):
        c = input()
        if c is not None and c == "escape":
            return False
        self.sprite_picker.update()
        self.map_board.update()
        return True

    def draw(self):
        self.sprite_picker.draw()
        self.map_board.draw()

    #
    # Serialization interface
    #

    def load(self, method):
        pass

    def save(self, method):
        pass
