import serial
import threading

from miniish.kernel.process import Process
from miniish.kernel.scheduler import exit
from miniish.kernel import console


class Screen(Process):
    def close(self):
        self.reader_worker_terminated = True
        self.reader_worker.join()
        self.serial.close()
        exit()

    def init(self, args: list[str] = []) -> None:
        self.serial = serial.Serial("/dev/ttyUSB0", 19200, timeout=0)
        self.reader_worker = threading.Thread(target=self.screen_reader_worker)
        self.reader_worker_terminated = False
        self.reader_worker.start()
        self.input_buffer = []
        self.input_buffer_lock = threading.Lock()

    def update(self) -> None:
        c = console.getchar()
        if c is not None:
            if c == "escape":
                self.close()
            elif c == "return":
                self.serial.write(b"\r\n")
            elif c == "backspace":
                self.serial.write(b"\x7f")
            elif len(c) == 1:
                self.serial.write(bytes(c.upper(), "ascii"))

        with self.input_buffer_lock:
            while len(self.input_buffer) > 0:
                c = self.input_buffer.pop(0)
                console.putchar(c)

    def screen_reader_worker(self):
        while not self.reader_worker_terminated:
            b = self.serial.read()
            if len(b) > 0 and b[0] < 128:
                c = b.decode("ascii")
                with self.input_buffer_lock:
                    self.input_buffer.append(c)
