import serial
import threading

from pyco import *

from miniish.sketch import SKETCH, _update_console, _draw_console


class SCREEN:
    serial = None
    reader_worker = None
    reader_worker_terminated = False
    buffer = [""]


def screen(args, out):
    SCREEN.serial = serial.Serial("/dev/ttyUSB0", 19200, timeout=0)
    SCREEN.reader_worker = threading.Thread(target=screen_reader_worker)
    SCREEN.reader_worker_terminated = False
    SCREEN.reader_worker.start()

    SKETCH.update = screen_update
    SKETCH.draw = screen_draw


def screen_update():
    c = input()
    if c is not None:
        if c == "escape":
            SCREEN.reader_worker_terminated = True
            SCREEN.reader_worker.join()
            SCREEN.serial.close()

            SKETCH.update = _update_console
            SKETCH.draw = _draw_console
            flush()
        elif c == "return":
            SCREEN.serial.write(b"\r\n")
        elif c == "backspace":
            SCREEN.serial.write(b"\x7f")
        else:
            SCREEN.serial.write(bytes(c.upper(), "ascii"))


def screen_draw():
    cls()
    y = 0
    for line in SCREEN.buffer:
        print(line, (0, y))
        y = y + 6


def screen_reader_worker():
    state = 0
    while not SCREEN.reader_worker_terminated:
        b = SCREEN.serial.read()
        if len(b) > 0 and b[0] < 128:
            c = b.decode("ascii")
            if state == 0:
                if c == "\n":
                    state = 0
                elif c == "\r":
                    state = 1
                elif c == "\x1b":
                    state = 2
                elif c == "\x08":
                    SCREEN.buffer[-1] = SCREEN.buffer[-1][:-1]
                else:
                    SCREEN.buffer[-1] = SCREEN.buffer[-1] + c.lower()
            elif state == 1:  # end of line
                if c == "\n":
                    if len(SCREEN.buffer) >= int(128 / 6):
                        SCREEN.buffer.pop(0)
                    SCREEN.buffer.append("")
                state = 0
            elif state == 2:  # filter ansi escape codes
                if c == "K" or c == "m" or c == "\n":
                    state = 0
