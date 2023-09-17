from miniish.kernel import console, disk
from miniish.kernel.process import Process
from miniish.kernel.scheduler import exit


class Save(Process):
    def init(self, args: list[str] = []) -> None:
        if len(args) > 2:
            console.print("usage: save <filename>")
        else:
            try:
                if len(args) == 2:
                    path = args[1] + ".miniish" if ".miniish" not in args[1] else args[1]
                    if "sketches/" not in path:
                        path = "/sketches/" + path
                else:
                    path = None
                    
                sketch = disk.open("/bin/sketch")
                editor = disk.open("/bin/editor")
                editor.save()
                sketch.save(disk.get_real_path(path) if path is not None else None)
                console.print("saved")
            except:
                console.print("i/o error: save failed")
        exit()
