from miniish.kernel.init import Init
from miniish.kernel import scheduler, disk, console, serial


if __name__ == "__main__":
    console.init()
    serial.init()
    disk.init()
    scheduler.start(Init())
