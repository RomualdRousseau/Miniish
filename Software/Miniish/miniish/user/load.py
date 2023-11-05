from miniish.kernel import console, virtfs
from miniish.kernel.process import Process
from miniish.kernel.scheduler import exit


class Load(Process):
    def init(self, args: list[str] = []) -> None:
        if len(args) != 2:
            console.print("usage: load <filename>")
        else:
            try:
                path = args[1] + ".miniish" if ".miniish" not in args[1] else args[1]
                if not virtfs.exists(path):
                    path = "/sketches/" + path

                sketch = virtfs.open(path)
                editor = virtfs.open("/bin/.editor")
                sketch.load(path)
                editor.load(path)
                console.print("loaded")
            except:
                console.print("i/o error: no such file or dir")
        exit()
