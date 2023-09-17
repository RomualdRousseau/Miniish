from miniish.kernel import disk
from miniish.kernel.process import Process
from miniish.kernel.scheduler import exec

class Run(Process):
    def init(self, args: list[str] = []) -> None:
        sketch = disk.open("/bin/sketch")
        if sketch is not None:
            exec(sketch, args[1:])