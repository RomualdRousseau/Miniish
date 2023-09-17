import threading

from miniish.kernel import console
from miniish.kernel.scheduler import exit
from miniish.languages.asm6502 import compile, upload


class Program:
    def __init__(self, verify: bool = False) -> None:
        self.verify = verify
        self.worker = None

    def _init(self) -> None:
        self.worker = threading.Thread(target=self._worker)
        self.worker.start()

    def _update(self) -> None:
        if self.worker is None or not self.worker.is_alive():
            exit()

    def _draw(self) -> None:
        console.render()

    def _worker(self) -> None:
        compile.compile(self.verify)
        if not self.verify:
            upload.upload()
