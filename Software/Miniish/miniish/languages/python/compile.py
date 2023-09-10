from importlib import reload

from pyco.globals import PYCO


def compile(checkonly = False):

    # Compile

    with open("program.py", "w") as srcfile:
        srcfile.write("from pyco import *\n\n")
        for source in PYCO.sources:  # type: ignore
            for line in source:
                srcfile.write(line.rstrip() + '\n')

    # Load

    import program  # type: ignore
    program = reload(program)
    return program
