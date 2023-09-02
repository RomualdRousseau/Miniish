import logging

from miniish.constants import *
from miniish.widgets import *

class Console:
    """The Console."""

    name = "console"

    def __init__(self):
        self.timer = 0
        self.buffer = ["", "", ""]
        self.lastcmd = ""
        self.history = []
        self.history_idx = 0
        self.state = 0
        self.prompt_enabled = True

    #
    # App interface
    #

    def init_ui(self):
        cls(COLOR_CONS_BG)
        blit(sys.load_png("miniish-logo"))
        self.print(BANNER)
        self.print(PROMPT, end="")
        
    def update(self):
        c = self.getchar()
        if c is not None:
            if c == "escape":
                return False
            else:
                self._parse(c)
        return True

    def draw(self):
        self._partial_cls()
        
        # Draw the buffer
        color(COLOR_CONS_FG)
        y = 0
        for line in self.buffer:
            print(line, (0, y))
            y += 6
            
        # Draw the blinking cursor
        if int(self.timer / 8) % 2 == 0:
            cursor_pos = (len(self.buffer[-1]) * 4, y - 6)
            rectfill(cursor_pos + (4, 6))
        
        # timer for the blinking cursor
        self.timer += 1

    def enable_prompt(self):
        self.prompt_enabled = True
        self.print()
        self.print(PROMPT, end="")
        
    def disable_prompt(self):
        self.prompt_enabled = False

    def clrscr(self):
        self.print("\x1b[2J\x1b[H", end="")
        
    def getchar(self):
        return input()
    
    def putchar(self, c):
        if self.state == 0:
            if c == "\n":
                self.state = 0
            elif c == "\r":
                self.state = 1
            elif c == "\x1b":
                self.state = 2
            elif c == "\x08":
                self.buffer[-1] = self.buffer[-1][:-1]
            else:
                self.buffer[-1] = self.buffer[-1] + c.lower()
        elif self.state == 1:  # end of line
            if c == "\n":
                self._newline()
            self.state = 0
        elif self.state == 2:  # parse ansi escape codes
            if c == "J":
                cls()
                self.state = 0
            elif c == "H":
                self.buffer = [""]
                self.state = 0
            elif not (c in ("[", ";") or c.isdigit()):
                self.state = 0
                
    def print(self, s="", end="\n"):
        for c in (s + end).replace("\n", "\r\n"):
            self.putchar(c)
          
    def execute(self, s):
        self._exec(s.split(" "))
        if self.prompt_enabled:
            self.print(PROMPT, end="")
        
    #
    # Privates
    #

    def _parse(self, c):
        # Very basic editings; backspace and return
        # and basic history
        if c == "return":
            self.print()
            if not self._exec(self.lastcmd.split(" ")):
                self.print("syntax error")
            if self.prompt_enabled:
                self.print(PROMPT, end="")
            self.history.append(self.lastcmd)
            self.lastcmd = ""
            self.history_idx = 0
        elif c == "backspace":
            if len(self.lastcmd) > 0:
                self.lastcmd = self.lastcmd[:-1]
                self.buffer[-1] = self.buffer[-1][:-1]
        elif c == "up":
            self.history_idx = max(0, min(self.history_idx + 1, len(self.history)))
            if self.history_idx > 0:
                self.lastcmd = self.history[-self.history_idx]
                self.buffer[-1] = PROMPT + self.history[-self.history_idx]
        elif c == "down":
            self.history_idx = max(1, min(self.history_idx - 1, len(self.history) - 1))
            if self.history_idx > 1:
                self.lastcmd = self.history[-self.history_idx]
                self.buffer[-1] = PROMPT + self.history[-self.history_idx]
        elif len(c) == 1:
            self.lastcmd += c
            self.buffer[-1] += c

    def _exec(self, args):
        import miniish.commands
        cmd = miniish.commands.COMMANDS.get(args[0])
        if cmd is not None:
            cmd(args, self, self)
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
                rectfill((0, y, 128, 6))
            y += 6
            
    def _newline(self, s=""):
        if len(self.buffer) >= int(128 / 6):
            self._partial_cls()
            del self.buffer[0]
        self.buffer.append(s)
