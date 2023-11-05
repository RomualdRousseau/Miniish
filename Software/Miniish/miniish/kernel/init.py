import logging

import pyco
import pyco.sys

from miniish.kernel import disk
from miniish.kernel.scheduler import exec, fork
from miniish.kernel.process import Process


class Init(Process):
    def init(self, args: list[str] = []) -> None:
        process = disk.open("/bin/sh")
        exec(fork(process))

