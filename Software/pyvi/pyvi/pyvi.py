"""
Entry point to the VIM implementation

"""

from .buffer import *
from .viewport import *
from .states import *


def create_empty_buffer(view_size, command_func=None):
    return Buffer(view_size, command_func)


def update_buffer(buffer, c):
    execute_one_step(buffer, c) 
    

def get_command(buffer):
    return buffer.command

def get_state(buffer):
    return buffer.state


def get_cursor(buffer):
    return buffer.cursor


def get_text(buffer):
    return buffer.buf


def get_current_line_number(buffer):
    return get_buffer_pos(buffer) + 1


def get_count_of_lines(buffer):
    return get_buffer_len(buffer)


def get_height_in_lines(buffer):
    return buffer.height_in_lines


def get_line_in_view(buffer, i):
    return get_buffer_line(buffer, i) if i <= get_last_line_pos(buffer) else None


def get_current_line_offset(buffer):
    return buffer.line_pos


def is_buffer_empty(buffer):
    return len(buffer.buf) == 0 or len(buffer.buf) == 1 and len(buffer.buf[0]) == 0
