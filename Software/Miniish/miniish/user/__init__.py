from miniish.editor import Editor
from miniish.user.sketch import Sketch
from miniish.user.load import Load
from miniish.user.save import Save
from miniish.user.shutdown import Shutdown
from miniish.user.run import Run
from miniish.user.lang import Lang
from miniish.user.clrscr import Clrscr
from miniish.user.screen import Screen
from miniish.user.verify import Verify
from miniish.user.export_png import ExportPng
from miniish.user.import_png import ImportPng
from miniish.user.listdir import ListDir

COMMANDS = {
    "sketch": Sketch(),
    "editor": Editor(),
    "import": ImportPng(),
    "export": ExportPng(),
    "load": Load(),
    "save": Save(),
    "shutdown": Shutdown(),
    "run": Run(),
    "upload": Run(),
    "verify": Verify(),
    "lang": Lang(),
    "clear": Clrscr(),
    "screen": Screen(),
    "ls": ListDir()
}
