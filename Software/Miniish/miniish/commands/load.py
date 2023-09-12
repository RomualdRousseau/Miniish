import pyco.sys

from miniish.kernel import console, disk
from miniish.kernel.process import Process
from miniish.kernel.scheduler import exit

class Load(Process):   
    def init(self, args: list[str] = []) -> None:
        if len(args) != 2:
            console.print("usage: load <filename>")
        else:
            path = args[1]
            sketch = disk.open(path)
            editor = disk.open("editor")
            if sketch is not None and editor is not None:
                editor.load()  # type: ignore
                console.print("loaded")
            else:
                console.print("i/o error: file not found")
        exit()