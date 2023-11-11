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
from miniish.user.procstat import ProcStat

COMMANDS = {
    ".editor": Editor("editor"),
    ".sketch": Sketch("sketch"),
    "sh": Shell("sh"),
    "run": Alias("run", "/bin/.sketch"),
    "upload": Alias("upload", "/bin/.sketch"),
    "verify": Alias("verify", "/bin/.sketch", ["verify"]),
    "import": ImportPng("import"),
    "export": ExportPng("export"),
    "load": Load("load"),
    "save": Save("save"),
    "shutdown": Shutdown("shutdown"),
    "lang": Lang("lang"),
    "clear": Clrscr("clear"),
    "screen": Screen("screen"),
    "ls": ListDir("ls"),
    "ps": ProcStat("ps")
}
