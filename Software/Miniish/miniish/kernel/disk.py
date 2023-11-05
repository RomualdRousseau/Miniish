import os

from miniish.user import COMMANDS
from miniish.kernel.process import Process

VIRTFS = [
    (0, 0, "d", "", ""),
    (1, 0, "d", "bin", "bin"),
    (2, 0, "l", "sketches", "sketches"),
]


def init() -> None:
    print("Disk: preparing disk...")
    _add_nodes(VIRTFS[1], COMMANDS.keys())
    _add_nodes(VIRTFS[2], os.listdir(VIRTFS[2][4]))
    print("Disk: ok")


def get_real_path(path: str) -> str:
    return _get_real_path(_find_node(path))


def listdir(path: str = os.path.sep) -> list[str]:
    node = _find_node(path)
    if node[2] in ("d", "l"):
        return list(
            map(_format_node, filter(lambda x: x[0] > 0 and x[1] == node[0], VIRTFS))
        )
    return [node[3]]


def exists(path: str) -> bool:
    try:
        _find_node(path)
        return True
    except:
        return False


def create(path: str) -> Process:
    if not exists(path):
        parent = os.path.dirname(path)
        file = os.path.relpath(path, parent)
        node = _find_node(parent)
        _add_nodes(node, [file])
    return COMMANDS["sketch"]


def open(path: str) -> Process:
    node = _find_node(path)
    p = COMMANDS.get(node[3])
    if p is not None:
        return p
    return COMMANDS["sketch"]


def _get_real_path(node):
    parent = VIRTFS[node[1]]
    return os.path.abspath(os.path.join(parent[4], node[4]))


def _find_node(path):
    segments = path.strip(os.path.sep).split(os.path.sep)
    node = VIRTFS[0]
    for segment in segments:
        node = next(filter(lambda x: x[1] == node[0] and x[3] == segment, VIRTFS))
    return node


def _add_nodes(parent, files):
    inode = len(VIRTFS)
    for file in files:
        VIRTFS.append((inode, parent[0], "f", file, file))
        inode = inode + 1


def _format_node(node):
    if node[2] in ("d", "l"):
        return node[3] + os.path.sep
    return node[3]
