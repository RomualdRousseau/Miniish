from pyco import sys

def export_png(args, out):
    if len(args) != 2:
        out.print("usage: export [FILE]")
    else:
        sys.export_png(args[1])
        out.print("exported")