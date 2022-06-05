"""
Mouse functions

"""

from .globals import *

def update():
    if PYCO.mouse_mask is not None:
        PYCO.screen.blit(PYCO.mouse_mask, PYCO.mouse_pos)
    else:
        PYCO.mouse_mask = pg.Surface((8, 8))
    pos = pg.mouse.get_pos()
    PYCO.mouse_pos = (pos[0] / 4, pos[1] / 4) 
    PYCO.mouse_btn = pg.mouse.get_pressed()
    PYCO.mouse_mod = pg.key.get_mods()


def draw():
    PYCO.mouse_mask.blit(PYCO.screen, (0, 0), PYCO.mouse_pos + (8, 8))
    n = PYCO.mouse_cursor + 32
    rect = (int(n % 16) * 8, int(n / 16) * 8) + (8, 8)
    PYCO.screen.blit(PYCO.system_sheet, PYCO.mouse_pos, rect)
    PYCO.mouse_wheel = (0, 0)
