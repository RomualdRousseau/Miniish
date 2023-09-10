from math import ceil

import pyco
import pyco.sys
import pyvi

from miniish.kernel import disk
from miniish.constants import COLOR_CURSOR, COLOR_MAIN_FG, COLOR_STAT_BG, COLOR_STAT_FG
from miniish.widgets.widgets import ButtonGroup, Button, MAX_BUFFERS


class CodeEditor:
    """The Code editor.

    Notes
    -----
    Mimic the beloved VI :)
    Syntax color for 6502 ASM and Python
    """

    name = "code-editor"

    def __init__(self):
        self.buffers = [self._create_buffer()]
        self.buffer = self.buffers[0]
        self.buffer_id = 0
        self.timer = 0
        self.language = None

    #
    # App interface
    #

    def init_ui(self):
        self.ui_tabs = ButtonGroup(-1, (2, 0), [])
        self.ui_plus = Button(-1, (2, 0), (12, 12), self._add_buffer)
        self._create_tab(0)

    def update(self):
        # Handle buffers management
        self.ui_tabs.update()
        if len(self.buffers) < MAX_BUFFERS:
            self.ui_plus.update()
        # Handle inputs and tranfer to vi
        c = pyco.input()
        if c is not None:
            if c == "escape" and pyvi.get_state(self.buffer) != "INSERT":
                return False
            pyvi.update_buffer(self.buffer, c)
        # Timer for the blinking cursor
        self.timer += 1
        return True

    def draw(self):
        # Draw the buffers with labels
        self.ui_tabs.draw()
        for b in range(len(self.buffers)):
            pyco.print("%d" % (b), (b * 9 + 6, 2), COLOR_STAT_BG)
        if len(self.buffers) < MAX_BUFFERS:
            self.ui_plus.draw()
        # Draw the text
        y = 8
        for i in range(pyvi.get_height_in_lines(self.buffer)):
            line = pyvi.get_line_in_view(self.buffer, i)
            if line is not None:
                x = -4 * pyvi.get_current_line_offset(self.buffer)
                self.language.colorize(line, (x, y))  # type: ignore
            else:
                pyco.print("~", (0, y), COLOR_MAIN_FG)
            y += 6
        # Draw the status line
        pyco.color(COLOR_STAT_FG)
        if pyvi.get_state(self.buffer) != "COMMAND":
            # Draw line statistics
            linestat = "%d/%d" % (
                pyvi.get_current_line_number(self.buffer),
                pyvi.get_count_of_lines(self.buffer),
            )
            pyco.print(pyvi.get_state(self.buffer).lower(), (1, 122))
            pyco.print(linestat, (128 - len(linestat) * 4, 122))
            # Draw the blinking cursor
            if int(self.timer / 8) % 2 == 0:
                (x, y) = pyvi.get_cursor(self.buffer)
                pyco.rectfill((x * 4, y * 6 + 8, 4, 6), COLOR_CURSOR)
        else:
            # Draw the command
            pyco.print(pyvi.get_command(self.buffer), (1, 122))
            # Draw the blinking cursor
            if int(self.timer / 8) % 2 == 0:
                x = len(pyvi.get_command(self.buffer))
                pyco.rectfill((x * 4, 121, 4, 6))

    #
    # Serialization interface
    #

    def load(self):
        self.buffers = []
        self.ui_tabs.buttons = []
        
        for source in pyco.sys.get_sources():
            buffer = self._create_buffer()
            buffer.buf = source
            self.buffers.append(buffer)
            self._create_tab(len(self.buffers) - 1)
            
        if len(self.buffers) == 0:
            self.buffers.append(self._create_buffer())
            self._create_tab(len(self.buffers) - 1)
            
        # Set the first buffer as default
        self.buffer = self.buffers[0]
        self.buffer_id = 0
        self.ui_tabs.select(0, True)

    def save(self,):
        sources = []
        for i in range(len(self.buffers)):
            sources.append(pyvi.get_text(self.buffers[i]))
        pyco.sys.set_sources(sources)

    #
    # Privates
    #

    def _guess_file_name(self, i, line):
        if i == 0:
            return "main.s"
        elif line[0] == ";":
            return line[1:].strip()
        else:
            return f"buffer{i}.i"

    def _create_buffer(self):
        buf = pyvi.create_empty_buffer((int(128 / 4), ceil(113 / 6)), self._command_func)
        return buf

    def _add_buffer(self, b):
        if len(self.buffers) < 8:
            self.buffers.append(self._create_buffer())
            self.buffer = self.buffers[-1]
            self.buffer_id = len(self.buffers) - 1
            self._create_tab(self.buffer_id)

    def _switch_buffer(self, b):
        if self.buffer_id != b.id:
            self._cleanup_buffer()
            self.buffer = self.buffers[b.id]
            self.buffer_id = b.id

    def _cleanup_buffer(self):
        if len(self.buffers) > 1 and pyvi.is_buffer_empty(self.buffer):
            del self.buffers[self.buffer_id]
            self._remove_last_tab()

    def _create_tab(self, buffer_id):
        tab = Button(buffer_id, (1, 0), (10, 11), self._switch_buffer)
        self.ui_tabs.append(tab)
        self.ui_plus.pos = (2 + len(self.ui_tabs.buttons) * 9, 0)

    def _remove_last_tab(self):
        self.ui_tabs.remove(-1)
        self.ui_plus.pos = (2 + len(self.ui_tabs.buttons) * 9, 0)

    def _command_func(self, command):
        if command == ":w":
            editor = disk.open("editor")
            sketch = disk.open("sketch")
            if editor is not None and sketch is not None and sketch.last_loaded is not None:  # type: ignore
                editor.save()  # type: ignore
                pyco.sys.save_cartdrige(sketch.last_loaded)  # type: ignore
