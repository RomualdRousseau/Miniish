from miniish.pyco import *
from miniish.pyco import sys

class Widget:

    def __init__(self, id_, pos_, size_):
        self.id = id_
        self.opos = pos_
        self.pos = pos_
        self.size= size_

    def inbounds(self, p):
        a = self.pos[0] <= p[0] < self.pos[0] + self.size[0]
        b = self.pos[1] <= p[1] < self.pos[1] + self.size[1]
        return a and b


class Button(Widget):

    def __init__(self, id_, pos_, frames_, callback_):
        Widget.__init__(self, id_, pos_, (8, 8))
        self.frames = frames_
        self.callback = callback_
        self.over = False
        self.press = False
        self.click = False
        self.toggle = False
        self.toggle_mode = False

    def update(self):
        #pover = self.over
        self.over = self.inbounds(mxy())
        self.press = self.over and mbtn()
        self.click = self.click or self.press
        if self.click and not mbtn():
            self.click = False
            self.toggle = not self.toggle
            if self.callback:
                self.callback(self)
        #if not pover and self.over:
        #    mcur(2)
        #elif pover and not self.over:
        #    mcur()

    def draw(self):
        sys.use("SYSTEM")
        toggle = self.toggle_mode and self.toggle
        press = not self.toggle_mode and self.press
        spr(self.frames[0 if toggle or press else 1], self.pos)
        sys.use()


class ButtonGroup(Widget):

    def __init__(self, id_, pos_, buttons_, toggle_mode_ = False, select_ = None):
        Widget.__init__(self, id_, pos_, (len(buttons_) * 8, 8))
        self.buttons = buttons_
        self.last_selected = None

        if toggle_mode_:
            for button in self.buttons:
                button.toggle_mode = True
            if select_ is not None:
                for b in select_:
                    self.buttons[b].toggle = True
        
        if select_ is not None:
            self.last_selected = self.buttons[select_[-1]]

        self.recalculate()

    def update(self):
        for button in self.buttons:
            button.update()
            if button.click:
                if self.last_selected is not None:
                    self.last_selected.press = False
                self.last_selected = button
            if self.last_selected is not None:
                self.last_selected.press = True
       
    def draw(self):
        for button in self.buttons:
            button.draw()

    def select(self, b, v):
        button = self.buttons[b]
        button.toggle = v
        if v:
            if self.last_selected is not None:
                self.last_selected.press = False
            self.last_selected = button
        if self.last_selected is not None:
            self.last_selected.press = True

    def append(self, button):
        self.buttons.append(button)
        self.recalculate()
        self.last_selected = self.buttons[-1]

    def remove(self, i):
        del self.buttons[i]

    def recalculate(self):
        off = self.pos
        for button in self.buttons:
            button.pos = (button.opos[0] + off[0], button.opos[1] + off[1])
            off = (button.opos[0] + off[0] + 8, off[1])

class TextSpinner(Widget):
    
    def __init__(self, id_, pos_, size_, min_, max_, callback_ = None):
        Widget.__init__(self, id_, pos_, size_)
        self.min = min_
        self.max = max_
        self.value = min_
        self.callback = callback_

    def update(self):
        if self.inbounds(mxy()):
            if mbtn(0):
                self.value += 1
                self.value = max(self.min, min(self.value, self.max))
                if self.callback:
                    self.callback(self)
            elif mbtn(2):
                self.value -= 1
                self.value = max(self.min, min(self.value, self.max))
                if self.callback:
                    self.callback(self)

    def draw(self):
        rectfill(self.pos + self.size, BLACK)
        print("%02d"%(self.value), (self.pos[0] + 1, self.pos[1] + 1), WHITE)

    def get_value(self):
        return self.value

    def set_value(self, value_):
        self.value = value_
