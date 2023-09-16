from time import sleep
from io import StringIO

from miniish.kernel import console, serial

DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_BAUD_RATE = 19200
START_ADDR = 0x0300
BLOCK_DATA = 8
SPEED = 0.005


def upload() -> None:
    with serial.open(DEFAULT_PORT, DEFAULT_BAUD_RATE):
        console.print("uploading", end="")
        
        with open("target/rom.bin", "rb") as reader:
            

            addr = START_ADDR
            state = 0
            while state == 0:
                data = reader.read(BLOCK_DATA)
                if len(data) == 0:
                    state = 1
                else:
                    _send(_emit_code(addr, data))
                    addr += BLOCK_DATA
                console.print(".", end="")
            console.print()

        console.print("done uploading.")

        _send(_emit_run(START_ADDR))


def _emit_code(adrr, data):
    buffer = StringIO()
    buffer.write(_hex(adrr, 4))
    sep = ":"
    for b in data:
        buffer.write(sep)
        buffer.write(_hex(b, 2))
        sep = " "
    buffer.write("\r\n")
    return buffer.getvalue()


def _emit_run(adrr):
    buffer = StringIO()
    buffer.write(_hex(adrr, 4))
    buffer.write("R\r\n")
    return buffer.getvalue()


def _send(code):
    for c in code:
        serial.write(c)
        sleep(SPEED)


def _hex(number, width):
    return hex(number)[2:].upper().rjust(width, "0")
