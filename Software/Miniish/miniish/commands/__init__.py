from .import_png import *
from .export_png import *
from .load import *
from .save import *
from .shutdown import *
from .run import *
from .check import *
from .lang import *
from .screen import *

COMMANDS = {
    "import": import_png,
    "export": export_png,
    "load": load,
    "save": save,
    "shutdown": shutdown_,
    "run": run_,
    "check": check,
    "lang": lang,
    "screen": screen
}