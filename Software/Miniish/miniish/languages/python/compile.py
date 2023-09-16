from importlib import reload

from pyco.globals import PYCO


def compile(verify = False):

    # Compile
    
    with open("target/__init__.py", "w"):
        pass

    with open("target/program.py", "w") as srcfile:
        srcfile.write("from pyco import *\n\n")
        for source in PYCO.sources:  # type: ignore
            for line in source:
                srcfile.write(line.rstrip() + '\n')

    # Load

    from target import program  # type: ignore
    program = reload(program)  # type: ignore
    return program
