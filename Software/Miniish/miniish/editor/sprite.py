from miniish.widgets import *


class SpriteEditor:
    """The sprite editor."""

    name = "sprite-editor"

    def __init__(self):
        pass

    #
    # App interface
    #

    def init_ui(self):
        self.color_picker = ColorPicker(0, (78, 10), (42, 42))
        self.sprite_picker = SpritePicker(1, (0, 87), (128, 34))
        self.flag_picker = FlagPicker(3, (78, 67), (64, 8))
        self.draw_board = DrawBoard(2, (6, 10), (66, 66))
        self.draw_board.color_picker = self.color_picker
        self.draw_board.sprite_picker = self.sprite_picker
        self.flag_picker.sprite_picker = self.sprite_picker

    def update(self):
        c = input()
        if c is not None and c == "escape":
            return False
        self.draw_board.update()
        self.color_picker.update()
        self.sprite_picker.update()
        self.flag_picker.update()
        return True

    def draw(self):
        self.draw_board.draw()
        self.color_picker.draw()
        self.sprite_picker.draw()
        self.flag_picker.draw()

    #
    # Serialization interface
    #

    def load(self):
        pass

    def save(self):
        pass
