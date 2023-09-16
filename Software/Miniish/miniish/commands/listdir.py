from miniish.kernel import console, disk
from miniish.kernel.scheduler import exit
from miniish.kernel.process import Process


class ListDir(Process):
    def init(self, args: list[str] = []) -> None:
        path = args[1] if len(args) == 2 else None
        for file in disk.listdir(path):
            console.print(file)
        exit()
