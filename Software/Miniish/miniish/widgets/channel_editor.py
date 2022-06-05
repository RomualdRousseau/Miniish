from miniish.pyco import synth
from miniish.pyco import sys
from miniish.widgets import *

KEYMAP_TO_PITCH_SCALE1={
        "z": "C",
        "s": "C#",
        "x": "D",
        "d": "D#",
        "c": "E",
        "v": "F",
        "g": "F#",
        "b": "G",
        "h": "G#",
        "n": "A",
        "j": "A#",
        "m": "B"
        }

KEYMAP_TO_PITCH_SCALE2={
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
        self.sound = -1
        self.note = 0
        self.cursor = 0
        self.top = 0
        self.last_volume = 4
        self.last_oscillator = 0
        self.last_octave = 2
        self.select_start = -1
        self.select_end = -1
        self.init_ui()

    #
    # Widget interface
    #

    def init_ui(self):
        pos = (self.pos[0] + self.size[0] / 2 - 5, self.pos[1] - 9)
        self.enable_button = Button(-1, (pos[0] - 8, pos[1]), (64, 63), self._enable_callback)
        self.enable_button.toggle_mode = True
        self.sound_picker = TextSpinner(-1, pos, (9, 7), 0, 63, self._sound_callback)

    def update(self, c):
        focus = self.inbounds(mxy())
        enable = self.enable_button.toggle
        # Update widgets 
        self.enable_button.update()
        if enable:
            self.sound_picker.update()
        # Update interfaces
        if self.sound == -1:
            self.enable_button.toggle = False
        else:
            self.enable_button.toggle = True
            self.sound_picker.set_value(self.sound)
        # Edit notes 
        if focus and enable and c is not None:
            sound = synth.get_sound(self.sound)
            if c == "left":
                self._move_cursor_left()                
                self.select_start = -1
                self.select_end = -1
            elif c == "right":
                self._move_cursor_right()
                self.select_start = -1
                self.select_end = -1
            elif c == "up" or c == "down":
                self.select_start = -1
                self.select_end = -1
            elif c == "shift-down":
                if self.select_start == -1:
                    self.select_start = self.note
                    self.select_end = self.note
                else:
                    self.select_end += 1
            elif c == "shift-up":
                if self.select_start == -1:
                    self.select_start = self.note
                    self.select_end = self.note
                else:
                    self.select_end -= 1
            elif c == "delete":
                if self.select_start == -1:
                    (p, wa, v, e, s) = sound[self.note]
                    sound[self.note] = (0, 0, 0, 0, s)
                else:
                    for i in range(self.select_start, self.select_end + 1):
                        (p, wa, v, e, s) = sound[i]
                        sound[i] = (0, 0, 0, 0, s)
                self.select_start = -1
                self.select_end = -1
            elif c == "control-x":
                if self.select_start == -1:
                    self.parent.copy_buffer = [sound[self.note]]
                    (p, wa, v, e, s) = sound[self.note]
                    sound[self.note] = (0, 0, 0, 0, s)
                else:
                    self.parent.copy_buffer = [sound[i] for i in range(self.select_start, self.select_end + 1)]
                    for i in range(self.select_start, self.select_end + 1):
                        (p, wa, v, e, s) = sound[i]
                        sound[i] = (0, 0, 0, 0, s)
                self.select_start = -1
                self.select_end = -1
            elif c == "control-c":
                if self.select_start == -1:
                    self.parent.copy_buffer = [sound[self.note]]
                else:
                    self.parent.copy_buffer = [sound[i] for i in range(self.select_start, self.select_end + 1)]
                self.select_start = -1
                self.select_end = -1
            elif c == "control-v":
                for i, note in enumerate(self.parent.copy_buffer):
                    sound[self.note + i] = note
                self.select_start = -1
                self.select_end = -1
            else:
                (p, wa, v, e, s) = sound[self.note]
                if c.isnumeric() and self.cursor >= 1:
                    n = int(c)
                    if self.cursor == 1:
                        p = (p % 12) + n * 12
                        self.last_octave = n
                    elif self.cursor == 2:
                        wa = min(n, 6)
                        self.last_oscillator = wa
                    elif self.cursor == 3:
                        v = min(n, 7)
                        self.last_volume = v
                    elif self.cursor == 4:
                        e = min(n, 5)
                    sound[self.note] = (p, wa, v, e, s)
                    synth.play_one_note(*sound[self.note])
                elif KEYMAP_TO_PITCH_SCALE1.get(c, None) != None:
                    p = synth.to_chromatic(KEYMAP_TO_PITCH_SCALE1[c], max(0, self.last_octave - 1))
                    if v == 0:
                        wa = self.last_oscillator
                        v = self.last_volume
                    sound[self.note] = (p, wa, v, e, s)
                    synth.play_one_note(*sound[self.note])
                    self.parent._move_selector_down()
                elif KEYMAP_TO_PITCH_SCALE2.get(c, None) != None:
                    p = synth.to_chromatic(KEYMAP_TO_PITCH_SCALE2[c], self.last_octave)
                    if v == 0:
                        wa = self.last_oscillator
                        v = self.last_volume
                    sound[self.note] = (p, wa, v, e, s)
                    synth.play_one_note(*sound[self.note])
                    self.parent._move_selector_down()
                self.select_start = -1
                self.select_end = -1

    def draw(self):
        focus = self.inbounds(mxy())
        enable = self.enable_button.toggle
        # Draw background
        rectfill(self._expand(self.pos + self.size, 1), BLACK)
        # Draw widgets 
        self.enable_button.draw()
        if enable:
            self.sound_picker.draw();
        # Draw partition
        if not enable:
            rectfill(self.pos + self.size, COLOR_MAIN_BG)
        else:
            sound = synth.get_sound(self.sound)
            sample = synth.get_samples_index()
            top = self._get_top() if sample < 0 else (sample - 12 if sample > 12 else 0)
            if self.select_end > 0 and self.select_end > top + 12:
                top = self.select_end - 12
            # Draw notes
            for i in range(min(32 - top, 13)):
                (p, wa, v, e, _) = sound[top + i]
                # Draw selector
                if self.note == top + i:
                    rectfill((self.pos[0], self.pos[1] + i * 7) + (self.size[0], 7), DARK_BLUE)
                # Draw cursor
                if focus and self.parent.sound_selector == top + i:
                    if self.cursor == 0:
                        rectfill((self.pos[0], self.pos[1] + i * 7) + (9, 7), YELLOW)
                    else:
                        rectfill((self.pos[0] + 5 * (self.cursor - 1) + 8, self.pos[1] + i * 7) + (5, 7), YELLOW)
                # Draw playing bar
                if sample >= 0 and sample == top + i:
                    rectfill((self.pos[0], self.pos[1] + i * 7) + (self.size[0], 7), YELLOW)
                if self.select_start <= top + i and top + i <= self.select_end:
                    rectfill((self.pos[0], self.pos[1] + i * 7) + (self.size[0], 7), YELLOW)
                # Draw notes info
                if v == 0:
                    print(".", (self.pos[0] + 1, self.pos[1] + i * 7 + 1), DARK_BLUE)
                    print(".", (self.pos[0] + 9, self.pos[1] + i * 7 + 1), DARK_BLUE)
                    print(".", (self.pos[0] + 14, self.pos[1] + i * 7 + 1), DARK_BLUE)
                    print(".", (self.pos[0] + 19, self.pos[1] + i * 7 + 1), DARK_BLUE)
                    print(".", (self.pos[0] + 24, self.pos[1] + i * 7 + 1), DARK_BLUE)
                else:
                    print("%-2s"%synth.to_pitch(p).lower(), (self.pos[0] + 1, self.pos[1] + i * 7 + 1), WHITE)
                    print("%d"%int(p / 12), (self.pos[0] + 9, self.pos[1] + i * 7 + 1), LIGHT_GRAY)
                    print("%d"%wa, (self.pos[0] + 14, self.pos[1] + i * 7 + 1), PINK)
                    print("%d"%v, (self.pos[0] + 19, self.pos[1] + i * 7 + 1), BLUE)
                    print("%d"%e, (self.pos[0] + 24, self.pos[1] + i * 7 + 1), INDIGO)

    #
    # Privates
    # 

    def _enable_callback(self, b):
        pattern = sys.get_music()[self.parent.pattern_selector]
        if b.toggle:
            pattern[self.id] = self.sound_picker.get_value()
        else:
            pattern[self.id] = -1

    def _sound_callback(self, b):
        pattern = sys.get_music()[self.parent.pattern_selector]
        pattern[self.id] = b.get_value()

    def _expand(self, r, o):
        (x, y, w, h) = r
        return (x - o, y - o, w + o * 2, h + o * 2)

    def _get_top(self):
        if self.parent.sound_selector > self.top + 12:
            self.top = self.parent.sound_selector - 12
        if self.parent.sound_selector < self.top:
            self.top = self.parent.sound_selector
        return self.top
    
    def _move_cursor_left(self):
        self.cursor -= 1
        if self.cursor < 0:
            self.cursor = 0

    def _move_cursor_right(self):
        self.cursor += 1
        if self.cursor > 4:
            self.cursor = 4
