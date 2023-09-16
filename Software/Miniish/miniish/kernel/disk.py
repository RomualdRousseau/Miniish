import os

from miniish.commands import COMMANDS
from miniish.kernel.process import Process


def listdir(path: str | None = None) -> list[str]:
    match path:
        case None | "/":
            return ["bin/", "examples/"]
            
        case "bin" | "/bin" | "bin/" | "/bin/":
            return list(map(lambda x: x, COMMANDS.keys()))
        
        case "examples" | "/examples" | "examples/" | "/examples/":
            return os.listdir("examples")
        
        case _:
            return []
            

def open(path: str) -> Process | None:
    p = get_process(path)
    if p is not None:
        return p

    sketch = get_process("sketch")
    if sketch is not None:
        if sketch.load(path):
            return sketch

    return None


def get_process(path: str) -> Process | None:
    return COMMANDS.get(path)
