"""
Functions to deal with graphic operations.
The interface is inspired by the PICO API.

"""

from .globals import *
from . import subr
from . import synth
from . import mouse

def sfx(n):
    """Play a sound.

    Parameters
    ----------
    n : The sound to play

    Notes
    -----

    """
    synth.play_sound(n)


def map(pos, cels):
    """Draws a portion of the map to the graphics buffer.

    Parameters
    ----------
    pos : The coordinates of the screen to place the upper left corner.
    cels : The position and dimensiton of the region of the map cell to draw.

    Notes
    -----
    The map is a grid of sprites from the sprite sheet, where each cell in the
    grid is assigned a sprite number. You can edit the map using the MINIISH map
    editor. You call the map() function to draw a region of the map (a subsection
    of the grid cells) onto the screen.

    You can use the map to draw large pictures by reusing sprite tiles in multiple
    cells. This is more memory efficient than drawing large images in pixels with
    the sprite editor, and easier to use than storing tables of sprite numbers in
    code.

    Any map cell set to sprite number 0 is not drawn, effectively making that cell
    transparent. You can use this along with using the transparent color for pixels
    in sprites to make regions of transparency in the image. A common technique is
    to layer multiple maps on top of one another, then animate the positions of
    these layers to produce effects such as parallax scrolling.

    Another use for maps is to design interactive levels or areas of a game world.
    When doing this, it is often necessary to determine which sprite is at a given
    location on the map, such as to determine whether a location next to the player
    is an obstruction. See mget().
    """
    pos = (pos[0] - PYCO.camera[0], pos[1] - PYCO.camera[1])
    (celx, cely, celw, celh) = cels
    seq = []
    for i in range(celh):
        cx, cy = celx, cely + i
        sx, sy = pos[0], pos[1] + i * 8
        for j in range(celw):
            if 0 <= cx < 128 and 0 <= cy < 64:
                n = PYCO.map[cy][cx]
                if n > 0:
                    r = (int(n % 16) * 8, int(n / 16) * 8, 8, 8)
                    seq.append((PYCO.sprite_sheet, (sx, sy), r)) 
            cx += 1
            sx += 8
    PYCO.screen.blits(seq)


def mget(cel):
    """Gets the sprite number assigned to a cell on the map.
    
    Parameters
    ----------
    cel : The column, row coordinates of the cell.

    Notes
    -----
    The mget() function returns the sprite number assigned to a cell on the map.
    If a cell was modified by a call to mset(), mget() returns the updated value.

    When using the map to store level designs, a common technique is to keep track
    of the player's effective cell position on the map, then use mget() to look for
    adjacent level features such as obstructions. This can be combined with sprite
    flags (read with fget()) to indicate which sprite tiles represent obstructions,
    so a general purpose test for obstructions only needs to read the flags.
    """
    if 0 <= cel[0] < 128 and 0 <= cel[1] < 64:
        return PYCO.map[cel[1]][cel[0]]
    else:
        return 0


def mset(cel, snum):
    """Sets a cell on the map to a new sprite number.

    Parameters
    ----------
    cel : The column, row coordinates of the cell.
    snum: The new sprite number to store.

    Notes
    -----
    The mset() function modifies the map data.

    A simple use of mset() is to place or remove objects on the map, such as
    a treasure that the player can pick up. This allows for the level designer
    to set the initial locations of objects.

    In a more sophisticated version of this technique, the program can scan the
    map for objects with mget(), store their locations in a table, then erase
    them from the map data and draw them separately. This may make the objects
    easier to animate or participate in physics simulation.

    Advanced techniques that use mset() include generating levels procedurally,
    or storing very large maps as compressed data and decompressing it into the
    map region as needed. In both cases, once the maps are written to memory,
    the game engine can use map() to draw the level to the screen.
    """
    if 0 <= cel[0] < 128 and 0 <= cel[1] < 64:
        PYCO.map[cel[1]][cel[0]] = snum


def clip(rect = None):
    """Sets the clipping region in the draw state.

    Parameters
    ----------
    rect : The coordinates of the clipping rectangle.

    Notes
    -----
    When the draw state has a clipping rectangle set, all drawing operations
    will not affect any pixels in the graphics buffer outside of this rectangle.
    This is useful for reserving parts of the screen.

    When called without arguments, the function resets the clipping region to be
    the entire screen.
    """
    PYCO.screen.set_clip(rect)


def blit(img, pos = (0, 0), rect = None):
    """Blits an image on the screen.
    
    Parameters
    ----------
    img : The image to blit.
    pos : The position on the screen.
    rect : The portion of the image to blit.
    """
    rect = img.get_rect() if rect is None else rect
    PYCO.screen.blit(img, pos, rect)


def color(color = LIGHT_GRAY):
    """Sets the draw color in the draw state.

    Parameters
    ----------
    color : The color number. Default is 6 (light gray).

    Notes
    -----
    Many graphics functions accept an optional color argument. When 
    this argument is omitted, the current color of the draw state is 
    used by default. The color() function sets this color.

    The color number corresponds to the MINIISH palette, a value between 0 and 15.

    When you provide an explicit color argument to a graphics function,
    MINIISH changes the draw color to that color.

    The previous color is returned when calling color(), allowing it to
    be saved and restored if needed.
    """
    prev_color, PYCO.color = PYCO.color, color
    return prev_color


def camera(offset = (0, 0)):
    """Sets the camera offset in the draw state.

    Parameters
    ----------
    offset : The offset, in pixels, to subtract from future draw coordinates. (default 0, 0)

    Notes
    -----
    Setting a camera offset causes all subsequent draw operations to have
    the offset subtracted from their x and y coordinates. Camera sets the
    origin point for draw functions, and by default it is (0,0).

    The way camera() works is somewhat unintuitive. So, if you might expect
    to use camera(64,64) to put the camera origin in the middle of the screen,
    you'd actually use camera(-64,-64) to move the screen so that its middle is
    in front of the camera. This is probably because camera() sets an screen
    variable that is invisibly used by all draw functions, and in this case,
    the origin changed from (0,0) to (-64,-64).

    Camera offsets can be used to implement screen effects such as parallax
    scrolling (with a different offset per layer) or screen shake (a small
    random offset per frame).
    """
    prev_camera, PYCO.camera = PYCO.camera, offset
    return prev_camera


def cls(color = BLACK):
    """Clears the graphics buffer.

    Parameters
    ----------
    color : A color to use for the background. The default is 0 (black).

    Notes
    -----
    The cls() function clears the graphics buffer, effectively setting 
    every pixel to the color 0. If the color argument is provided,
    that number is used instead.

    It is common (though not required) to call cls() at the beginning
    of the _draw() function as part of the game loop.
    """
    PYCO.screen.fill(PALETTE[color])


def pget(pos):
    """Gets the color value of a pixel on the screen.

    Parameters
    ----------
    pos : The position on the screen.

    Notes
    -----
    The pget() function reads the color value of a pixel from the
    graphics buffer.

    It will read from the buffer even if the buffer has not yet been
    copied to the display.

    It will return 0 (black) if given coordinates outside the range (0-127,0-127).
    """
    if 0 <= pos[0] < 128 and 0 <= pos[1] < 128:
        col = PYCO.screen.get_at(pos)
        return get_palette_exact(col)
    return BLACK


def pset(pos, color = None):
    """Sets a pixel in the graphics buffer.

    Parameters
    ----------
    pos : The position in the graphics buffer.
    color : The color value to set. If unspecified,
        the color of the current draw state will be used.

    Notes
    -----
    The pset() function sets a pixel in the graphics buffer.

    This operation is affected by the draw state.
    """
    PYCO.color = color if color is not None else PYCO.color
    if 0 <= pos[0] < 128 and 0 <= pos[1] < 128:
        PYCO.screen.set_at(pos, PALETTE[PYCO.color])


def rect(rect, color = None):
    """Draws an empty rectangle shape.

    Parameters
    ----------
    rect : The position and dimensions on the screen.
    color : The color of the rectangle border. If omitted,
        the color from the draw state is used. 

    Notes
    -----
    This draws a rectangle shape parallel to the screen borders.
    """
    rect = (rect[0] - PYCO.camera[0], rect[1] - PYCO.camera[1], rect[2], rect[3])
    PYCO.color = color if color is not None else PYCO.color
    pg.draw.rect(PYCO.screen, PALETTE[PYCO.color], rect, 1)


def rectfill(rect, color = None):
    """Draws a filled-in rectangle shape.

    Parameters
    ----------
    rect : The position and dimensions on the screen.
    color : The color of the rectangle border. If omitted, 
        the color from the draw state is used. 

    Notes
    -----
    This draws a rectangle shape parallel to the screen borders.
    """
    rect = (rect[0] - PYCO.camera[0], rect[1] - PYCO.camera[1], rect[2], rect[3])
    PYCO.color = color if color is not None else PYCO.color
    PYCO.screen.fill(PALETTE[PYCO.color], rect)


def sspr(n, pos, s):
    """Draws a sprite on the screen.

    Parameters
    ----------
    n : The sprite number.
    pos : The position on the screen.

    Notes
    -----
    This operation is affected by the draw state.
    """
    pos = (pos[0] - PYCO.camera[0], pos[1] - PYCO.camera[1])
    rect = (int(n % 16) * s[0], int(n / 16) * s[1]) + s
    scale = (int(16 * s[0]), int(16 * s[1]))
    PYCO.screen.blit(pg.transform.scale(PYCO.sprite_sheet, scale), pos, rect)

def spr(n, pos):
    """Draws a sprite on the screen.

    Parameters
    ----------
    n : The sprite number.
    pos : The position on the screen.

    Notes
    -----
    This operation is affected by the draw state.
    """
    pos = (pos[0] - PYCO.camera[0], pos[1] - PYCO.camera[1])
    rect = (int(n % 16) * 8, int(n / 16) * 8, 8, 8)
    PYCO.screen.blit(PYCO.sprite_sheet, pos, rect)


def sget(pos):
    """Gets the color value of a pixel on the sprite sheet.

    Parameters
    ----------
    pos : The position on the sprite sheet.

    Notes
    -----
    This is similar to pget() except instead of the graphics buffer,
    it gets the color value from the sprite sheet. The sprite sheet
    is treated as a single canvas 128 pixels wide and 128 pixels high.

    It will return 0 (black) if given coordinates outside the range (0-127,0-127).
    """
    if 0 <= pos[0] < 128 and 0 <= pos[1] < 128:
        col = PYCO.sprite_sheet.get_at(pos)
        return subr.get_palette_exact(col)
    return BLACK


def sset(pos, color = None):
    """Sets the color value of a pixel on the sprite sheet.

    Parameters
    ----------
    pos : The position on the sprite sheet.
    color : The color value to set. If unspecified,
        the color of the current draw state will be used.

    Notes
    -----
    This is similar to pset() except instead of the graphics buffer, 
    it sets the color value to the sprite sheet. The sprite sheet is
    treated as a single canvas 128 pixels wide and 128 pixels high.
    """
    PYCO.color = color if color is not None else PYCO.color
    if 0 <= pos[0] < 128 and 0 <= pos[1] < 128:
        PYCO.sprite_sheet.set_at(pos, PALETTE[PYCO.color])


def fget(n, f = None):
    """Gets the value of a flag of a sprite.

    Parameters
    ----------
    n : The sprite number.
    f : The flag index (0-7). If omitted, a bit field of all flags is returned.

    Notes
    -----
    Each sprite has eight flags that can be set in the sprite editor
    or by the fset() function. You can use these flags for any purpose.
    One possible purpose is to define "layers" of map tiles, which
    modifies the behavior of the map() function.

    Flags are numbered from 0 to 7, appearing left to right in the sprite editor.

    When fget() is called without a flag index, it returns a number that
    represents all of the flags. This is a bit field where flag 0 is the
    "least significant" bit: flag 0 (leftmost) has a value of 1, flag 1 has
    a value of 2, flag 2 has a value of 4, and so on, up to flag 7 with a
    value of 128.
    """
    if f is None:
        return PYCO.sprite_flags[n]
    else:
        return (PYCO.sprite_flags[n] & (1 << f)) > 0


def fset(n, v, f = None):
    """Sets the value of a flag of a sprite.

    Parameters
    ----------
    n : The sprite number.
    v : The value, either true or false if the flag index is specified, or
        the bit field of all flags if it is not.
    f : The flag index (0-7). If omitted, a bit field of all flags is returned.

    Notes
    -----
    Each sprite has eight flags that can be set in the sprite editor or by the
    fset() function. You can use these flags for any purpose. One possible
    purpose is to define "layers" of map tiles, which modifies the behavior of
    the map() function.

    To set a specific flag, specify the flag index as the second argument, and
    either true or false as the value. Flags are numbered from 0 to 7, appearing
    left to right in the sprite editor.

    When fset() is called without a flag index, it accepts a number that
    represents all of the flags. This is a bit field where flag 0 is the 
    "least significant" bit: flag 0 (leftmost) has a value of 1, flag 1 has
    a value of 2, flag 2 has a value of 4, and so on, up to flag 7 with a
    value of 128.
    """
    if f is None:
        PYCO.sprite_flags[n] = v
    elif v:
        PYCO.sprite_flags[n] |= (1 << f)
    else:
        PYCO.sprite_flags[n] &= ~(1 << f)


def flush():
    """Clears the keyboard buffer.
    
    Notes
    -----
    """
    PYCO.keybuf = []
    pg.event.clear(eventtype = pg.KEYDOWN)


def input():
    """Read a character in the keyboard buffer.

    Notes
    -----
    The input function pops the first character from the keyboard buffer
    or returns None if the bufefr is empty.

    This function translates the character in a Python string or returns hint
    if not a printable character.

    Hints
    -----
    "return" : if enter/return key is pressed.
    "backspace" : if backspace key is pressed.
    """
    if len(PYCO.keybuf) == 0:
        return None
    else:
        event, PYCO.keybuf = PYCO.keybuf[0], PYCO.keybuf[1:]
        if event.key == pg.K_RETURN:
            return "return"
        elif event.key == pg.K_BACKSPACE:
            return "backspace"
        elif event.key == pg.K_ESCAPE:
            return "escape"
        elif event.key == pg.K_UP:
            return "up"
        elif event.key == pg.K_DOWN:
            return "down"
        elif event.key == pg.K_LEFT:
            return "left"
        elif event.key == pg.K_RIGHT:
            return "right"
        elif event.key == pg.K_TAB:
            return " "
        elif event.mod & pg.KMOD_CTRL:
            return "control-" + pg.key.name(event.key)
        else:
            return event.unicode


def print(text, pos = (0, 0), color = None):
    """Prints a string of characters to the screen.

    Parameters
    ----------
    text : The Python string of characters to print.
    pos : The position of the upper left corner to start printing.
    color : The color to use for the text. If unspecified,
        the color of the current draw state will be used.

    Notes
    -----
    The print function writes a line of text to the screen using the MINIISH font.
    
    If only the text argument is supplied, print() uses the camera position and
    draw color from the current draw state to determine where to draw the text,
    and what color to use.
    """
    if text == "":
        return
    PYCO.color = color if color is not None else PYCO.color
    render = subr.render_text(text, PALETTE[PYCO.color])
    pos = (pos[0] - PYCO.camera[0], pos[1] - PYCO.camera[1])
    PYCO.screen.blit(render, pos)


def mcur(n = 0):
    """Selects the mouse cursor.

    Parameters
    ----------
    n : the number of the cursor. Default is 0.
   
    Notes
    -----
    0 : the pointer
    1 : the cross
    2 : the finger

    """
    PYCO.mouse_cursor = n


def mxy():
    """Returns the mouse coordinates.
    
    Notes
    -----
    The coordinates are translated to the screen coordinates.
    """
    return PYCO.mouse_pos


def mbtn(n = 0):
    """Returns the mouse buttons being pressed at this moment.
    
    Notes
    ----
    This function only returns the left button status; True if pressed False otherwise.
    """
    return PYCO.mouse_btn[n]


def flip():
    """Copies the graphics buffer to the screen, then synchronizes to i
    the next frame at 30 frames per second.

    Notes
    -----
    Sketches that use the built-in game loop functions _update() and _draw() do
    not need to call flip(). It can, however, be used to synchronize with
    the 30-frames-per-second draw timer in carts that implement 
    their own custom game loop.
    """
    PYCO.display.blit(pg.transform.scale(PYCO.screen, (512, 512)), (0, 0))            
    pg.display.flip()
    PYCO.clock.tick(30)
