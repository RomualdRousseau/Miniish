"""
Functions to deal with buffer operations; insert a block, delete a line, ...

"""

import re

class Buffer:
    def __init__(self, view_size):
        self.state = "NORMAL"
        self.width_in_chars = view_size[0]
        self.height_in_lines = view_size[1]
        self.buf = [""]
        self.buf_pos = 0
        self.cursor = (0, 0)
        self.undo = []
        self.redo = []
        self.repeat = []
        self.paste_full_line = False
        self.command = ""
        self.search = []
        self.search_curr = 0


def fix_zero_buffer(buffer):
    if len(buffer.buf) == 0:
        buffer.buf = [""]
        buffer.buf_pos = 0
        buffer.cursor = (0, 0)


def get_buffer_len(buffer):
    return len(buffer.buf)


def get_buffer_pos(buffer):
    return buffer.buf_pos + buffer.cursor[1]


def get_buffer_line(buffer, i):
    return buffer.buf[buffer.buf_pos + i]


def replace_buffer_all(buffer, search, replacement):
    regex = re.compile(search)
    for i in range(len(buffer.buf)):
        line = buffer.buf[i]
        buffer.buf[i] = regex.sub(replacement, line)
        if buffer.buf[i] != line:
            buffer.undo.append(("=", i, line))


def search_buffer_all(buffer, search):
    regex = re.compile(search)
    buffer.search = []
    buffer.search_curr = 0
    for i in range(len(buffer.buf)):
        matches = regex.finditer(buffer.buf[i])
        for m in matches:
            buffer.search.append((i, m.start(), m.end()))


def insert_block_before_current_line(buffer, block):
    pos = get_buffer_pos(buffer)
    buffer.undo.append(("-", pos, block))
    head, tail = buffer.buf[:pos], buffer.buf[pos:]
    buffer.buf = head + block + tail


def insert_block_after_current_line(buffer, block):
    pos = get_buffer_pos(buffer) + 1
    buffer.undo.append(("-", pos, block))
    head, tail = buffer.buf[:pos], buffer.buf[pos:]
    buffer.buf = head + block + tail


def delete_buffer_current_line(buffer):
    pos = get_buffer_pos(buffer)
    buffer.undo.append(("+", pos, buffer.buf[pos]))
    del buffer.buf[pos]


def set_current_line(buffer, line):
    pos = get_buffer_pos(buffer)
    buffer.undo.append(("=", pos, buffer.buf[pos]))
    buffer.buf[pos] = line


def get_current_line(buffer):
    if get_buffer_pos(buffer) >= len(buffer.buf):
        return None
    else:
        return buffer.buf[get_buffer_pos(buffer)]
