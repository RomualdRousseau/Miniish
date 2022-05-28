from miniish.constants import *
from miniish.widgets import *

class DrawBoard(Widget):
    """Widget to draw a sprite.
    """

    def __init__(self, id_, pos_, size_):
        Widget.__init__(self, id_, pos_, size_)
        self.cell_size = (int((size_[0] - 2) / 8), int((size_[1] - 2) / 8))
        self.tool_funcs = [
                self.tool_pen,
                self.tool_paste,
                self.tool_select,
                self.tool_pan,
                self.tool_paint
                ]
        self.tool_func = None
        self.selected_tool = -1
        self.selected_sprite = -1
        self.canvas = [[0 for j in range(8)] for i in range(8)]
        self.select_start = None
        self.select_size = None
        self.clipboard = None
        self.init_ui()

    #
    # Widget interface
    #

    def init_ui(self):
        pass

    def update(self):
        # The tool changed
        if self.selected_tool != self.sprite_picker.tool:
            self.selected_tool = self.sprite_picker.tool
            self.tool_func = self.tool_funcs[self.selected_tool]
        # The sprite changed
        if self.selected_sprite != self.sprite_picker.selected:
            self.selected_sprite = self.sprite_picker.selected
            self.canvas = self._copy((0, 0), (8, 8))
        # Call the tool func and change the mouse cursor
        m = mxy()
        if self.inbounds(m):
            mcur(1)
            (x, y) = self._scr_to_brd(m)
            if 0 <= x < 8 and 0 <= y < 8:
                self.tool_func((x, y))
        else:
            mcur()

    def draw(self):
        (w, h) = self.cell_size
        # Draw the background
        rectfill(self.pos + self.size, BLACK)
        # Draw the board
        for i in range(8):
            for j in range(8):
                pixel = self.canvas[i][j]
                rectfill(self._brd_to_scr((j, i)) + (w, h), pixel)
        # Draw the selection
        if self.select_start is not None:
            pos = self._brd_to_scr(self.select_start)
            siz = (self.select_size[0] * w, self.select_size[1] * h)
            rect(pos + siz, WHITE)
       
    def tool_pen(self, pos):
        if mbtn():
            pixel = self.color_picker.selected
            self._draw_pixel(pos, pixel)

    def tool_paste(self, pos):
        if mbtn() and self.clipboard is not None:
           self._paste(pos) 

    def tool_select(self, pos):
        if mbtn():
            if self.select_start is None:
                self.select_start = pos
                self.select_size = (0, 0)
            else:
                self.select_size = (
                        pos[0] - self.select_start[0] + 1,
                        pos[1] - self.select_start[1] + 1
                        )
        elif self.select_start is not None:
            self.clipboard = self._copy(self.select_start, self.select_size)
            self.select_start = None
            self.select_size = None

    def tool_pan(self, pos):
        pass

    def tool_paint(self, pos):
        DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        def fill(x, y, c1, c2):
            if c1 != c2 and 0 <= x < 8 and 0 <= y < 8 and self.canvas[y][x] == c1:
                self._draw_pixel((x, y), c2)
                for i in range(len(DIRS)):
                    fill(x + DIRS[i][0], y + DIRS[i][1], c1, c2)
        if mbtn():
            col1 = self.canvas[pos[1]][pos[0]]
            col2 = self.color_picker.selected
            fill(pos[0], pos[1], col1, col2)

    #
    # Privates
    # 

    def _copy(self, pos, size):
        (x, y), (w, h) = self._brd_to_sps(pos), size
        return [[sget((x + j, y + i)) for j in range(w)] for i in range(h)]

    def _paste(self, pos):
        for i in range(len(self.clipboard)):
            for j in range(len(self.clipboard[i])):
                pixel = self.clipboard[i][j]
                self._draw_pixel((pos[0] + j, pos[1] + i), pixel)

    def _draw_pixel(self, pos, pixel):
        (x, y) = pos
        if 0 <= x < 8 and 0 <= y < 8:
            self.canvas[y][x] = pixel
            sset(self._brd_to_sps((x, y)), pixel)

    def _scr_to_brd(self, pos):
        (x, y), (w, h) = self.pos, self.cell_size
        return (int((pos[0] - x + 3) / w), int((pos[1] - y + 3) / h))

    def _brd_to_scr(self, pos):
        (x, y), (w, h) = self.pos, self.cell_size
        return (x + pos[0] * w + 1, y + pos[1] * h + 1)

    def _brd_to_sps(self, pos):
        sel = self.selected_sprite
        return (int(sel % 16) * 8 + pos[0], int(sel / 16) * 8 + pos[1])
