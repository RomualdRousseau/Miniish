from miniish.editor import Editor
from miniish.sketch import Sketch
from miniish.commands.load import Load
from miniish.commands.save import Save
from miniish.commands.shutdown import Shutdown
from miniish.commands.run import Run
from miniish.commands.lang import Lang
from miniish.commands.clrscr import Clrscr
from miniish.commands.screen import Screen
from miniish.commands.verify import Verify
from miniish.commands.export_png import ExportPng
from miniish.commands.import_png import ImportPng
from miniish.commands.listdir import ListDir

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
