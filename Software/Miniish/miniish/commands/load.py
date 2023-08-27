from miniish.sketch import *

def load(args, out):
    if len(args) != 2:
        out.print("usage: load <filename>")
    else:
        SKETCH.last_loaded = args[1]
        for app in APPS:
            app.load("PRE")
        if sys.load_cartdrige(SKETCH.last_loaded):
            for app in APPS:
                app.load("POST")
            out.print("loaded")
        else:
            out.print("file not found")