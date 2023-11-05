from typing import Any
from importlib import reload

from miniish.languages.language import Language
from miniish.languages.python import compile, syntax

class Python(Language):
    def get_name(self) -> str:
        return "python"
    
    def compile(self, verify: bool = False) -> Any:
        compile.compile(verify)
        if verify:
            return None
        from target import program  # type: ignore
        program = reload(program)  # type: ignore
        return program
    
    def colorize(self, line: str, pos: tuple[int, int]) -> None:
        syntax.colorize(line, pos)
