"""
Various system routines

"""

import csv

from .globals import *
from . import pyco
from . import subr
from . import synth
from . import mouse
from . import cartdrige


def get_sources():
    return PYCO.sources


def set_sources(sources):
    PYCO.sources = sources


def get_music():
    return PYCO.music

def get_sound(n):
    return PYCO.sounds[n]


def set_sound(n, sound):
    PYCO.sounds[n] = sound


def load_cartdrige(file_name):
    """Load cartdrige data.
    
    Parameters
    ----------
    file_name : file name to load the data from.
    """
    file_name = file_name + ".miniish" if ".miniish" not in file_name else file_name 
    PYCO.sources = []
    def callback(headers, text):
        part = headers["Content-type"]
        if part == "text":
            PYCO.sources.append(text)
        elif part == "spritesheet":
            reader = csv.reader(text)
            for i, row in enumerate(reader):
                for j, pixel in enumerate(row):
                    pyco.sset((j, i), int(pixel))
        elif part == "spriteflag":
            reader = csv.reader(text)
            for i, row in enumerate(reader):
                for j, flag in enumerate(row):
                    pyco.fset(i * 16 + j, int(flag))
        elif part == "map":
            reader = csv.reader(text)
            for i, row in enumerate(reader):
                for j, tile in enumerate(row):
                    pyco.mset((j, i), 0 if int(tile) < 0 else int(tile))
        elif part == "sound":
            reader = csv.reader(text)
            for i, row in enumerate(reader):
                speed = 1
                for j, pack in enumerate(row):
                    if j == 0:
                        speed = int(pack)
                    else:
                        pack = int(pack)
                        p, w, v, e = (pack >> 9) & 63, (pack >> 6) & 7, (pack >> 3) & 7, (pack >> 0) & 7
                        sound = PYCO.sounds[int(i)]
                        sound[int(j) - 1] = (p, w, v, e, speed)
                        PYCO.sounds[int(i)] = sound
        elif part == "music":
            reader = csv.reader(text)
            for i, row in enumerate(reader):
                for j, sound in enumerate(row):
                    PYCO.music[i][j] = int(sound)
    with cartdrige.CartdrigeReader(file_name) as reader:
        reader.read(callback)


def save_cartdrige(file_name):
    """Save cartdrige data

    Parameters
    ----------
    file_name : file name to save data to.
    """
    file_name = file_name + ".miniish" if ".miniish" not in file_name else file_name 
    with cartdrige.CartdrigeWriter(file_name) as writer:
        writer.header("Name", file_name)
        writer.header("Author", "Unknown")
        writer.body_begin()

        for text in PYCO.sources:
            if len(text) > 0:
                writer.body_part("text", text)

        def write_spritesheet(txtfile):
            writer = csv.writer(txtfile, lineterminator='\n')
            for i in range(128):
                row = []
                for j in range(128):
                    p = pyco.sget((j, i))
                    row.append(p)
                writer.writerow(row)
        writer.body_part_with_cb("spritesheet", write_spritesheet)

        def write_spriteflag(txtfile):
            writer = csv.writer(txtfile, lineterminator='\n')
            for i in range(16):
                row = []
                for j in range(16):
                    row.append(pyco.fget(i * 16 + j))
                writer.writerow(row)
        writer.body_part_with_cb("spriteflag", write_spriteflag)

        def write_map(txtfile):
            writer = csv.writer(txtfile, lineterminator='\n')
            for i in range(64):
                row = []
                for j in range(128):
                    row.append(pyco.mget((j, i)))
                writer.writerow(row)
        writer.body_part_with_cb("map", write_map)

        def write_sound(txtfile):
            writer = csv.writer(txtfile, lineterminator='\n')
            for i in range(64):
                s = PYCO.sounds[i]
                row = []
                speed = s[0][4]
                row.append(speed)
                for j in range(32):
                    p, w, v, e, _ = s[j]
                    pack = ((p & 63) << 9) | ((w & 7) << 6) | ((v & 7) << 3) | ((e & 7) << 0)
                    row.append(pack)
                writer.writerow(row)
        writer.body_part_with_cb("sound", write_sound)

        def write_music(txtfile):
            writer = csv.writer(txtfile, lineterminator='\n')
            for i in range(64):
                m = PYCO.music[i]
                row = []
                for j in range(4):
                    row.append(m[j])
                writer.writerow(row)
        writer.body_part_with_cb("music", write_music)

        writer.body_end()


def debug(s):
    print(s)

def load_png(file_name):
    """Loads an image from the assets folder. 
    
    Parameters
    ----------
    file_name : The file name of the image to load.

    Notes
    -----
    This function excepts the image to be in PNG format and will add automatically
    the .png extension.
    """
    return subr.load_asset_png(file_name)


def screenshot():
    """Takes a screenshot of the screen.
    
    Notes
    -----
    This functions returns the image of the screen. It can used with the blit
    funtions.
    """
    sc = pg.Surface((128, 128))
    sc.blit(PYCO.screen, (0, 0))
    return sc


def use(sprite_sheet = None):
    """Selects the sprite sheet used by the current draw state.

    Parameters
    ----------
    sprite_sheet : The sprite sheet to use; GAME or SYSTEM. Default is GAME.

    Notes
    -----
    MINIISH contains 2 sprite sheets, one for the GAME and one for the SYSTEM
    itself to draw the elements of the interface. This function update the cyurrent
    draw state to use one of these sprite sheets.

    If no argument is supplied, the GAME sprite sheet will be used by the current
    draw state.
    """
    sprite_sheet = "GAME" if sprite_sheet is None else sprite_sheet
    if sprite_sheet == "SYSTEM":
        PYCO.sprite_sheet = PYCO.system_sheet
    else:
        PYCO.sprite_sheet = PYCO.game_sheet


def import_png(file_path):
    """Imports a PNG image file as sprite data.

    Parameters
    ----------
    file_path : The .png graphics file to import. 

    Notes
    -----
    This command imports a specially formatted PNG image file to be the sprite
    sheet for the current cartridge. The file must be 128 pixels wide, 128 pixels
    tall, and use the PICO-8 palette (otherwise the file will be clipped, and the
    colors will be set to the closest PICO-8 color).

    To edit the sprite sheet in an external graphics editing program, use the export
    command to make a PNG image file with the correct properties, edit it in the
    external editor, then use the import command to update the cartridge. You can
    set up the palette in your editor by placing some of each color on the sprite
    sheet within PICO-8, then sampling the exported file.
    """
    file_path = file_path + ".png" if ".png" not in file_path else file_path
    PYCO.game_sheet = pg.image.load(file_path).convert_alpha()


def export_png(file_path):
    """Exports sprite data as PNG image file.
    
    Parameters
    ----------
    file_path : The .png graphics file to export.

    Notes
    -----
    This command can be used to generate a PNG image of the sprite sheet.

    Exported files are created in the current working directory.
    """
    file_path = file_path + ".png" if ".png" not in file_path else file_path 
    pg.image.save(PYCO.game_sheet, file_path)


def shutdown():
    """Quits MINIISH.
    
    Notes
    -----
    The shutdown command closes the MINIISH.

    Caution: MINIISH will not warn you if you have unsaved changes. Be sure to
    save your work before quitting.
    """
    PYCO.running =  False


def set_callbacks(init_, update_, draw_):
    """Sets the game loop callbacks.

    Parameters
    ----------
    init_ : The _init() function is called by MINIISH to initialize a sketch.
    update_ : The first part of a game loop is the update_() function.
    draw_ : The _draw() function is the second part of the game loop.

    Notes
    -----
    See run() for details about the game loop.

    This function is internally used and should nver be called by a sketch.
    """
    PYCO.init = init_
    PYCO.update = update_
    PYCO.draw = draw_


def run():
    """Runs the sketch.

    Notes
    -----
    This function initializes MINIISH engine and start the game loop.

    The game loop is the mechanism that drives a game's logic and
    rendering processes. Because each cycle of the loop updates the display,
    it is important for the loop to run at regular intervals to keep the
    animation smooth and the game feeling responsive to user input.

    MINIISH has a built-in game loop that runs 30 times per second. You use
    this in your code by defining three functions: _init(), _update(), and _draw().

    This function is internally used and should nver be called by a sketch.
    """
    #pg.mixer.pre_init(frequency = synth.SAMPLING_RATE, size = -8, channels = 1)
    pg.init()
    #pg.mixer.init()
    pg.key.set_repeat(500, 33)
    pg.mouse.set_visible(False)
    
    PYCO.display = pg.display.set_mode((1024, 1024))
    PYCO.clock = pg.time.Clock()
    PYCO.screen = pg.Surface((128, 128))
    PYCO.font = subr.load_asset_png("miniish-font")
    PYCO.game_sheet = subr.load_asset_png("miniish-default-spritesheet") 
    PYCO.system_sheet = subr.load_asset_png("miniish-system-spritesheet")
    PYCO.sprite_sheet = subr.PYCO.game_sheet
    PYCO.sprite_flags = [0 for i in range(256)]
    PYCO.map = [[0 for j in range(128)] for i in range(64)]
    PYCO.color = LIGHT_GRAY
    PYCO.camera = (0, 0)
    PYCO.mouse_cursor = 0
    PYCO.mouse_btn = (False, False, False)
    PYCO.mouse_pos = (0, 0)
    PYCO.mouse_mask = None
    PYCO.mouse_mask_pos = (0, 0)
    PYCO.mouse_wheel = (0, 0)
    PYCO.keybuf = []
    PYCO.sounds = [[(0, 0, 0, 0, 1) for j in range(32)] for i in range(64)]
    PYCO.music = [[-1, -1, -1, -1] for i in range(64)]
    PYCO.sources= []
    PYCO.running = True

    if PYCO.init is not None:
        PYCO.init()

    while not subr.is_done(pg.event.get()):
        mouse.update()
        PYCO.update()
        PYCO.draw()
        mouse.draw()
        pyco.flip()

    #pg.mixer.quit()
    pg.quit()

