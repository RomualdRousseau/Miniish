from miniish.kernel.scheduler import exit
from miniish.kernel.process import Process
from miniish.languages import get_current_language


class Verify(Process):
    def init(self, args: list[str] = []) -> None:
        get_current_language().compile(verify=True)
        exit()