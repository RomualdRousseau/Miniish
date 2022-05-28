import os

from miniish.pyco import *
from miniish.pyco import sys
from miniish.sketch import *
from miniish.sketch import _run


def import_(args, out):
    if len(args) != 2:
        out.print("usage: import [FILE]")
    else:
        sys.import_png(args[1])
        out.print("imported")


def export_(args, out):
    if len(args) != 2:
        out.print("usage: export [FILE]")
    else:
        sys.export_png(args[1])
        out.print("exported")


def load_(args, out):
    if len(args) != 2:
        out.print("usage: load <filename>")
    else:
        SKETCH.last_loaded = args[1]
        for app in APPS:
            app.load("PRE")
        sys.load_cartdrige(SKETCH.last_loaded)
        for app in APPS:
            app.load("POST")
        out.print("loaded")


def save_(args,out):
    if len(args) != 2 and SKETCH.last_loaded is None:
        out.print("usage: save <filename>")
    else:
        for app in APPS:
            app.save("PRE")
        sys.save_cartdrige(args[1] if len(args) == 2 else SKETCH.last_loaded)
        for app in APPS:
            app.save("POST")
        out.print("saved")


def shutdown_(args, out):
    out.print("bye")
    sys.shutdown()


def run_(args, out):
    _run()


def lang_(args, out):
    if len(args) != 2:
        out.print("usage: lang <python | asm6502>")
    else:
        SKETCH.language = LANGUAGES[args[1]]
        for app in APPS:
            app.language = SKETCH.language


__all__ = {
        "import" : import_,
        "export": export_,
        "load": load_,
        "save": save_,
        "shutdown": shutdown_,
        "run": run_,
        "lang": lang_
        }
