import logging

BOUNDARY = "------1234567890"

class CartdrigeWriter:
    def __init__(self, file_name):
        self.txtfile = open(file_name, "w")

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, ex_trace):
        self.txtfile.close()

    def header(self, key, value):
        self.txtfile.write(f"{key}: {value}\n")

    def body_begin(self):
        self.txtfile.write(f"Boundary: {BOUNDARY}\n\n")

    def body_part(self, part, text):
        self.txtfile.write(f"{BOUNDARY}\n")
        self.txtfile.write(f"Content-type: {part}\n\n")
        for line in text:
            self.txtfile.write(line.rstrip() + '\n')

    def body_part_with_cb(self, part, callback):
        self.txtfile.write(f"{BOUNDARY}\n")
        self.txtfile.write(f"Content-type: {part}\n\n")
        callback(self.txtfile)

    def body_end(self):
        self.txtfile.write(f"{BOUNDARY}\n")

    
class CartdrigeReader:
    def __init__(self, file_name):
        self.txtfile = open(file_name)

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, ex_trace):
        self.txtfile.close()

    def read(self, callback):
        state = 0
        headers = {}
        text = []
        for line in self.txtfile:
            line = line.rstrip()
            if state == 0:
                if line == "":
                    state = 1
                else:
                    key, value = line.split(": ")
                    headers[key] = value
            elif state == 1:
                if line == headers["Boundary"]:
                    state = 2
                else:
                    logging.error("Boundary excepted")
            elif state == 2:
                if line == "":
                    text = []
                    state = 3
                else:
                    key, value = line.split(": ")
                    headers[key] = value
            elif state == 3:
                if line == headers["Boundary"]:
                    callback(headers, text)
                    state = 2
                else:
                    text.append(line)
