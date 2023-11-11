from miniish.kernel.init import Init
from miniish.kernel import scheduler, console, serial, virtfs
from miniish.constants import OS_NAME, OS_VERSION

if __name__ == "__main__":
    print(f"Loading {OS_NAME} {OS_VERSION} ...")
    console.init()
    serial.init()
    virtfs.init()
    scheduler.start(Init("init"))
