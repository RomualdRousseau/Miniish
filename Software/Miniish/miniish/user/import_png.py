import pyco.sys

from miniish.kernel import console
from miniish.kernel.scheduler import exit
from miniish.kernel.process import Process


class ImportPng(Process):
    def init(self, args: list[str] = []) -> None:
        if len(args) != 2:
            console.print("usage: import [FILE]")
        else:
            try:
                pyco.sys.import_png(args[1])
                console.print("imported")
            except:  # noqa: E722
                console.print("i/o error: file not found")
        exit()
