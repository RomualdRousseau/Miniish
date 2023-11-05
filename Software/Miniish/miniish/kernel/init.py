import logging

import pyco
import pyco.sys

from miniish.kernel import virtfs
from miniish.kernel.scheduler import exec, fork
from miniish.kernel.process import Process


class Init(Process):
    def init(self, args: list[str] = []) -> None:
        process = virtfs.open("/bin/sh")
        exec(fork(process))

