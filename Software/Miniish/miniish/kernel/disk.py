import os

from miniish.commands import COMMANDS
from miniish.kernel.process import Process

FS = [
    (0, 0, "d", "", ""),
    (1, 0, "d", "bin", "bin"),
    (2, 0, "l", "sketches", "sketches"),
]


def start() -> None:
    print("Disk: preparing disk...")
    _add_nodes(FS, FS[1], COMMANDS.keys())
    print("Disk: ok")


def get_real_path(path: str) -> str:
    try:
        node, fs = _find_node(path)
        return _get_real_path(fs, node)
    except:
        parent = os.path.dirname(path)
        file = os.path.relpath(path, parent)
        node, fs = _find_node(parent)
        return os.path.join(_get_real_path(fs, node), file)


def listdir(path: str = os.path.sep) -> list[str]:
    node, fs = _find_node(path)
    if node[2] in ("d", "l"):
        return list(
            map(_format_node, filter(lambda x: x[0] > 0 and x[1] == node[0], fs))
        )
    return [node[3]]


def exists(path: str) -> bool:
    try:
        _find_node(path)
        return True
    except:
        return False


def open(path: str) -> Process:
    node, _ = _find_node(path)
    p = COMMANDS.get(node[3])
    if p is not None:
        return p
    return COMMANDS["sketch"]


def _get_real_path(fs, node):
    return os.path.abspath(os.path.join(fs[node[1]][4], node[4]))


def _find_node(path):
    segments = path.strip(os.path.sep).split(os.path.sep)

    # Augment the FS with links

    fs = FS.copy()
    for node in filter(lambda x: x[2] == "l", FS):
        _add_nodes(fs, node, os.listdir(node[4]))

    # Find the node

    node = fs[0]
    for segment in segments:
        node = next(filter(lambda x: x[1] == node[0] and x[3] == segment, fs))
    return node, fs


def _add_nodes(fs, parent, files):
    inode = len(fs)
    for file in files:
        fs.append((inode, parent[0], "f", file, file))
        inode = inode + 1


def _format_node(node):
    if node[2] in ("d", "l"):
        return node[3] + os.path.sep
    return node[3]
