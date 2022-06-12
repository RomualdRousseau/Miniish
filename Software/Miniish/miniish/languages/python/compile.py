from importlib import reload
from miniish.pyco import *

def compile(args, out):

    # Compile

    with open("program.py", "w") as srcfile:
        srcfile.write("from miniish.pyco import *\n\n")
        for source in PYCO.sources:
            for line in source:
                srcfile.write(line.rstrip() + '\n')

    # Load

    import program
    program = reload(program)
    
    return program
