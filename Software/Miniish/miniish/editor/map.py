import pyco

from miniish.editor.widgets.component import Component
from miniish.editor.widgets.map_board import MapBoard
from miniish.editor.widgets.sprite_picker import SpritePicker


class MapEditor(Component):
    """The Map editor."""

    def __init__(self) -> None:
        pass

    def init_ui(self) -> None:
        self.sprite_picker = SpritePicker(1, (0, 87), (128, 34))
        self.map_board = MapBoard(2, (0, 8), (128, 69))
        self.map_board.sprite_picker = self.sprite_picker

    def update(self) -> bool:
        c = pyco.input()
        if c is not None and c == "escape":
            return False
        self.sprite_picker.update()
        self.map_board.update()
        return True

    def draw(self) -> None:
        self.sprite_picker.draw()
        self.map_board.draw()
