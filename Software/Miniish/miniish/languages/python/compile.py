from pyco.globals import PYCO


def compile(verify: bool = False) -> None: 
    with open("target/__init__.py", "w"):
        pass

    with open("target/program.py", "w") as srcfile:
        srcfile.write("from pyco import *\n\n")
        for source in PYCO.sources:  # type: ignore
            for line in source:
                srcfile.write(line.rstrip() + "\n")
