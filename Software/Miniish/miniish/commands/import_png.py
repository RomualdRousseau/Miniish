from pyco import sys

def import_png(args, input, output):
    if len(args) != 2:
        output.print("usage: import [FILE]")
    else:
        sys.import_png(args[1])
        output.print("imported")