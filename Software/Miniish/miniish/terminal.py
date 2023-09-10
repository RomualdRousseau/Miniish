import logging

from pyco.sys import load_png
from pyco.pyco import blit, cls

from miniish.kernel import console, disk
from miniish.kernel.scheduler import fork, exec, resume
from miniish.kernel.process import Process
from miniish.constants import BANNER, COLOR_CONS_BG, PROMPT


class Terminal(Process):
    """The Terminal."""

    name = "terminal"

    def __init__(self) -> None:
        self.apps_init: bool = False
        self.lastcmd: str = ""
        self.history: list[str] = []
        self.history_idx: int = 0
        self.child_is_running: bool = False

    #
    # Process interface
    #

    def init(self, args: list[str] = []) -> None:
        cls(COLOR_CONS_BG)
        blit(load_png("miniish-logo"))
        console.print(BANNER)
        console.print(PROMPT, end="")

    def update(self) -> None:
        if self.child_is_running:
            console.print(PROMPT, end="")
            self.child_is_running = False
            
        c = console.getchar()
        match c:
            case None:
                return
            
            case "escape":
                process = resume()
                if process is None:
                    editor = disk.open("editor")
                    if editor is not None:
                        exec(fork(editor))
                        
            case "return":
                console.print()
                command = self.lastcmd
                if len(command) > 0:
                    self.history.append(self.lastcmd)
                    self.lastcmd = ""
                    self.history_idx = 0
                    self._execute_command(command.split(" "))
                if not self.child_is_running:
                    console.print(PROMPT, end="")

            case "backspace":
                if len(self.lastcmd) > 0:
                    self.lastcmd = self.lastcmd[:-1]
                    console.putchar("\x08")

            case "up":
                self.history_idx = min(self.history_idx + 1, len(self.history))
                if self.history_idx > 0:
                    self.lastcmd = self.history[-self.history_idx]
                console.print(PROMPT + self.lastcmd, end="")

            case "down":
                self.history_idx = max(self.history_idx - 1, 0)
                if self.history_idx > 0:
                    self.lastcmd = self.history[-self.history_idx]
                else:
                    self.lastcmd = ""
                console.print(PROMPT + self.lastcmd, end="")

            case _:
                if len(c) == 1:
                    self.lastcmd += c
                    console.putchar(c)

    def _execute_command(self, args: list[str]) -> None:  
        process = disk.open(args[0])
        if process is not None:
            exec(fork(process), args)
            self.child_is_running = True
        else:
            try:
                result = eval(" ".join(args))
                if result is not None:
                    console.print(str(result))
            except Exception as x:
                logging.warning(x)
                console.print("syntax error")
