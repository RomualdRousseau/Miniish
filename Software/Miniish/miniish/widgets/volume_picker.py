from pyco import *

from .widgets import *


class VolumePicker(Widget):
    """Widget to draw a pitch."""

    def __init__(self, id_, pos_, size_):
        Widget.__init__(self, id_, pos_, size_)
        self.cell_size = (self.size[0] / 32, (self.size[1] - 2) / 7)
        self.init_ui()

    #
    # Widget interface
    #

    def init_ui(self):
        pass

    def update(self):
        (w, h) = self.cell_size
        m = mxy()
        if self.inbounds(m) and mbtn():
            (x, y) = (m[0] - self.pos[0], m[1] - self.pos[1])
            i = int(x / w)
            sound = synth.get_sound(self.parent.sound)
            (p, wa, _, e, s) = sound[i]
            v = max(0, 7 - int(y / h))
            sound[i] = (p, wa, v, e, s)
            synth.set_sound(self.parent.sound, sound)

    def draw(self):
        (w, h) = self.cell_size

        print(":volume", (2, self.pos[1] - 6), BLUE)
        rectfill(self.pos + self.size, BLACK)

        sound = synth.get_sound(self.parent.sound)
        for i in range(32):
            (_, _, v, _, _) = sound[i]
            b = self.pos[1] + self.size[1]
            rectfill((self.pos[0] + i * w + 1, b - v * h - 2, 3, 2), v + 1)
