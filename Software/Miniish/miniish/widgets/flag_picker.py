from miniish.widgets import *


class FlagPicker(Widget):
    """Widget to pick a flag for a given sprite
    """

    def __init__(self, id_, pos_, size_):
        Widget.__init__(self, id_, pos_, size_)
        self.sprite_selected = -1
        self.init_ui()
    #
    # Widget interface
    #

    def init_ui(self):
        (x, y) = self.pos
        self.flags = ButtonGroup(-1, (x, y), [
            Button(i, (-2, 0), (14 + i, 13), self._switch_flag) for i in range(8)
            ], True)

    def update(self):
        # The sprite changed
        if self.sprite_selected != self.sprite_picker.selected:
            self.sprite_selected = self.sprite_picker.selected
            for i in range(8):
                self.flags.select(i, fget(self.sprite_selected, i))
        # Update widgets
        self.flags.update()

    def draw(self):
        self.flags.draw()

    #
    # Privates
    #

    def _switch_flag(self, b):
        fset(self.sprite_selected, b.toggle, b.id)
