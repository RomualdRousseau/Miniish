from miniish.kernel.process import Process


def open(path: str) -> Process | None:
    p = get_process(path)
    if p is not None:
        return p

    sketch = get_process("sketch")
    if sketch is not None:
        if sketch.load(path):
            return sketch

    return None


def get_process(path: str) -> Process | None:
    from miniish.commands import COMMANDS
    return COMMANDS.get(path)
