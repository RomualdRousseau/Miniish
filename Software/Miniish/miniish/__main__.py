from miniish.terminal import Terminal
from miniish.kernel import scheduler, disk, console, serial


if __name__ == "__main__":
    disk.start()
    console.start()
    serial.start()
    scheduler.start(Terminal())
