from miniish.kernel import console, virtfs
from miniish.kernel.process import Process
from miniish.kernel.scheduler import exit


class Save(Process):
    def init(self, args: list[str] = []) -> None:
        if len(args) > 2:
            console.print("usage: save <filename>")
        else:
            try:
                if len(args) == 2:
                    path = (
                        args[1] + ".miniish" if ".miniish" not in args[1] else args[1]
                    )
                    if "/" not in path:
                        path = "/sketches/" + path
                else:
                    path = None

                sketch = virtfs.create(path or "/bin/.sketch")
                editor = virtfs.open("/bin/.editor")
                editor.save(path)
                sketch.save(path)
                console.print("saved")
            except:
                console.print("i/o error: no such file or dir")
        exit()
