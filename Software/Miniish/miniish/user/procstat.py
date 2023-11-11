from miniish.kernel import console
from miniish.kernel.scheduler import exit, SCHEDULER
from miniish.kernel.process import Process


class ProcStat(Process):
    def init(self, args: list[str] = []) -> None:
        console.print(f"pid stat cmd")
        for p in SCHEDULER.paused + SCHEDULER.active:
            console.print(f"{p.pid: 3} {p.status: <4} {p.name}")
        exit()
