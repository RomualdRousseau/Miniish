from miniish.pyco import *
from miniish.pyco import sys
from miniish.widgets import *
from miniish.code import *
from miniish.sprite import *
from miniish.map import *
from miniish.sound import *
from miniish.music import *
from miniish.console import *

import miniish.languages.python as lang_python
import miniish.languages.asm6502 as lang_asm6502

LANGUAGES = {
        "python" : lang_python,
        "asm6502": lang_asm6502
        }

APPS = [
        CodeEditor(),
        SpriteEditor(),
        MapEditor(),
        SoundEditor(),
        MusicEditor()
        ]

CONSOLE = Console()

class SKETCH: pass

#
# PYCO interface
#

def _init():
    SKETCH.console = CONSOLE
    SKETCH.app = APPS[0]
    SKETCH.update = _update_console
    SKETCH.draw = _draw_console
    SKETCH.console_screen = None
    SKETCH.language = LANGUAGES["asm6502"]
    SKETCH.last_loaded = None
    _init_ui() 


def _update():
    SKETCH.update()


def _draw():
    SKETCH.draw()


def _run():
    program = SKETCH.language.compile()
    if program is None:
        return

    def update_run():
        # Handle inputs
        c = input()
        if c == "escape":
            SKETCH.update = _update_console
            SKETCH.draw = _draw_console
            flush()
        program._update()

    SKETCH.update = update_run
    SKETCH.draw = program._draw
    flush()

    program._init()


#
# Privates
#

def _init_ui():
    # Init APPS selector
    SKETCH.bar = ButtonGroup(-1, (128 - len(APPS) * 8, 0), [
            Button(i, (0, 0), (i * 2, i * 2 + 1), _switch_app) for i in range(len(APPS))    
            ], False, [0])
    # Init all APPS and CONSOLE
    for app in APPS:
        app.language = SKETCH.language
        app.init_ui()
    CONSOLE.init_ui()


def _update_console():
    if not SKETCH.console.update():
        SKETCH.update = _update_app
        SKETCH.draw = _draw_app
        SKETCH.console_screen = sys.screenshot()
        flush()

 
def _draw_console():
    SKETCH.console.draw()


def _update_app():
    SKETCH.bar.update()
    if not SKETCH.app.update():
        SKETCH.update = _update_console
        SKETCH.draw = _draw_console
        if SKETCH.console_screen is not None:
            blit(SKETCH.console_screen)
        flush()


def _draw_app():
    rectfill((0, 0, 128, 8), COLOR_STAT_BG)
    rectfill((0, 8, 128, 113), COLOR_MAIN_BG)
    rectfill((0, 121, 128, 7), COLOR_STAT_BG)
    SKETCH.bar.draw()
    SKETCH.app.draw()


def _switch_app(self):
    SKETCH.app = APPS[self.id]
    flush()
