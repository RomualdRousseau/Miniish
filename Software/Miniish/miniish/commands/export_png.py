from pyco import sys

def export_png(args, input, output):
    if len(args) != 2:
        output.print("usage: export [FILE]")
    else:
        sys.export_png(args[1])
        output.print("exported")