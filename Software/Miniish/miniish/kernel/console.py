from typing import Callable

import pyco

from miniish.constants import COLOR_CONS_BG, COLOR_CONS_FG

NO_FILTER = lambda x: x


class CONSOLE:
    timer: int = 0
    buffer: list[str] = [""]
    state: int = 0
    filter: Callable[[str], str] = NO_FILTER


def set_filter(filter: Callable[[str], str] = NO_FILTER):
    CONSOLE.filter = filter


def render() -> None:
    _cls_partial()

    # Draw the buffer
    pyco.color(COLOR_CONS_FG)
    y = 0
    for line in CONSOLE.buffer:
        pyco.print(line, (0, y))
        y += 6

    # Draw the blinking cursor
    if int(CONSOLE.timer / 8) % 2 == 0:
        pyco.color(COLOR_CONS_FG)
    else:
        pyco.color(COLOR_CONS_BG)
    cursor_pos = (len(CONSOLE.buffer[-1]) * 4, y - 6)
    pyco.rectfill(cursor_pos + (4, 6))

    # timer for the blinking cursor
    CONSOLE.timer += 1


def clrscr() -> None:
    print("\x1b[2J\x1b[H", end="")


def getchar() -> str | None:
    return pyco.input()


def putchar(c: str) -> None:
    match CONSOLE.state:
        case 0:
            if c == "\n":
                CONSOLE.state = 0
            elif c == "\r": # start new line
                CONSOLE.state = 1
            elif c == "\x1b": # start ansi escape code
                CONSOLE.state = 2
            elif c == "\x08": # backspace
                CONSOLE.buffer[-1] = CONSOLE.buffer[-1][:-1]
            else:
                CONSOLE.buffer[-1] += CONSOLE.filter(c)
                
        case 1: # new line
            if c == "\n":
                _print_newline()
            else:
                CONSOLE.buffer[-1] = CONSOLE.filter(c)
            CONSOLE.state = 0
            
        case 2: # ansi escape codes
            if c == "J":
                pyco.cls()
                CONSOLE.state = 0
            elif c == "H":
                CONSOLE.buffer = [""]
                CONSOLE.state = 0
            elif not (c in ("[", ";") or c.isdigit()):
                CONSOLE.state = 0


def print(s: str = "", end: str = "\n") -> None:
    for c in (s + end).replace("\n", "\r\n"):
        putchar(c)


def _cls_partial() -> None:
    y = 0
    pyco.color(COLOR_CONS_BG)
    for line in CONSOLE.buffer:
        if len(line) > 0:
            pyco.rectfill((0, y, len(line) * 4 + 8, 6))
        y += 6


def _print_newline(s: str = "") -> None:
    if len(CONSOLE.buffer) >= int(128 / 6):
        _cls_partial()
        del CONSOLE.buffer[0]
    CONSOLE.buffer.append(s)
