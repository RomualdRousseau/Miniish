"""
Various functions

"""

import re
import pyperclip


def find_start_word_pos(line):
    pattern = r"^\s+"
    match = re.search(pattern, line)
    return match.end() if match is not None else 0


def find_next_word_pos(line, pos, spaces = True):
    pattern = r"\W+" if spaces else r"\s+"
    match = re.search(pattern, line[pos:])
    return pos + (match.end() if match is not None else 0)


def find_previous_word_pos(line, pos, spaces = True):
    pattern = r"\w+\W*$" if spaces else r"\S+\s*$"
    match = re.search(pattern, line[:pos - 1])
    return match.start() if match is not None else pos


def get_clipboard():
   return [s.rstrip() for s in pyperclip.paste().split('\n')] 


def set_clipboard(buffer, data, full_line = False):
    if data is not None:
        pyperclip.copy(data)
    buffer.paste_full_line = full_line
    return data


def record_current_step(buffer, c):
    if c != '.': # avoid repeat of repeat
        buffer.repeat.append(c)


def record_start_step(buffer):
    buffer.undo.append(("*", 0, None))
    buffer.redo = []
    buffer.repeat = []
