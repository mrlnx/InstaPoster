import os

class FileUtil:

    def __init__(self, filename):
        self.filename = filename

    def last_modified(self):
        return os.path.getmtime(self.filename);

class LoggerUtil:

    def __init__(self, filename):
        self.filename = filename

        with open(self.filename, 'r') as self.file_read:
            self.file_read_content = self.file_read.read()
            self.file_read_lines = self.file_read.readlines()

    def read(self):
        return self.file_read

    def read_lines(self):
        return self.file_read_lines

    def write_new_line(self, content):
        self.file_read_lines.append(content + '\n')
        with open(self.filename, 'w') as self.file_write:
            self.file_write.writelines(self.file_read_lines)
