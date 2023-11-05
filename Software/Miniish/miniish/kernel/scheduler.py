import pyco
import pyco.sys

from miniish.kernel.process import Process

class SCHEDULER:
    active: list[Process] = []
    paused: list[Process] = []
    curr: Process | None = None


def start(process: Process) -> None:
    print("Scheduler: start " + str(process))
    SCHEDULER.curr = process
    pyco.sys.set_callbacks(_init, _update, _draw)
    pyco.sys.run()
    print("Scheduler: shutdown.")
    

def shutdown() -> None:
    pyco.sys.shutdown()


def fork(process: Process) -> Process:
    if SCHEDULER.curr is not None:
        SCHEDULER.active.append(SCHEDULER.curr)
    return process


def exec(process: Process, args: list[str] = []) -> None:
    print("Scheduler: exec " + str(process))
    SCHEDULER.curr = process
    pyco.flush()
    SCHEDULER.curr.init(args)


def exit() -> None:
    if len(SCHEDULER.active) == 1:
        pyco.sys.shutdown()
    else:
        print("Scheduler: exit " + str(SCHEDULER.curr))
        SCHEDULER.curr = SCHEDULER.active.pop()
        pyco.flush()


def pause() -> None:
    if SCHEDULER.curr is not None:
        SCHEDULER.paused.append(SCHEDULER.curr)
    SCHEDULER.curr = SCHEDULER.active.pop()
    pyco.flush()


def resume() -> Process | None:
    if SCHEDULER.curr is not None:
        SCHEDULER.active.append(SCHEDULER.curr)
    if len(SCHEDULER.paused) == 0:
        return None
    SCHEDULER.curr = SCHEDULER.paused.pop()
    pyco.flush()
    return SCHEDULER.curr


def _init() -> None:
    if SCHEDULER.curr is not None:
        SCHEDULER.curr.init()


def _update() -> None:
    if SCHEDULER.curr is not None:
        SCHEDULER.curr.update()


def _draw() -> None:
    if SCHEDULER.curr is not None:
        SCHEDULER.curr.draw()
