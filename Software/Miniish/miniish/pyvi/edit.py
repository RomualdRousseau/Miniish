"""
Functions to deal with edit operations

"""

from .buffer import *
from .subr import *


def insert_character(buffer, c):
    pos = buffer.cursor[0]
    line = get_current_line(buffer)
    if line is not None:
        head, tail = line[:pos], line[pos:]
        set_current_line(buffer, head + c + tail)
    return line


def insert_blank_line_before_current_line(buffer):
    indent = ""
    line = get_current_line(buffer)
    if line is not None:
        indent = " " * find_start_word_pos(line) 
    insert_block_before_current_line(buffer, [indent])


def insert_blank_line_after_current_line(buffer, auto_tail):
    pos = buffer.cursor[0]
    prefix = ""
    line = get_current_line(buffer)
    if line is not None:
        prefix = " " * find_start_word_pos(line) 
        if auto_tail:
            head, tail = line[:pos], line[pos:]
            set_current_line(buffer, head)
            prefix += tail
    insert_block_after_current_line(buffer, [prefix])


def replace_character(buffer, c):
    pos = buffer.cursor[0]
    line = get_current_line(buffer)
    if line is not None:
        line[pos] = c
        set_current_line(buffer, line)
    return line


def replace_current_line(buffer):
    line = get_current_line(buffer)
    if line is not None:
        indent = " " * find_start_word_pos(line)
        set_clipboard(buffer, line, True)
        set_current_line(buffer, indent)
    return line


def replace_end_of_current_line(buffer):
    pos = buffer.cursor[0]
    line = get_current_line(buffer)
    if line is not None:
        head, tail = line[:pos], line[pos:]
        set_clipboard(buffer, tail)
        set_current_line(buffer, head)
    return line


def replace_current_word(buffer):
    pos = buffer.cursor[0]
    line = get_current_line(buffer)
    if line is not None:
        start, end = pos, find_next_word_pos(line, pos)
        if end > start:
            set_clipboard(buffer, line[start:end - 1])
            set_current_line(buffer, line[:start] + line[end - 1:])
        else:
            head, tail = line[:start], line[start:]
            set_clipboard(buffer, tail)
            set_current_line(buffer, head)
    return line


def delete_character(buffer):
    pos = buffer.cursor[0]
    line = get_current_line(buffer)
    if line is not None and pos < len(line):
        head, c, tail = line[:pos], line[pos], line[pos + 1:]
        set_clipboard(buffer, c)
        set_current_line(buffer, head + tail)
    return line


def delete_current_line(buffer):
    line = get_current_line(buffer)
    if line is not None:
        set_clipboard(buffer, line, True)
        delete_buffer_current_line(buffer)
    return line


def delete_end_of_current_line(buffer):
    pos = buffer.cursor[0]
    line = get_current_line(buffer)
    if line is not None:
        head, tail = line[:pos], line[pos:]
        set_clipboard(buffer, tail)
        set_current_line(buffer, head)
    return line


def delete_current_word(buffer):
    pos = buffer.cursor[0]
    line = get_current_line(buffer)
    if line is not None:
        start, end = pos, find_next_word_pos(line, pos)
        if end > start:
            set_clipboard(buffer, line[start:end])
            set_current_line(buffer, line[:start] + line[end:])
        else:
            set_clipboard(buffer, line[start:])
            set_current_line(buffer, line[:start])
    return line 


def copy_current_line(buffer):
    line = get_current_line(buffer)
    if line is not None:
        set_clipboard(buffer, line, True)
    return line


def copy_end_of_current_line(buffer):
    pos = buffer.cursor[0]
    line = get_current_line(buffer)
    if line is not None:
        _, tail = line[:pos], line[pos:]
        set_clipboard(buffer, tail)
    return line


def copy_current_word(buffer):
    pos = buffer.cursor[0]
    line = get_current_line(buffer)
    if line is not None:
        start, end = pos, find_next_word_pos(line, pos)
        if end > start:
            set_clipboard(buffer, line[start:end - 1])
        else:
            set_clipboard(buffer, line[start:])
    return line


def paste_data_after_current_line(buffer):
    insert_block_after_current_line(buffer, get_clipboard())
    

def paste_data_before_current_line(buffer):
    insert_block_before_current_line(buffer, get_clipboard())


def paste_data(buffer):
    data = get_clipboard()
    if len(data) > 0:
        insert_character(buffer, data[0])
        if len(data) > 1:
            insert_block_after_current_line(buffer, get_clipboard()[1:])
