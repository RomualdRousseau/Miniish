from miniish.sketch import *

def lang(args, out):
    if len(args) != 2:
        out.print("usage: lang <python | asm6502>")
    else:
        SKETCH.language = LANGUAGES[args[1]]
        for app in APPS:
            app.language = SKETCH.language