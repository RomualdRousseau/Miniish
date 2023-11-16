from miniish.kernel import scheduler, console, serial, virtfs
from miniish.kernel.init import Init
from miniish.constants import OS_NAME, OS_VERSION


def boot():
    print(f"Loading {OS_NAME} {OS_VERSION} ...")
    console.init()
    serial.init()
    virtfs.init()
    scheduler.start(Init("init"))
