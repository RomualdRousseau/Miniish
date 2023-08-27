"""
Various sub routines

"""

from .globals import *


def get_palette_exact(col):
    for i in range(len(PALETTE)):
        if col == PALETTE[i]:
            return i
    return BLACK


def char_size(code):
    return 4 if code < 96 else 8


def render_text(text, col):
    # Generate sprite characters
    seq, cp = [], 0 
    for char in text:
        code = ord(char) - 32
        if not 0 <= code < 128:
            code = 31
        x, y = int(code % 16) * 8, int(code / 16) * 6
        seq.append((PYCO.font, (cp, 0), (x, y, 8, 6))) 
        cp += char_size(code)
    # Blit the sprite characters on a surface
    render = pg.Surface((cp, 6), pg.SRCALPHA)
    render.blits(seq)
    # Tint the characters
    if col != WHITE:
        render.fill(col, None, pg.BLEND_RGBA_MULT)
    return render


def load_asset_png(file_name):
    file_name = file_name + ".png" if ".png" not in file_name else file_name 
    file_path = get_asset_path(file_name)
    return pg.image.load(file_path).convert_alpha()


def get_asset_path(file_name):
    return os.path.join('assets', file_name)


def guess_file_name(i, line):
    if i == 0:
        return "main.s"
    elif line[0] == ';':
        return line[1:].strip()
    else:
        return f"buffer{i}.i"


def extend_key(event, key):
    if event.mod & pg.KMOD_SHIFT:
        return "shift-" + key
    elif event.mod & pg.KMOD_CTRL:
        return "control-" + key
    else:
        return key


def is_done(events):
    if not events:
        return not PYCO.running
    else:
        head, *tail = events
        if head.type == pg.KEYDOWN and not head.key in IGNORE_KEYS:
            PYCO.keybuf.append(head)
        elif head.type == pg.MOUSEWHEEL:
            PYCO.mouse_wheel = (head.x, head.y)
        return head.type == pg.QUIT or is_done(tail)
