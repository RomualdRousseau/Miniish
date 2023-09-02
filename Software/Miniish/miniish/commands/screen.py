import serial
import threading

from miniish.constants import PROMPT
from miniish.sketch import SKETCH, _update_console

def screen(args, input, output):
    Screen(input, output, "/dev/ttyUSB0", 19200)

class Screen:
     
    def __init__(self, input, output, port, baudrate):
        self.input = input
        self.output = output
        self.serial = serial.Serial(port, baudrate, timeout=0)
        self.reader_worker = threading.Thread(target=self.screen_reader_worker)
        self.reader_worker_terminated = False
        self.reader_worker.start()
        self.input_buffer = []
        self.input_buffer_lock = threading.Lock()
        
        self.output.disable_prompt()
        SKETCH.update = self.update
        
    def close(self):
        self.reader_worker_terminated = True
        self.reader_worker.join()
        self.serial.close()
        
        self.output.enable_prompt()
        SKETCH.update = _update_console
        
    def update(self):
        c = self.input.getchar()
        if c is not None:
            if c == "escape":
                self.close()
                return False
            elif c == "return":
                self.serial.write(b"\r\n")
            elif c == "backspace":
                self.serial.write(b"\x7f")
            elif len(c) == 1:
                self.serial.write(bytes(c.upper(), "ascii"))
    
        with self.input_buffer_lock:
            while len(self.input_buffer) > 0:
                c = self.input_buffer.pop(0)
                self.output.putchar(c)
    
        return True

    def screen_reader_worker(self):
        while not self.reader_worker_terminated:
            b = self.serial.read()
            if len(b) > 0 and b[0] < 128:
                c = b.decode("ascii")
                with self.input_buffer_lock:
                    self.input_buffer.append(c)
