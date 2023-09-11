from miniish.kernel.process import Process
from miniish.kernel.scheduler import exit
from miniish.kernel import console, serial


class Screen(Process):
    def init(self, args: list[str] = []) -> None:
        serial.open("/dev/ttyUSB0")

    def update(self) -> None:
        c = console.getchar()
        if c is not None:
            if c == "escape":
                serial.close()
                exit()
            elif c == "return":
                serial.write("\r\n")
            elif c == "backspace":
                serial.write("\x7f")
            elif len(c) == 1:
                serial.write(c.upper())

        for c in (serial.read() or ""):
            console.putchar(c.lower())
