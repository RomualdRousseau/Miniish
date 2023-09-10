from typing import Callable

import pyco

from miniish.editor.widgets.widgets import Widget
from miniish.editor.widgets.sprite_picker import SpritePicker
from miniish.editor.widgets.color_picker import ColorPicker


class DrawBoard(Widget):
    """Widget to draw a sprite."""

    def __init__(self, id_, pos_, size_):
        Widget.__init__(self, id_, pos_, size_)
        self.cell_size: tuple[int, int] = (
            int((size_[0] - 2) / 8),
            int((size_[1] - 2) / 8),
        )
        self.tool_funcs: list[Callable[[tuple[int, int]], None]] = [
            self.tool_pen,
            self.tool_paste,
            self.tool_select,
            self.tool_pan,
            self.tool_paint,
        ]
        self.tool_func: Callable[[tuple[int, int]], None] | None = None
        self.selected_tool: int = -1
        self.selected_sprite: int = -1
        self.canvas: list[list[int]] = [[0 for j in range(8)] for i in range(8)]
        self.select_start: tuple[int, int] | None = None
        self.select_size: tuple[int, int] | None = None
        self.clipboard: list[list[int]] | None = None
        self.sprite_picker: SpritePicker | None = None
        self.color_picker: ColorPicker | None = None
        self.init_ui()

    #
    # Widget interface
    #

    def init_ui(self) -> None:
        pass

    def update(self) -> None:
        if self.sprite_picker is not None:
            # The tool changed
            if self.selected_tool != self.sprite_picker.tool:
                self.selected_tool = self.sprite_picker.tool
                self.tool_func = self.tool_funcs[self.selected_tool]
            # The sprite changed
            if self.selected_sprite != self.sprite_picker.selected:
                self.selected_sprite = self.sprite_picker.selected
                self.canvas = self._copy((0, 0), (8, 8))
        # Call the tool func and change the mouse cursor
        m = pyco.mxy()
        if self.inbounds(m):
            pyco.mcur(1)
            (x, y) = self._scr_to_brd(m)
            if 0 <= x < 8 and 0 <= y < 8 and self.tool_func is not None:
                self.tool_func((x, y))
        else:
            pyco.mcur()

    def draw(self) -> None:
        (w, h) = self.cell_size
        # Draw the background
        pyco.rectfill(self.pos + self.size, pyco.BLACK)
        # Draw the board
        for i in range(8):
            for j in range(8):
                pixel = self.canvas[i][j]
                pyco.rectfill(self._brd_to_scr((j, i)) + (w, h), pixel)
        # Draw the selection
        if self.select_start is not None and self.select_size is not None:
            pos = self._brd_to_scr(self.select_start)
            siz = (self.select_size[0] * w, self.select_size[1] * h)
            pyco.rect(pos + siz, pyco.WHITE)

    def tool_pen(self, pos: tuple[int, int]) -> None:
        if pyco.mbtn() and self.color_picker is not None:
            pixel = self.color_picker.selected
            self._draw_pixel(pos, pixel)

    def tool_paste(self, pos: tuple[int, int]) -> None:
        if pyco.mbtn() and self.clipboard is not None:
            self._paste(pos)

    def tool_select(self, pos: tuple[int, int]) -> None:
        if pyco.mbtn():
            if self.select_start is None:
                self.select_start = pos
                self.select_size = (0, 0)
            else:
                self.select_size = (
                    pos[0] - self.select_start[0] + 1,
                    pos[1] - self.select_start[1] + 1,
                )
        elif self.select_start is not None:
            self.clipboard = self._copy(self.select_start, self.select_size)
            self.select_start = None
            self.select_size = None

    def tool_pan(self, pos: tuple[int, int]) -> None:
        pass

    def tool_paint(self, pos: tuple[int, int]) -> None:
        DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def fill(x, y, c1, c2):
            if c1 != c2 and 0 <= x < 8 and 0 <= y < 8 and self.canvas[y][x] == c1:
                self._draw_pixel((x, y), c2)
                for i in range(len(DIRS)):
                    fill(x + DIRS[i][0], y + DIRS[i][1], c1, c2)

        if pyco.mbtn() and self.color_picker is not None:
            col1 = self.canvas[pos[1]][pos[0]]
            col2 = self.color_picker.selected
            fill(pos[0], pos[1], col1, col2)

    #
    # Privates
    #

    def _copy(self, pos, size):
        (x, y), (w, h) = self._brd_to_sps(pos), size
        return [[pyco.sget((x + j, y + i)) for j in range(w)] for i in range(h)]

    def _paste(self, pos):
        if self.clipboard is not None:
            for i in range(len(self.clipboard)):
                for j in range(len(self.clipboard[i])):
                    pixel = self.clipboard[i][j]
                    self._draw_pixel((pos[0] + j, pos[1] + i), pixel)

    def _draw_pixel(self, pos, pixel):
        (x, y) = pos
        if 0 <= x < 8 and 0 <= y < 8:
            self.canvas[y][x] = pixel
            pyco.sset(self._brd_to_sps((x, y)), pixel)

    def _scr_to_brd(self, pos):
        (x, y), (w, h) = self.pos, self.cell_size
        return (int((pos[0] - x + 3) / w), int((pos[1] - y + 3) / h))

    def _brd_to_scr(self, pos):
        (x, y), (w, h) = self.pos, self.cell_size
        return (x + pos[0] * w + 1, y + pos[1] * h + 1)

    def _brd_to_sps(self, pos):
        sel = self.selected_sprite
        return (int(sel % 16) * 8 + pos[0], int(sel / 16) * 8 + pos[1])
