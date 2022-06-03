"""
Functions to deal with the viewport operations
"""

from .buffer import *
from .subr import *


def get_last_char_pos(buffer):
    line = get_current_line(buffer)
    if line is None:
        return 0
    else:
        return max(0, min(buffer.width_in_chars, len(line)) - 1)


def get_last_line_pos(buffer):
    return min(buffer.height_in_lines, len(buffer.buf) - buffer.buf_pos) - 1


def move_cursor_next_search(buffer):
    if len(buffer.search) > 0:
        location = buffer.search[buffer.search_curr]
        move_cursor_goto(buffer, location)
        buffer.search_curr = (buffer.search_curr + 1) % len(buffer.search)


def move_cursor_goto(buffer, location):
    buffer.buf_pos = max(0, location[0] - int(buffer.height_in_lines / 2))
    buffer.cursor = (location[1], location[0] - buffer.buf_pos)


def move_cursor_start_of_file(buffer):
    buffer.buf_pos = 0
    buffer.cursor = (0, 0)


def move_cursor_end_of_file(buffer):
    buffer.buf_pos = max(0, len(buffer.buf) - buffer.height_in_lines)
    buffer.cursor = (get_last_char_pos(buffer), get_last_line_pos(buffer))


def move_cursor_right(buffer):
    buffer.cursor = (buffer.cursor[0] + 1, buffer.cursor[1])
    keep_cursor_inbounds(buffer)


def move_cursor_left(buffer):
    buffer.cursor = (buffer.cursor[0] - 1, buffer.cursor[1])
    keep_cursor_inbounds(buffer)


def move_cursor_up(buffer):
    if buffer.cursor[1] == 0:
        buffer.buf_pos -= 1
    buffer.cursor = (buffer.cursor[0], buffer.cursor[1] - 1)
    keep_cursor_inbounds(buffer)


def move_cursor_down(buffer):
    if buffer.cursor[1] == buffer.height_in_lines - 1:
        buffer.buf_pos += 1
    buffer.cursor = (buffer.cursor[0], buffer.cursor[1] + 1)
    keep_cursor_inbounds(buffer)


def move_cursor_start_of_line(buffer, auto_indent):
    indent = 0
    if auto_indent:
        line = get_current_line(buffer)
        if line is not None:
            indent = find_start_word_pos(line)
    buffer.cursor = (indent, buffer.cursor[1])


def move_cursor_end_of_line(buffer):
    padding = 1 if buffer.state in ("INSERT", "CHANGE") else 0
    pos = get_last_char_pos(buffer)
    buffer.cursor = ((pos + padding) if pos > 0 else 0, buffer.cursor[1])


def move_cursor_next_word(buffer, spaces):
    line = get_current_line(buffer)
    pos = buffer.cursor[0]
    if line is not None:
        pos = find_next_word_pos(line, pos, spaces)
    buffer.cursor = (pos, buffer.cursor[1])


def move_cursor_previous_word(buffer, spaces):
    line = get_current_line(buffer)
    pos = buffer.cursor[0]
    if line is not None:
        pos = find_previous_word_pos(line, pos, spaces)
    buffer.cursor = (pos, buffer.cursor[1])


def keep_cursor_inbounds(buffer):
    padding = 1 if buffer.state in ("INSERT", "CHANGE") else 0
    buffer.buf_pos = max(0, min(buffer.buf_pos, get_buffer_len(buffer) - 1))
    buffer.cursor = (
            buffer.cursor[0],
            max(0, min(buffer.cursor[1], get_last_line_pos(buffer)))
            )
    buffer.cursor = (
            max(0, min(buffer.cursor[0], get_last_char_pos(buffer) + padding)), 
            buffer.cursor[1]
            )
