import pyco.sys

from miniish.kernel import console, disk
from miniish.kernel.process import Process
from miniish.kernel.scheduler import exit

class Load(Process):   
    def init(self, args: list[str] = []) -> None:
        if len(args) != 2:
            console.print("usage: load <filename>")
        else:
            try:
                path = args[1] + ".miniish" if ".miniish" not in args[1] else args[1]
                if not disk.exists(path):
                    path = "/sketches/" + path
                    
                sketch = disk.open(path)
                editor = disk.open("/bin/editor")
                sketch.load(disk.get_real_path(path))
                editor.load()
                console.print("loaded")
            except:
                console.print("i/o error: file not found")
        exit()