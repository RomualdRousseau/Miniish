import pyco

from miniish.constants import COLOR_CONS_BG, COLOR_CONS_FG


class CONSOLE:
    timer: int = 0
    buffer: list[str] = [""]
    state: int = 0


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
        cursor_pos = (len(CONSOLE.buffer[-1]) * 4, y - 6)
        pyco.rectfill(cursor_pos + (4, 6))

    # timer for the blinking cursor
    CONSOLE.timer += 1


def clrscr() -> None:
    print("\x1b[2J\x1b[H", end="")


def getchar() -> str | None:
    return pyco.input()


def putchar(c: str) -> None:
    if CONSOLE.state == 0:
        if c == "\n":
            CONSOLE.state = 0
        elif c == "\r":
            CONSOLE.state = 1
        elif c == "\x1b":
            CONSOLE.state = 2
        elif c == "\x08":
            CONSOLE.buffer[-1] = CONSOLE.buffer[-1][:-1]
        else:
            CONSOLE.buffer[-1] = CONSOLE.buffer[-1] + c
    elif CONSOLE.state == 1:  # end of line
        if c == "\n":
            _print_newline()
        else:
            CONSOLE.buffer[-1] = c
        CONSOLE.state = 0
    elif CONSOLE.state == 2:  # parse ansi escape codes
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
            pyco.rectfill((0, y, 128, 6))
        y += 6


def _print_newline(s: str = "") -> None:
    if len(CONSOLE.buffer) >= int(128 / 6):
        _cls_partial()
        del CONSOLE.buffer[0]
    CONSOLE.buffer.append(s)
