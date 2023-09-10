from miniish.editor import Editor
from miniish.sketch import Sketch
from miniish.commands.load import Load
from miniish.commands.save import Save
from miniish.commands.shutdown import Shutdown
from miniish.commands.run import Run
from miniish.commands.lang import Lang
from miniish.commands.clrscr import Clrscr
from miniish.commands.screen import Screen

COMMANDS = {
    "sketch": Sketch(),
    "editor": Editor(),
    # "import": import_png,
    # "export": export_png,
    "load": Load(),
    "save": Save(),
    "shutdown": Shutdown(),
    "run": Run(),
    # "check": check,
    "lang": Lang(),
    "clear": Clrscr(),
    "screen": Screen(),
}
