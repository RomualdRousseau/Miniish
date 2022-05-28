"""
Functions to deal with command operations

"""

from .buffer import *
from .viewport import *


def execute_command(buffer):
    if len(buffer.command) > 0:
        params = buffer.command.split("/")
        if params[0] == ":%s":
            search_buffer_all(buffer, params[1])
            move_cursor_next_search(buffer)
            replace_buffer_all(buffer, params[1], params[2])
        elif params[0] == "":
            search_buffer_all(buffer, params[1])
            move_cursor_next_search(buffer)
