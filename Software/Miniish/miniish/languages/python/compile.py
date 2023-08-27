from pyco import *

from importlib import reload


def compile(args, out, checkonly = False):

    # Compile

    with open("program.py", "w") as srcfile:
        srcfile.write("from pyco import *\n\n")
        for source in PYCO.sources:
            for line in source:
                srcfile.write(line.rstrip() + '\n')

    # Load

    import program
    program = reload(program)
    
    return program
