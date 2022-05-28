import sys
from math import ceil

from miniish.widgets import *
from miniish.pyco import sys

class MapBoard(Widget):
    """Widget to draw a map.
    """

    def __init__(self, id_, pos_, size_):
        Widget.__init__(self, id_, pos_, size_)
        self.cell_size = (4, 4)
        self.tool_funcs = [
                self.tool_pen,
                self.tool_paste,
                self.tool_select,
                self.tool_pan,
                self.tool_paint
                ]
        self.tool_func = None
        self.selected_tile = None
        self.selected_tool = -1
        self.selected_sprite = -1
        self.select_start = None
        self.select_size = None
        self.clipboard = None
        self.pmouse = None
        self.origin = (0, 0)
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
        m = mxy()
        if self.inbounds(m):
            (x, y) = self._scr_to_brd(m)
            # Call the tool func and change the mouse cursor
            if 0 <= x < 128 and 0 <= y < 64:
                self.tool_func((x, y), m)
                self.selected_tile = (x, y)
            elif self.tool_func == self.tool_pan:
                self.tool_func((x, y), m)
            # Handle zoom
            wheel = -PYCO.mouse_wheel[1]
            if wheel != 0:
                self.tool_zoom((x, y), m, wheel)
        else:
            self.selected_tile = None

    def draw(self):
        (x, y), (w, h), (px, py) = self.pos, self.cell_size, self.origin
        (px, py) = (int(px), int(py))
        clip(self.pos + self.size)
        # Draw the background
        sys.use("SYSTEM")
        for i in range(9):
            for j in range(16):
                spr(44, (x + j * 8, y + i * 8))
        sys.use()
        # Draw the board
        r = (px, py) + (ceil(128 / w), ceil(72 / h))
        self._map(self.pos, r)
        # Draw the grid
        if self.pmouse is not None:
            self._grid(self.pos, r)
        else:
            r = (x - px * w, y - py * h, w * 128, h * 64)
            rect(self._expand(r, 2), WHITE)
            rect(self._expand(r, 1), BLACK)
        clip()
        # Draw the selection
        if self.select_start is not None:
            p = self._brd_to_scr(self.select_start)
            s = (self.select_size[0] * w, self.select_size[1] * h)
            rect(p + s, WHITE)
        elif self.selected_tile is not None:
            # Draw the current tile selection
            if self.tool_func != self.tool_pan:
                r = self._brd_to_scr(self.selected_tile) + (w, h)
                rect(self._expand(r, 1), WHITE) 
            # Draw the status
            print("view x: %03d y: %03d"%self.selected_tile, (0, 122), COLOR_STAT_FG)
       
    def tool_pen(self, p, m):
        if mbtn():
            mset(p, self.selected_sprite)

    def tool_paste(self, p, m):
        if mbtn() and self.clipboard is not None:
           self._paste(p) 

    def tool_select(self, p, m):
        if mbtn():
            if self.select_start is None:
                self.select_start = p
                self.select_size = (0, 0)
            else:
                self.select_size = (
                        p[0] - self.select_start[0] + 1,
                        p[1] - self.select_start[1] + 1
                        )
        elif self.select_start is not None:
            self.clipboard = self._copy(self.select_start, self.select_size)
            self.select_start = None
            self.select_size = None

    def tool_pan(self, p, m):
        if mbtn():
            if self.pmouse is None:
                self.pmouse = m
            else:
                (w, h) = self.cell_size
                dx = (m[0] - self.pmouse[0]) * 2 / w
                dy = (m[1] - self.pmouse[1]) * 2 / h
                self.origin = (self.origin[0] - dx, self.origin[1] - dy)
                self.pmouse = m
        else:
            self.pmouse = None

    def tool_paint(self, p, m):
        DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        def fill(x, y, t1, t2):
            if  t1 != t2 and 0 <= x < 128 and 0 <= y < 64 and mget((x, y)) == t1:
                mset((x, y), t2)
                for i in range(len(DIRS)):
                    fill(x + DIRS[i][0], y + DIRS[i][1], t1, t2)
        if mbtn():
            tile1 = mget(p)
            tile2 = self.selected_sprite
            sys.setrecursionlimit(8000)
            fill(p[0], p[1], tile1, tile2)
            sys.setrecursionlimit(1000)

    def tool_zoom(self, p, m, dz):
        (w, h) = self.cell_size
        (w, h) = (max(2, min(w + dz, 8)), max(2, min(h + dz, 8)))
        if (w, h) != self.cell_size:
            self.cell_size = (w, h)
            mm = self._brd_to_scr(p)
            self.origin = (
                    self.origin[0] + (mm[0] + 3 - m[0]) / w,
                    self.origin[1] + (mm[1] + 3 - m[1]) / h
                    )

    #
    # Privates
    # 

    def _copy(self, p, s):
        (x, y), (w, h) = p, s
        return [[mget((x + j, y + i)) for j in range(w)] for i in range(h)]

    def _paste(self, p):
        for i in range(len(self.clipboard)):
            for j in range(len(self.clipboard[i])):
                mset((p[0] + j, p[1] + i), self.clipboard[i][j])

    def _scr_to_brd(self, p):
        (x, y), (w, h), (px, py) = self.pos, self.cell_size, self.origin
        return (int(px) + int((p[0] - x) / w), int(py) + int((p[1] - y) / h))

    def _brd_to_scr(self, p):
        (x, y), (w, h), (px, py) = self.pos, self.cell_size, self.origin
        return (x + (p[0] - int(px)) * w, y + (p[1] - int(py)) * h)

    def _expand(self, r, o):
        (x, y, w, h) = r
        return (x - o, y - o, w + o * 2, h + o * 2) 

    def _map(self, p, r):
        (w, h) = self.cell_size
        (celx, cely, celw, celh) = r
        for i in range(celh):
            cx, cy = celx, cely + i
            sx, sy = p[0], p[1] + i * h
            for j in range(celw):
                if 0 <= cx < 128 and 0 <= cy < 64:
                    tile = PYCO.map[cy][cx]
                    if tile > 0:
                        sspr(tile, (sx, sy), (w, h))
                    else:
                        rectfill((sx, sy) + (w, h), BLACK)
                cx += 1
                sx += w

    def _grid(self, p, r):
        (w, h) = self.cell_size
        (celx, cely, celw, celh) = r
        for i in range(celh):
            cx, cy = celx, cely + i
            sx, sy = p[0], p[1] + i * h
            for j in range(celw):
                if 0 <= cx < 128 and 0 <= cy < 64:
                    rect((sx - 1, sy - 1) + (w + 1, h + 1), DARK_BLUE)
                if 0 <= cx <= 128 and 0 <= cy <= 64:
                    if (cx % 16) == 0 and (cy % 16) == 0:
                       rect((sx - 3, sy - 3) + (5, 5), DARK_BLUE)
                       rectfill((sx - 2, sy - 2) + (3, 3), LIGHT_GRAY)
                cx += 1
                sx += w


