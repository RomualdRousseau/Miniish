import pyco.sys

from miniish.kernel import console
from miniish.kernel.scheduler import exit
from miniish.kernel.process import Process


class ExportPng(Process):
    def init(self, args: list[str] = []) -> None:
        if len(args) != 2:
            console.print("usage: export [FILE]")
        else:
            pyco.sys.export_png(args[1])
            console.print("exported")
        exit()
