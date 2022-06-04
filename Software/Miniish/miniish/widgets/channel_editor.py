from miniish.pyco import synth
from miniish.pyco import sys
from miniish.widgets import *

KEYMAP_TO_PITCH={
        "q": "C",
        "2": "C#",
        "w": "D",
        "3": "D#",
        "e": "E",
        "r": "F",
        "5": "F#",
        "t": "G",
        "6": "G#",
        "y": "A",
        "7": "A#",
        "u": "B"
        }

class ChannelEditor(Widget):
    """Widget to edit a channel.
    """

    def __init__(self, id_, pos_, size_):
        Widget.__init__(self, id_, pos_, size_)
        self.top = 0
        self.selector = 0
        self.cursor = 0
        self.init_ui()

    #
    # Widget interface
    #

    def init_ui(self):
        pos = (self.pos[0] + self.size[0] / 2 - 5, self.pos[1] - 9)
        self.enable_button = Button(-1, (pos[0] - 8, pos[1]), (64, 63), self._enable_callback)
        self.enable_button.toggle_mode = True
        self.sound_picker = TextSpinner(-1, pos, (9, 7), 1, 16, self._sound_callback)

    def update_ui(self):
        pattern = sys.get_music()[self.parent.selector]
        if pattern[self.id] == -1:
            self.enable_button.toggle = False
        else:
            self.enable_button.toggle = True
            self.sound_picker.set_value(pattern[self.id] + 1)

    def update(self, c):
        if self.enable_button.toggle and self.inbounds(mxy()) and c is not None:
            pattern = sys.get_music()[self.parent.selector]
            sound = synth.get_sound(pattern[self.id])
            if c == "down":
                self.selector += 1
                if self.selector > 31:
                    self.selector = 31
                if self.selector > self.top + 12:
                    self.top = self.selector - 12
            elif c == "up":
                self.selector -= 1
                if self.selector < 0:
                    self.selector = 0
                if self.selector < self.top:
                    self.top = self.selector
            elif c == "left":
                self.cursor -= 1
                if self.cursor < 0:
                    self.cursor = 0
            elif c == "right":
                self.cursor += 1
                if self.cursor > 4:
                    self.cursor = 4
            elif c == "backspace":
                sound[self.selector] = (0, 0, 0, 0, 0)
            elif c.isnumeric() and self.cursor >= 1:
                (p, wa, v, e, s) = sound[self.selector]
                n = int(c)
                if self.cursor == 1:
                    sound[self.selector] = ((p % 12) + n * 12, wa, v, e, s)
                elif self.cursor == 2:
                    sound[self.selector] = (p, n, v, e, s)
                elif self.cursor == 3:
                    sound[self.selector] = (p, wa, n, e, s)
                elif self.cursor == 4:
                    sound[self.selector] = (p, wa, v, n, s)
            elif KEYMAP_TO_PITCH.get(c, None) != None:
                (p, wa, v, l, e) = sound[self.selector]
                n = synth.to_chromatic(KEYMAP_TO_PITCH[c], int(p / 12))
                v = 4 if v == 0 else v
                sound[self.selector] = (n, wa, v, l, e)
        # Update widgets 
        self.enable_button.update()
        if self.enable_button.toggle:
            self.sound_picker.update()

    def draw(self):
        focus = self.inbounds(mxy())
        pattern = sys.get_music()[self.parent.selector]
        sound = synth.get_sound(pattern[self.id])
        # Draw background
        rectfill(self._expand(self.pos + self.size, 1), BLACK)
        if not self.enable_button.toggle:
            rectfill(self.pos + self.size, COLOR_MAIN_BG)
        else:
            # Draw notes
            for i in range(13):
                if self.top + i > 31:
                    continue
                (p, wa, v, e, _) = sound[self.top + i]
                # Draw selector and cursor
                if focus and self.selector == self.top + i:
                    rectfill((self.pos[0], self.pos[1] + i * 7) + (self.size[0], 7), DARK_BLUE)
                    if self.cursor == 0:
                        rectfill((self.pos[0], self.pos[1] + i * 7) + (9, 7), YELLOW)
                    else:
                        rectfill((self.pos[0] + 5 * (self.cursor - 1) + 8, self.pos[1] + i * 7) + (5, 7), YELLOW)
                # Draw notes info
                if v == 0:
                    print(".", (self.pos[0] + 1, self.pos[1] + i * 7 + 1), DARK_BLUE)
                    print(".", (self.pos[0] + 9, self.pos[1] + i * 7 + 1), DARK_BLUE)
                    print(".", (self.pos[0] + 14, self.pos[1] + i * 7 + 1), DARK_BLUE)
                    print(".", (self.pos[0] + 19, self.pos[1] + i * 7 + 1), DARK_BLUE)
                    print(".", (self.pos[0] + 24, self.pos[1] + i * 7 + 1), DARK_BLUE)
                else:
                    print("%-2s"%synth.to_pitch(p).lower(),
                            (self.pos[0] + 1, self.pos[1] + i * 7 + 1), WHITE)
                    print("%d"%int(p / 12),
                            (self.pos[0] + 9, self.pos[1] + i * 7 + 1), LIGHT_GRAY)
                    print("%d"%wa,
                            (self.pos[0] + 14, self.pos[1] + i * 7 + 1), PINK)
                    print("%d"%v,
                            (self.pos[0] + 19, self.pos[1] + i * 7 + 1), BLUE)
                    print("%d"%e,
                            (self.pos[0] + 24, self.pos[1] + i * 7 + 1), INDIGO)
        # Draw widgets
        self.enable_button.draw()
        if self.enable_button.toggle:
            self.sound_picker.draw();

    #
    # Privates
    # 

    def _enable_callback(self, b):
        pattern = sys.get_music()[self.parent.selector]
        if b.toggle:
            pattern[self.id] = self.sound_picker.get_value() - 1
        else:
            pattern[self.id] = -1

    def _sound_callback(self, b):
        pattern = sys.get_music()[self.parent.selector]
        pattern[self.id] = b.get_value() - 1

    def _expand(self, r, o):
        (x, y, w, h) = r
        return (x - o, y - o, w + o * 2, h + o * 2) 
