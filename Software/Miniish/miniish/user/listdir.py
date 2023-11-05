from miniish.kernel import console, virtfs
from miniish.kernel.scheduler import exit
from miniish.kernel.process import Process


class ListDir(Process):
    def init(self, args: list[str] = []) -> None:
        try:
            path = args[1] if len(args) == 2 else "/"
            for file in sorted(virtfs.listdir(path)):
                if not file.startswith('.'):
                    console.print(file)
        except:
            console.print("i/o error: no such file or dir")
        exit()
