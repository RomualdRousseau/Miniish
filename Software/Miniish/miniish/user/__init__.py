from miniish.editor import Editor
from miniish.user.sketch import Sketch
from miniish.user.alias import Alias
from miniish.user.shell import Shell
from miniish.user.load import Load
from miniish.user.save import Save
from miniish.user.shutdown import Shutdown
from miniish.user.lang import Lang
from miniish.user.clrscr import Clrscr
from miniish.user.screen import Screen
from miniish.user.export_png import ExportPng
from miniish.user.import_png import ImportPng
from miniish.user.listdir import ListDir

COMMANDS = {
    ".editor": Editor(),
    ".sketch": Sketch(),
    "sh": Shell(),
    "run": Alias("/bin/.sketch"),
    "upload": Alias("/bin/.sketch"),
    "verify": Alias("/bin/.sketch", ["verify"]),
    "import": ImportPng(),
    "export": ExportPng(),
    "load": Load(),
    "save": Save(),
    "shutdown": Shutdown(),
    "lang": Lang(),
    "clear": Clrscr(),
    "screen": Screen(),
    "ls": ListDir()
}
