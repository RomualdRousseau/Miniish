from miniish.kernel import console, virtfs
from miniish.kernel.scheduler import exit, SCHEDULER
from miniish.kernel.process import Process


class ProcStat(Process):
    def init(self, args: list[str] = []) -> None:
        console.print(f"stat command")
        for p in SCHEDULER.paused:
            console.print(f"p    {p}")
        for p in SCHEDULER.active:
            console.print(f"a    {p}")
        exit()
