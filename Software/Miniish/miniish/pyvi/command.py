"""
Functions to deal with command operations

"""

import re

from .buffer import *
from .viewport import *


def execute_command(buffer):
    if re.match("/", buffer.command):
        word = buffer.command[1:] 
        search_buffer_all(buffer, word)
        move_cursor_next_search(buffer)
    elif re.match(":%s/", buffer.command):
        params = buffer.command.split("/")
        search_buffer_all(buffer, params[1])
        move_cursor_next_search(buffer)
        replace_buffer_all(buffer, params[1], params[2])
    elif re.match(":\\d+$", buffer.command):
        line = max(0, int(buffer.command[1:]) - 1)
        move_cursor_goto(buffer, (line, 0))
    elif buffer.command_func is not None:
        buffer.command_func(buffer.command)
