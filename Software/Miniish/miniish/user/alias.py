import pyco.sys

from miniish.kernel import disk
from miniish.kernel.scheduler import exec
from miniish.kernel.process import Process


class Alias(Process):
    def __init__(self, path: str, args: list[str] = []) -> None:
        self.path: str = path
        self.args: list[str] = args
        
    def init(self, args: list[str] = []) -> None:
        sketch = disk.open(self.path)
        if sketch is not None:
            exec(sketch, self.args)