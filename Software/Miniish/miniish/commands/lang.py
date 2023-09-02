from miniish.sketch import *

def lang(args, input, output):
    if len(args) != 2:
        output.print("usage: lang <python | asm6502>")
    else:
        SKETCH.language = LANGUAGES[args[1]]
        for app in APPS:
            app.language = SKETCH.language