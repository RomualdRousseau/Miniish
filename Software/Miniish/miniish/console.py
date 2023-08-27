import logging

from miniish.constants import *
from miniish.pyco import *
from miniish.widgets import *


class Console:
    """The Console.
    """

    name = "console"

    def __init__(self):
        self.timer = 0
        self.buffer = ["", ""]
        self.lastcmd = ""
        self.history = []
        self.history_idx = 0

    #
    # App interface
    #

    def init_ui(self):
        cls(COLOR_CONS_BG)
        blit(sys.load_png("miniish-logo"))
        self.print(BANNER) 
        self.print(PROMPT)

    def update(self):
        # Handle inputs
        c = input()
        if c is not None:
            if c == "escape":
                return False
            else:
                self._parse(c)
        # timer for the blinking cursor
        self.timer +=1
        return True

    def draw(self):
        self._partial_cls()
        y = 0
        color(COLOR_CONS_FG)
        # Draw the buffer
        for line in self.buffer:
            print(line, (0, y))
            y += 6
        # Draw the blinking cursor
        if int(self.timer / 8) % 2 == 0:
            cursor_pos = (len(self.buffer[-1]) * 4, y - 6)
            rectfill(cursor_pos + (4, 6))

    def print(self, s):
        def badd(s):
            # Scroll buffer if at the end of the screen
            if len(self.buffer) >= int(128 / 6):
                self._partial_cls()
                del self.buffer[0]
            self.buffer.append(s)
        # Add multi-lines in the buffer 
        for line in self._split_strings(s):
            badd(line)

    def execute(self, s):
        self._exec(s.split(' '))
        self.print(PROMPT)

    #
    # Privates
    #

    def _split_strings(self, s):
        result = []
        for line in s.split('\n'):
            while len(line) > 32:
                result.append(line[:32])
                line = line[32:]
            result.append(line)
        return result

    def _parse(self, c):
        # Very basic editings; backspace and return
        # and basic history
        if c == "return":
            if not self._exec(self.lastcmd.split(' ')):
                self.print("syntax error")
            self.print(PROMPT)
            self.history.append(self.lastcmd)
            self.lastcmd = ""
            self.history_idx = 0
        elif c == "backspace":
            if len(self.lastcmd) > 0:
                self.lastcmd = self.lastcmd[:-1]
                self.buffer[-1] = self.buffer[-1][:-1]
        elif c == "up":
            self.history_idx = max(0, min(self.history_idx + 1, len(self.history)))
            self.lastcmd = self.history[-self.history_idx]
            self.buffer[-1] = PROMPT + self.history[-self.history_idx]
        elif c == "down":
            self.history_idx = max(1, min(self.history_idx - 1, len(self.history) - 1))
            self.lastcmd = self.history[-self.history_idx]
            self.buffer[-1] = PROMPT + self.history[-self.history_idx]
        elif len(c) == 1:
            self.lastcmd += c
            self.buffer[-1] += c

    def _exec(self, args):
        from . import commands
        cmd = commands.__all__.get(args[0])
        if cmd is not None:
            cmd(args, self)
            flush()
            return True
        elif len(args[0]) > 0:
            try:
                result = eval(self.lastcmd)
                if result is not None:
                    self.print(str(result))
                return True
            except Exception as x:
                logging.warning(x)
                return False
        else:
            return True

    def _partial_cls(self):
        y = 0
        color(COLOR_CONS_BG)
        for line in self.buffer:
            if len(line) > 0:
                rectfill((0, y, len(line) * 4 + 8, 6))
            y += 6
