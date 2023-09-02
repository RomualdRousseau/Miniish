from miniish.sketch import *

def check(args, input, output):
    SKETCH.language.compile(args, output, checkonly=True)
