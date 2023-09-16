import pyco
import pyco.sys

from miniish.kernel.process import Process
from miniish.kernel.scheduler import exit
from miniish.languages import get_current_language


class Sketch(Process):
    def __init__(self) -> None:
        self.last_loaded = None
        self.program = None

    def init(self, args: list[str] = []) -> None:
        verify = len(args) == 1 and args[0] == "verify"
        self.program = get_current_language().compile(verify)
        if self.program is not None:
            self.program._init()
        else:
            exit()

    def update(self) -> None:
        c = pyco.input()
        if c == "escape":
            pyco.music(-1)
            exit()
        elif self.program is not None:
            self.program._update()

    def draw(self) -> None:
        if self.program is not None:
            self.program._draw()

    def load(self, path: str | None = None) -> bool:
        if path is not None and pyco.sys.load_cartdrige(path):
            self.last_loaded = path
            return True
        else:
            return False

    def save(self, path: str | None = None) -> None:
        self.last_loaded = path if path is not None else self.last_loaded
        if self.last_loaded is not None:
            pyco.sys.save_cartdrige(self.last_loaded)
