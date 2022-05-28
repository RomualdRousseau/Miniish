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


def make_(args, out):
    for i, text in enumerate(PYCO.sources):
        if len(text) > 0:
            line = text[0]
            file_name = f"buffer{i}.i"
            if i == 0:
                file_name = "main.s"
            elif line[0] == ';':
                file_name = line[1:].strip()
            with open("work/" + file_name, "w") as writer:
                for line in text:
                    writer.write(line + "\n")
    
    with open("work/sprites.dat", "wb") as writer:
        for y in range(16):
            for x in range(16):
                for sy in range(8):
                    for sx in range(8):
                        pixel = pyco.sget((x * 8 + sx, y * 8 + sy))
                        if sx % 2 == 0:
                            acc = pixel << 4
                        else:
                            acc = acc | pixel
                            writer.write(b'%c' % acc)
    
    with open("work/map.dat", "wb") as writer:
        for i in range(32):
            for j in range(32):
                writer.write(b'%c' % pyco.mget((j, i)))
    
    if len(args) == 1:
        os.system("make -C work")
    else:
        os.system("make -C work " + args[1])
    
    out.print("done")


__all__ = {
        "import" : import_,
        "export": export_,
        "load": load_,
        "save": save_,
        "shutdown": shutdown_,
        "run": run_,
        "lang": lang_,
        "make": make_
        }
