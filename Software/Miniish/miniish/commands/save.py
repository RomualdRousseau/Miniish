from miniish.sketch import *

def save(args, input, output):
    if len(args) != 2 and SKETCH.last_loaded is None:
        output.print("usage: save <filename>")
    else:
        if len(args) == 2:
            SKETCH.last_loaded = args[1]
        for app in APPS:
            app.save("PRE")
        sys.save_cartdrige(SKETCH.last_loaded)
        for app in APPS:
            app.save("POST")
        output.print("saved")