from typing import Any


class Language:
    def get_name(self) -> str:
        return ""
    
    def compile(self, checkonly: bool = False) -> Any | None:
        return None
    
    def colorize(self, line: int, pos: tuple[int, int]) -> None:
        pass