from miniish.kernel.process import Process
from miniish.kernel.scheduler import exit
from miniish.kernel import console, serial

DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_BAUD_RATE = 19200


class Screen(Process):
    def init(self, args: list[str] = []) -> None:
        port = DEFAULT_PORT
        baudrate = DEFAULT_BAUD_RATE
        if len(args) == 2:
            port = args[1]
        elif len(args) == 3:
            baudrate = int(args[2])

        try:
            serial.open(port, baudrate)
        except:
            console.print("i/o error: could not open port")
            exit()
            
        console.set_filter(str.lower)
        console.print("\\ ", end="")
        

    def update(self) -> None:
        c = console.getchar()
        match c:
            case None:
                for c in serial.read() or "":
                    console.putchar(c)

            case "escape":
                console.set_filter()
                serial.close()
                exit()

            case "return":
                serial.write("\r\n")

            case "backspace":
                serial.write("\x7f")

            case _:
                if len(c) == 1:
                    serial.write(c.upper())
