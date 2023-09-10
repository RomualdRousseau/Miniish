from miniish.kernel import console, disk
from miniish.kernel.process import Process
from miniish.kernel.scheduler import exit


class Lang(Process):
    def init(self, args: list[str] = []) -> None:
        if len(args) != 2:
            console.print("usage: lang <python | asm6502>")
        else:
            lang = args[1]
            sketch = disk.open("sketch")
            editor = disk.open("editor")
            if sketch is not None and editor is not None and lang is not None:
                sketch.change_language(lang)  # type: ignore
                editor.change_language(lang)  # type: ignore
                console.print("Language: " + lang)
        exit()
