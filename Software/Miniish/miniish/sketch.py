import pyco
import pyco.sys

from miniish.kernel import disk
from miniish.kernel.process import Process
from miniish.kernel.scheduler import exit
from miniish.constants import DEFAULT_LANGUAGE
from miniish.languages import LANGUAGES


class Sketch(Process):
    def __init__(self) -> None:
        self.language = LANGUAGES[DEFAULT_LANGUAGE]
        self.last_loaded = None
        self.program = None

    def init(self, args: list[str] = []) -> None:
        self.program = self.language.compile()
        if self.program is not None:
            self.program._init()

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
            
    def load(self, path: str) -> bool:
        if pyco.sys.load_cartdrige(path):
            self.last_loaded = path
            return True
        else:
            return False

    def save(self, path: str) -> None:
        self.last_loaded = path
        pyco.sys.save_cartdrige(self.last_loaded)
        
    def change_language(self, lang: str) -> None:
        self.language = LANGUAGES.get(lang) or LANGUAGES[DEFAULT_LANGUAGE]