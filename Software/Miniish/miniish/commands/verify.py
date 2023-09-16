from miniish.kernel import disk
from miniish.kernel.process import Process
from miniish.kernel.scheduler import exec


class Verify(Process):
    def init(self, args: list[str] = []) -> None:
        sketch = disk.open("sketch")
        if sketch is not None:
            exec(sketch, ["verify"])