import logging

import pyco
import pyco.sys

from miniish.kernel import console, virtfs
from miniish.kernel.scheduler import fork, exec, resume, exit
from miniish.kernel.process import Process
from miniish.constants import BANNER, COLOR_CONS_BG, PROMPT


class Shell(Process):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.lastcmd: str = ""
        self.history: list[str] = []
        self.history_idx: int = 0
        self.state: int = 0

    def init(self, args: list[str] = []) -> None:
        pyco.cls(COLOR_CONS_BG)
        console.print(BANNER)
        console.print(PROMPT, end="")

    def update(self) -> None:
        match self.state:
            case 0:
                c = console.getchar()
                if c is not None:
                    self._parse_input(c)

            case 1:  # Command is running
                console.print(PROMPT, end="")
                self.state = 0

            case 2:  # Editor is running
                pyco.blit(self.img)
                self.state = 0

    def _parse_input(self, c: str) -> None:
        match c:
            case "escape":
                self.img = pyco.sys.screenshot()
                self._switch_to_editor()
                self.state = 2

            case "return":
                console.print()
                if len(self.lastcmd) > 0:
                    self.history.append(self.lastcmd)
                    self._exec_command(self.lastcmd.split(" "))
                    self.lastcmd = ""
                    self.history_idx = 0
                self.state = 1

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

    def _switch_to_editor(self) -> None:
        process = resume()
        if process is None:
            process = virtfs.open("/bin/.editor")
            exec(fork(process))

    def _exec_command(self, args: list[str]) -> None:
        if args[0] == "exit":
            exit()
        elif virtfs.exists(args[0]):
            process = virtfs.open(args[0])
            exec(fork(process), args)
        elif virtfs.exists("/bin/" + args[0]):
            process = virtfs.open("/bin/" + args[0])
            exec(fork(process), args)
        else:
            self._exec_python(" ".join(args))

    def _exec_python(self, statement: str) -> None:
        try:
            result = eval(statement)
            if result is not None:
                console.print(str(result))
        except Exception as x:
            logging.warning(x)
            console.print("syntax error")
