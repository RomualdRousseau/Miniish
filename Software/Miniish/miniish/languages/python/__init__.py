from typing import Any

from miniish.languages.language import Language
from miniish.languages.python import compile, syntax

class Python(Language):
    def get_name(self) -> str:
        return "python"
    
    def compile(self, checkonly: bool = False) -> Any | None:
        return compile.compile(checkonly)
    
    def colorize(self, line: int, pos: tuple[int, int]) -> None:
        syntax.colorize(line, pos)
