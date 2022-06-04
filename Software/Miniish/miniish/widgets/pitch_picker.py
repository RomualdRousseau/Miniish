from miniish.pyco import synth
from miniish.widgets import *


class PitchPicker(Widget):
    """Widget to draw a pitch.
    """

    def __init__(self, id_, pos_, size_):
        Widget.__init__(self, id_, pos_, size_)
        self.cell_size = (self.size[0] / 32, (self.size[1] - 2) / 64)
        self.last_note = None
        self.init_ui()

    #
    # Widget interface
    #

    def init_ui(self):
        pass

    def update(self):
        (w, h) = self.cell_size
        m = mxy()
        # Handle mouse input
        if self.inbounds(m):
            (x, y) = (m[0] - self.pos[0], m[1] - self.pos[1])
            i = int(x / w)
            if mbtn():
                sound = synth.get_sound(self.parent.sound - 1)
                (_, _, v, e, s) = sound[i]
                p = max(0, 63 - int(y / h))
                wa = self.parent.oscillator
                sound[i] = (p, wa, v if v > 0 else 4, e, s)
                synth.set_sound(self.parent.sound - 1, sound)
            self.last_note = i
        else:
            self.last_note = None

    def draw(self):
        (w, h) = self.cell_size
        # Draw background
        print(":pitch", (2, self.pos[1] - 8), INDIGO)
        rectfill(self._expand(self.pos + self.size, 1), BLACK)
        # Draw graph 
        sound = synth.get_sound(self.parent.sound - 1)
        sample = synth.get_samples_index()
        for i in range(32):
            (p, wa, v, _, _) = sound[i]
            if v > 0:
                b = self.pos[1] + self.size[1]
                c = LIGHT_GRAY if i == sample else DARK_BLUE
                rectfill((
                    self.pos[0] + i * w + 1,
                    b - int(p * h + 2),
                    2,
                    int(p * h + 2)), c)
                rectfill((
                    self.pos[0] + i * w + 1,
                    b - p * h - 2,
                    2,
                    2), RED + wa)
        # Draw status line
        if self.last_note is not None:
            print("note: %d"%(self.last_note), (0, 122), COLOR_STAT_FG)

    #
    # Privates
    # 

    def _expand(self, r, o):
        (x, y, w, h) = r
        return (x - o, y - o, w + o * 2, h + o * 2) 
