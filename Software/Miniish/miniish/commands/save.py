from miniish.kernel import console, disk
from miniish.kernel.process import Process
from miniish.kernel.scheduler import exit


class Save(Process):
    def init(self, args: list[str] = []) -> None:
        if len(args) > 2:
            console.print("usage: save <filename>")
        else:
            path = args[1] if len(args) == 2 else sketch.last_loaded  # type: ignore
            sketch = disk.open("sketch")
            editor = disk.open("editor")
            if sketch is not None and editor is not None and path is not None:
                sketch.save(path)  # type: ignore
                editor.save()  # type: ignore
                console.print("saved")
            else:
                console.print("Error: could not save")
        exit()
