class Logger:
    file_path = ''
    fp = None

    def __init__(self, _file_path):
        self.file_path = _file_path
        self.fp = open(_file_path, "w")

    def log(self, message):
        self.fp.write(message + '\n');