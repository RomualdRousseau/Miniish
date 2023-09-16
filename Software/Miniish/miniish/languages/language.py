from typing import Any


class Language:
    def get_name(self) -> str:
        return ""
    
    def compile(self, verify: bool = False) -> Any:
        return None
    
    def colorize(self, line: int, pos: tuple[int, int]) -> None:
        pass