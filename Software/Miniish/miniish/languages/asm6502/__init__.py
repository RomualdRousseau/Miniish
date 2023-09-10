from typing import Any

from miniish.languages.language import Language
from miniish.languages.asm6502 import compile, syntax

class Asm6502(Language):
    def get_name(self) -> str:
        return "asm6502"
    
    def compile(self, checkonly: bool = False) -> Any | None:
        return compile.compile(checkonly)
    
    def colorize(self, line: int, pos: tuple[int, int]) -> None:
        syntax.colorize(line, pos)
