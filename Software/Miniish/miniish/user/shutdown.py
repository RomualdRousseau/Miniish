import pyco.sys

from miniish.kernel import console
from miniish.kernel.process import Process
from miniish.kernel.scheduler import shutdown

class Shutdown(Process):
    def init(self, args: list[str] = []) -> None:
        console.print("bye")
        shutdown()
