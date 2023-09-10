import pyco
import pyco.synth

from miniish.editor import sound
from miniish.editor.widgets.widgets import Widget


class VolumePicker(Widget):
    """Widget to draw a pitch."""

    def __init__(self, id_, pos_, size_) -> None:
        Widget.__init__(self, id_, pos_, size_)
        self.cell_size = (self.size[0] / 32, (self.size[1] - 2) / 7)
        self.parent: sound.SoundEditor | None = None
        self.init_ui()

    #
    # Widget interface
    #

    def init_ui(self) -> None:
        pass

    def update(self) -> None:
        (w, h) = self.cell_size
        m = pyco.mxy()
        if self.inbounds(m) and pyco.mbtn() and self.parent is not None:
            (x, y) = (m[0] - self.pos[0], m[1] - self.pos[1])
            i = int(x / w)
            sound = pyco.synth.get_sound(self.parent.sound)
            (p, wa, _, e, s) = sound[i]
            v = max(0, 7 - int(y / h))
            sound[i] = (p, wa, v, e, s)
            pyco.synth.set_sound(self.parent.sound, sound)

    def draw(self) -> None:
        (w, h) = self.cell_size

        pyco.print(":volume", (2, self.pos[1] - 6), pyco.BLUE)
        pyco.rectfill(self.pos + self.size, pyco.BLACK)

        if self.parent is not None:
            sound = pyco.synth.get_sound(self.parent.sound)
            for i in range(32):
                (_, _, v, _, _) = sound[i]
                b = self.pos[1] + self.size[1]
                pyco.rectfill((self.pos[0] + i * w + 1, b - v * h - 2, 3, 2), v + 1)
