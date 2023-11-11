import pyco
import pyco.sys

from miniish.kernel.process import Process

RUNNING = -1


class SCHEDULER:
    active: list[Process] = []
    paused: list[Process] = []
    next_pid = 0


def start(process: Process) -> None:
    print(f"Scheduler: start {process}")
    SCHEDULER.active.append(assign_next_pid(process))
    pyco.sys.set_callbacks(_init, _update, _draw)
    pyco.sys.run()
    print("Scheduler: shutdown.")


def shutdown() -> None:
    pyco.sys.shutdown()


def assign_next_pid(process: Process) -> Process:
    process.pid = SCHEDULER.next_pid
    SCHEDULER.next_pid += 1
    return process


def fork(process: Process) -> Process:
    if len(SCHEDULER.active) > 0:
        SCHEDULER.active.append(SCHEDULER.active[RUNNING])
    return process


def exec(process: Process, args: list[str] = []) -> None:
    SCHEDULER.active[RUNNING] = assign_next_pid(process)
    pyco.flush()
    SCHEDULER.active[RUNNING].spawn(args)


def exit() -> None:
    if len(SCHEDULER.active) > 0:
        SCHEDULER.active.pop()
        pyco.flush()


def pause() -> None:
    if len(SCHEDULER.active) > 0:
        SCHEDULER.active[RUNNING].status = 'p'
        SCHEDULER.paused.append(SCHEDULER.active[RUNNING])  
        SCHEDULER.active.pop()
        pyco.flush()


def resume() -> Process | None:
    if len(SCHEDULER.paused) == 0:
        return None
    else:
        SCHEDULER.active.append(SCHEDULER.paused.pop())
        SCHEDULER.active[RUNNING].status = 'r'
        pyco.flush()
        return SCHEDULER.active[RUNNING]


def _init() -> None:
    if len(SCHEDULER.active) > 0:
        SCHEDULER.active[RUNNING].init()


def _update() -> None:
    if len(SCHEDULER.active) > 0:
        SCHEDULER.active[RUNNING].update()


def _draw() -> None:
    if len(SCHEDULER.active) > 0:
        SCHEDULER.active[RUNNING].draw()
