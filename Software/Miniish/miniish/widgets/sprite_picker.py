from miniish.widgets import *


class SpritePicker(Widget):
    """Widget to pick a sprite from the sprite sheet.
    """

    def __init__(self, id_, pos_, size_):
        Widget.__init__(self, id_, pos_, size_)
        self.cell_size = (int(size_[0] / 16), int((size_[1] - 2) / 4))
        self.page = 0
        self.tool = 0
        self.selected = 1
        self.init_ui() 

    #
    # Widget interface
    #

    def init_ui(self):
        (x, y), (w, h) = self.pos, self.size
        # Init the page selector
        self.tabs = ButtonGroup(-1, (x + w - 4 * 8, y - 8), [
                Button(i, (0, 0), (37 + i * 2, 36 + i * 2), self._switch_tab) for i in range(4)    
                ], False, [0])
        # Init the tool selector
        self.tools = ButtonGroup(-1, (x + 20, y - 9), [
                Button(i, (1, 0), (22 + i * 2, 23 + i * 2), self._switch_tool) for i in range(5)    
                ], False, [0])

    def update(self):
        # Update widgets
        self.tabs.update()
        self.tools.update()
        # Select a new sprite
        (mx, my) = mxy()
        if self.inbounds((mx, my)) and mbtn():
            (x, y), (w, h) = self.pos, self.cell_size
            pos = (int((mx - x) / w), int((my - y - 1) / h))
            self.selected = self.page * 16 * 4 + pos[1] * 16 + pos[0] 
        
    def draw(self):
        (x, y), (w, h) = self.pos, self.cell_size
        # Draw the background
        rectfill(self.pos + self.size, BLACK)
        # Draw the widgets
        self.tabs.draw()
        self.tools.draw()
        # Draw the sprites
        for i in range(4):
            for j in range(16):
                pos = (x + j * w, y + i * h + 1)
                spr(self.page * 16 * 4 + i * 16 + j, pos)
        # Draw the sprite selector
        sel = self.selected - self.page * 16 * 4
        pos = (x + int(sel % 16) * w - 1, y + int(sel / 16) * h)
        rect(pos + (w + 2, h + 2), WHITE)
        # Draw the selected sprite preview
        spr(self.selected, (x + 69, y - 9))
        # Draw the selected sprite number
        rectfill((x + 78, y - 8, 13, 7), 6)
        print("%03d"%(self.selected), (x + 79, y - 7), 13)

    #
    # Privates
    #

    def _switch_tab(self, b):
        sel = self.selected - self.page * 16 * 4
        self.page = b.id
        self.selected = sel + self.page * 16 * 4
        pass

    def _switch_tool(self, b):
        self.tool = b.id
