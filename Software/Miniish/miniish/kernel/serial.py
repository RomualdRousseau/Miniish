import serial
import threading


class SERIAL:
    serial: serial.Serial
    reader_worker: threading.Thread
    reader_worker_terminated: bool
    input_buffer: list[str]
    input_buffer_lock: threading.Lock

    def __enter__(self):
        return SERIAL

    def __exit__(self, *args):
        close()


def open(port: str, baudrate: int = 19200) -> SERIAL:
    SERIAL.serial = serial.Serial(port, baudrate, timeout=0)
    SERIAL.reader_worker = threading.Thread(target=_reader_worker)
    SERIAL.reader_worker_terminated = False
    SERIAL.reader_worker.start()
    SERIAL.input_buffer = []
    SERIAL.input_buffer_lock = threading.Lock()
    return SERIAL()


def close() -> None:
    SERIAL.reader_worker_terminated = True
    SERIAL.reader_worker.join()
    SERIAL.input_buffer = []
    SERIAL.serial.close()


def read() -> str | None:
    with SERIAL.input_buffer_lock:
        if len(SERIAL.input_buffer) > 0:
            data = "".join(SERIAL.input_buffer)
            SERIAL.input_buffer = []
            return data
        return None


def write(s: str) -> None:
    SERIAL.serial.write(bytes(s, "ascii"))


def _reader_worker() -> None:
    while not SERIAL.reader_worker_terminated:
        b = SERIAL.serial.read()
        if len(b) > 0 and b[0] < 128:
            c = b.decode("ascii")
            with SERIAL.input_buffer_lock:
                SERIAL.input_buffer.append(c)
