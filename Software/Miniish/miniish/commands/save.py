from miniish.kernel import console, disk
from miniish.kernel.process import Process
from miniish.kernel.scheduler import exit


class Save(Process):
    def init(self, args: list[str] = []) -> None:
        if len(args) > 2:
            console.print("usage: save <filename>")
        else:
            sketch = disk.open("sketch")
            if sketch is not None:
                editor = disk.open("editor")
                path = args[1] if len(args) == 2 else sketch.last_loaded  # type: ignore
                if editor is not None and path is not None:
                    editor.save()  # type: ignore
                    sketch.save(path)  # type: ignore
                    console.print("saved")
                else:
                    console.print("i/o error: save failed")
        exit()
