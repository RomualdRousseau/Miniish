"""
Functions to deal with the state machine

"""

from .buffer import *
from .viewport import *
from .edit import *
from .undo import *
from .subr import *
from .command import *

STATES = {
        "COMMAND": lambda b,c: state_command(b, c),
        "NORMAL" : lambda b,c: state_normal(b, c),
        "INSERT" : lambda b,c: state_insert(b, c),
        "CHANGE" : lambda b,c: state_change(b, c),
        "REPLACE": lambda b,c: state_replace(b, c),
        "DELETE" : lambda b,c: state_delete(b, c),
        "COPY"   : lambda b,c: state_copy(b, c),
        "GOTO"   : lambda b,c: state_goto(b, c)
        }


def execute_one_step(buffer, c):
    update_func = STATES[buffer.state]
    update_func(buffer, c)
    keep_cursor_inbounds(buffer)
    fix_zero_buffer(buffer)


def repeat_n_func(buffer, func):
    for n in range(buffer.selblock):
        func()
    buffer.selblock = 0


def state_command(buffer, c):
    global command
    if c == "return":
        buffer.state = "NORMAL"
        if len(buffer.command) > 0:
            record_start_step(buffer)
            execute_command(buffer)
            buffer.command = ""
        return True
    elif c == "backspace":
        buffer.command = buffer.command[:-1]
        return True
    else:
        buffer.command += c
        return True


def state_normal(buffer, c):
    state_normal_action(buffer, c) \
        or state_normal_navigation(buffer, c) \
        or state_normal_enter_insert(buffer, c) \
        or state_normal_enter_delete(buffer, c) \
        or state_normal_enter_copy(buffer, c)


def state_normal_action(buffer, c):
    if c in (':', '/'):
        buffer.state = "COMMAND"
        buffer.command = c
        buffer.selblock = 0
        return True
    elif c == 'u':
        do_undo(buffer)
        buffer.selblock = 0
        return True
    elif c == "control-r":
        do_redo(buffer)
        buffer.selblock = 0
        return True
    elif c == '.':
        # do repeat
        for c in buffer.repeat:
            execute_one_step(buffer, c)
        buffer.selblock = 0
        return True
    elif (c == '*' or c == 'n') and len(buffer.search) > 0:
        location = buffer.search[buffer.search_curr]
        move_cursor_goto(buffer, location)
        buffer.search_curr = (buffer.search_curr + 1) % len(buffer.search)
        buffer.selblock = 0
        return True
    elif c.isnumeric():
        buffer.selblock = buffer.selblock * 10 + int(c)
        return buffer.selblock > 0
    else:
        return False


def state_normal_navigation(buffer, c):
    if c == 'h' or c == "left":
        repeat_n_func(buffer, lambda: move_cursor_left(buffer))
        return True
    elif c == 'l' or c == "right":
        repeat_n_func(buffer, lambda: move_cursor_right(buffer))
        return True
    elif c == 'k' or c == "up":
        repeat_n_func(buffer, lambda: move_cursor_up(buffer))
        return True
    elif c == 'j' or c == "down":
        repeat_n_func(buffer, lambda: move_cursor_down(buffer))
        return True
    elif c == '0':
        move_cursor_start_of_line(buffer, False)
        return True
    elif c == '^':
        move_cursor_start_of_line(buffer, True)
        return True
    elif c == '$':
        move_cursor_end_of_line(buffer)
        return True
    elif c == 'w':
        repeat_n_func(buffer, lambda: move_cursor_next_word(buffer, True))
        return True
    elif c == 'W':
        repeat_n_func(buffer, lambda: move_cursor_next_word(buffer, False))
        return True
    elif c == 'b':
        repeat_n_func(buffer, move_cursor_previous_word(buffer, True))
        return True
    elif c == 'B':
        repeat_n_func(buffer, move_cursor_previous_word(buffer, False))
        return True
    elif c == 'g':
        buffer.state = "GOTO"
        return True
    elif c == 'G':
        move_cursor_end_of_file(buffer)
        return True
    else:
        return False


def state_normal_enter_insert(buffer, c):
    if c == 'i' or c == 'a' and get_last_char_pos(buffer) == 0:
        buffer.state = "INSERT"
        record_start_step(buffer)
        record_current_step(buffer, c)
        return True
    elif c == 'I' or c == 'A' and get_last_char_pos(buffer) == 0:
        buffer.state = "INSERT"
        record_start_step(buffer)
        record_current_step(buffer, c)
        move_cursor_start_of_line(buffer, True)
        return True
    elif c == 'a':
        buffer.state = "INSERT"
        record_start_step(buffer)
        record_current_step(buffer, c)
        move_cursor_right(buffer)
        return True
    elif c == 'A':
        buffer.state = "INSERT"
        record_start_step(buffer)
        record_current_step(buffer, c)
        move_cursor_end_of_line(buffer)
        return True
    elif c == 'o':
        buffer.state = "INSERT"
        record_start_step(buffer)
        record_current_step(buffer, c)
        insert_blank_line_after_current_line(buffer, False)
        move_cursor_down(buffer)
        move_cursor_start_of_line(buffer, True)
        return True
    elif c == 'O':
        buffer.state = "INSERT"
        record_start_step(buffer)
        record_current_step(buffer, c)
        insert_blank_line_before_current_line(buffer)
        move_cursor_start_of_line(buffer, True)
        return True
    elif c == 'c':
        buffer.state = "CHANGE"
        record_start_step(buffer)
        record_current_step(buffer, c)
        return True
    elif c == 'C':
        buffer.state = "INSERT"
        record_start_step(buffer)
        record_current_step(buffer, c)
        move_cursor_start_of_line(buffer, True)
        replace_end_of_current_line(buffer)
        return True
    elif c == 'r':
        buffer.state = "REPLACE"
        record_start_step(buffer)
        record_current_step(buffer, c)
        return True
    elif c == 'R':
        buffer.state = "INSERT"
        record_start_step(buffer)
        record_current_step(buffer, c)
        replace_end_of_current_line(buffer)
        return True
    else:
        return False


def state_normal_enter_delete(buffer, c):
    if c == 'x' and len(buffer.buf) > 0:
        record_start_step(buffer)
        repeat_n_func(buffer, lambda: (f() for f in [
            record_current_step(buffer, c),
            delete_character(buffer)]))
        return True
    elif c == 'd':
        buffer.state = "DELETE"
        record_start_step(buffer)
        record_current_step(buffer, c)
        return True
    return False


def state_normal_enter_copy(buffer, c):
    if c == 'y':
        buffer.state = "COPY"
        return True
    elif c == 'Y':
        copy_current_line(buffer)
        return True
    elif c == 'p':
        record_start_step(buffer)
        record_current_step(buffer, c)
        if buffer.paste_full_line:
            paste_data_after_current_line(buffer)
            move_cursor_down(buffer)
            move_cursor_start_of_line(buffer, True)
        else:
            move_cursor_right(buffer)
            paste_data(buffer)
        return True
    elif c == 'P':
        record_start_step(buffer)
        record_current_step(buffer, c)
        if buffer.paste_full_line:
            paste_data_before_current_line(buffer)
            move_cursor_start_of_line(buffer, True)
        else:
            paste_data(buffer)
        return True
    return False


def state_insert(buffer, c):
    if c == "return":
        record_current_step(buffer, c)
        insert_blank_line_after_current_line(buffer, True)
        move_cursor_down(buffer)
        move_cursor_start_of_line(buffer, True)
    elif c == "backspace":
        record_current_step(buffer, c)
        if buffer.cursor[0] > 0:
            move_cursor_left(buffer)
            delete_character(buffer)
        elif get_buffer_pos(buffer) > 0:
            line = delete_current_line(buffer)
            move_cursor_up(buffer)
            move_cursor_end_of_line(buffer)
            set_current_line(buffer, get_current_line(buffer) + line)
    elif c == "escape":
        buffer.state = "NORMAL"
        record_current_step(buffer, c)
    elif len(c) == 1:
        record_current_step(buffer, c)
        insert_character(buffer, c)
        move_cursor_right(buffer)
    return True


def state_change(buffer, c):
    if c == 'c':
        buffer.state = "INSERT"
        record_current_step(buffer, c)
        replace_current_line(buffer)
    elif c == '$':
        buffer.state = "INSERT"
        record_current_step(buffer, c)
        replace_end_of_current_line(buffer)
    elif c == 'w':
        buffer.state = "INSERT"
        record_current_step(buffer, c)
        replace_current_word(buffer)
    else: 
        buffer.state = "NORMAL"
    return True

def state_replace(buffer, c):
    record_current_step(buffer, c)
    replace_character(buffer, c)
    buffer.state = "NORMAL"
    return True

def state_delete(buffer, c):
    if c == 'd':
        buffer.state = "NORMAL"
        repeat_n_func(buffer, lambda: (f() for f in [
            record_current_step(buffer, c),
            delete_current_line(buffer)]))
    elif c == '$':
        buffer.state = "NORMAL"
        record_current_step(buffer, c)
        delete_end_of_current_line(buffer)
    elif c == 'w':
        buffer.state = "NORMAL"
        record_current_step(buffer, c)
        delete_current_word(buffer)
    else:
        buffer.state = "NORMAL"
    return True


def state_copy(buffer, c):
    if c == 'y':
        buffer.state = "NORMAL"
        copy_current_line(buffer)
    elif c == '$':
        buffer.state = "NORMAL"
        copy_end_of_current_line(buffer)
    elif c == 'w':
        buffer.state = "NORMAL"
        copy_current_word(buffer)
    else:
        buffer.state = "NORMAL"
    return True


def state_goto(buffer, c):
    if c == 'g':
        buffer.state = "NORMAL"
        move_cursor_start_of_file(buffer)
    else:
        buffer.state = "NORMAL"
    return True
