from pyco import sys

def import_png(args, out):
    if len(args) != 2:
        out.print("usage: import [FILE]")
    else:
        sys.import_png(args[1])
        out.print("imported")