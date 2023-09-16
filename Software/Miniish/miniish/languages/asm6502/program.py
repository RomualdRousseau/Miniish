import threading

from miniish.kernel import console
from miniish.kernel.scheduler import exit
from miniish.languages.asm6502 import compile, upload


class Program:
    def __init__(self, verify: bool = False):
        self.verify = verify
        self.worker = None

    def _init(self):
        self.worker = threading.Thread(target=self._worker)
        self.worker.start()

    def _update(self):
        if self.worker is None or not self.worker.is_alive():
            exit()

    def _draw(self):
        console.render()

    def _worker(self):
        compile.compile(self.verify)
        if not self.verify:
            upload.upload()
