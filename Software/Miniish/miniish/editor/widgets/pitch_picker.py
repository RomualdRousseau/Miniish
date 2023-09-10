import pyco
import pyco.synth

from miniish.editor import sound
from miniish.constants import COLOR_STAT_FG
from miniish.editor.widgets.widgets import Widget


class PitchPicker(Widget):
    """Widget to draw a pitch."""

    def __init__(self, id_, pos_, size_) -> None:
        Widget.__init__(self, id_, pos_, size_)
        self.cell_size = (self.size[0] / 32, (self.size[1] - 2) / 64)
        self.last_note = None
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
        # Handle mouse input
        if self.inbounds(m):
            (x, y) = (m[0] - self.pos[0], m[1] - self.pos[1])
            i = int(x / w)
            if pyco.mbtn() and self.parent is not None:
                sound = pyco.synth.get_sound(self.parent.sound)
                (_, _, v, e, s) = sound[i]
                p = max(0, 63 - int(y / h))
                if pyco.mmod() & pyco.pg.KMOD_SHIFT:
                    p = pyco.synth.to_pentascale(p)
                wa = self.parent.oscillator
                sound[i] = (p, wa, v if v > 0 else 4, e, s)
                pyco.synth.set_sound(self.parent.sound, sound)
            self.last_note = i
        else:
            self.last_note = None

    def draw(self) -> None:
        (w, h) = self.cell_size
        # Draw background
        pyco.print(":pitch", (2, self.pos[1] - 8), pyco.INDIGO)
        pyco.rectfill(self._expand(self.pos + self.size, 1), pyco.BLACK)
        # Draw graph
        if self.parent is not None:
            sound = pyco.synth.get_sound(self.parent.sound)
            sample = pyco.synth.get_samples_index()
            for i in range(32):
                (p, wa, v, _, _) = sound[i]
                if v > 0:
                    b = self.pos[1] + self.size[1]
                    c = pyco.LIGHT_GRAY if i == sample else pyco.DARK_BLUE
                    pyco.rectfill(
                        (
                            self.pos[0] + i * w + 1,
                            b - int(p * h + 2),
                            2,
                            int(p * h + 2),
                        ),
                        c,
                    )
                    pyco.rectfill(
                        (self.pos[0] + i * w + 1, b - p * h - 2, 2, 2), pyco.RED + wa
                    )
        # Draw status line
        if self.last_note is not None:
            pyco.print("note: %d" % (self.last_note), (0, 122), COLOR_STAT_FG)

    #
    # Privates
    #

    def _expand(self, r, o):
        (x, y, w, h) = r
        return (x - o, y - o, w + o * 2, h + o * 2)
