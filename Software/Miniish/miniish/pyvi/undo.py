"""
Functions to deal with undo/redo operations

"""

from .buffer import *


def do_undo(buffer):
    do_replay(buffer, buffer.undo, buffer.redo)


def do_redo(buffer):
    do_replay(buffer, buffer.redo, buffer.undo)


def do_replay(buffer, redo, undo):
    if len(redo) == 0:
        return
    first_run = True
    while len(redo) > 0:
        (op, pos, line_or_block) = redo.pop()
        if op == "*":
            undo.append(("*", 0, None))
            if not first_run:
                break
        elif op == "=":
            undo.append(("=", pos, buffer.buf[pos]))
            buffer.buf[pos] = line_or_block
        elif op == "-":
            undo.append(("+", pos, line_or_block)) 
            if isinstance(line_or_block, str):
                del buffer.buf[pos]
            else:
                del buffer.buf[pos:pos + len(line_or_block)]
        elif op == "+":
            undo.append(("-", pos, line_or_block))
            if isinstance(line_or_block, str):
                buffer.buf = buffer.buf[:pos] + [line_or_block] + buffer.buf[pos:]
            else:
                buffer.buf = buffer.buf[:pos] + line_or_block + buffer.buf[pos:]
        first_run = False
