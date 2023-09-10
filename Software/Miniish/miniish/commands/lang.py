from miniish.kernel import console
from miniish.kernel.process import Process
from miniish.kernel.scheduler import exit
from miniish.languages import get_current_language, change_language


class Lang(Process):
    def init(self, args: list[str] = []) -> None:
        if len(args) != 2:
            console.print("usage: lang <python | asm6502>")
        else:
            change_language(args[1])
            console.print("Language: " + get_current_language().get_name())
        exit()
