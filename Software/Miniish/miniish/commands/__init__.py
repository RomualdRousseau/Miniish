from miniish.editor import Editor
from miniish.sketch import Sketch
from miniish.commands.load import Load
from miniish.commands.save import Save
from miniish.commands.shutdown import Shutdown
from miniish.commands.run import Run
from miniish.commands.lang import Lang
from miniish.commands.clrscr import Clrscr
from miniish.commands.screen import Screen
from miniish.commands.check import Check
from miniish.commands.export_png import ExportPng
from miniish.commands.import_png import ImportPng

COMMANDS = {
    "sketch": Sketch(),
    "editor": Editor(),
    "import": ImportPng(),
    "export": ExportPng(),
    "load": Load(),
    "save": Save(),
    "shutdown": Shutdown(),
    "run": Run(),
    "check": Check(),
    "lang": Lang(),
    "clear": Clrscr(),
    "screen": Screen(),
}
