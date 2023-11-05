import pyco.sys

from miniish.kernel import virtfs
from miniish.kernel.scheduler import exec
from miniish.kernel.process import Process


class Alias(Process):
    def __init__(self, path: str, args: list[str] = []) -> None:
        self.path: str = path
        self.args: list[str] = args
        
    def init(self, args: list[str] = []) -> None:
        sketch = virtfs.open(self.path)
        if sketch is not None:
            exec(sketch, self.args)