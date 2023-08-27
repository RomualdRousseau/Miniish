from pyco import *

from .widgets import *


class ColorPicker(Widget):
    """Widget to pick a color from PYCO palette."""

    def __init__(self, id_, pos_, size_):
        Widget.__init__(self, id_, pos_, size_)
        self.cell_size = (int((size_[0] - 2) / 4), int((size_[1] - 2) / 4))
        self.selected = 0
        self.init_ui()

    #
    # Widget interface
    #

    def init_ui(self):
        pass

    def update(self):
        # Select a new color
        (mx, my) = mxy()
        if self.inbounds((mx, my)) and mbtn():
            (x, y), (w, h) = self.pos, self.cell_size
            pos = (int((mx - x - 1) / w), int((my - y - 1) / h))
            self.selected = pos[1] * 4 + pos[0]

    def draw(self):
        (x, y), (w, h) = self.pos, self.cell_size
        # Draw the background
        rectfill(self.pos + self.size, BLACK)
        # Draw the palette
        for i in range(4):
            for j in range(4):
                pos = (x + j * w + 1, y + i * h + 1)
                rectfill(pos + (w, h), i * 4 + j)
        # Draw the selector
        pos = (x + int(self.selected % 4) * w, y + int(self.selected / 4) * h)
        rect(pos + (w + 2, h + 2), WHITE)
