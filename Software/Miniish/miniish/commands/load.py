from miniish.sketch import *

def load(args, input, output):
    if len(args) != 2:
        output.print("usage: load <filename>")
    else:
        SKETCH.last_loaded = args[1]
        for app in APPS:
            app.load("PRE")
        if sys.load_cartdrige(SKETCH.last_loaded):
            for app in APPS:
                app.load("POST")
            output.print("loaded")
        else:
            output.print("file not found")