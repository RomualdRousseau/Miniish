from miniish.kernel import console
from miniish.kernel.scheduler import exit
from miniish.kernel.process import Process


class Clrscr(Process):
    def init(self, args: list[str] = []) -> None:
        console.clrscr()
        exit()
