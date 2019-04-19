import os
from datetime import datetime

class FileUtil:

    def __init__(self, filename):
        self.filename = filename
        self.create_project(filename)

    def create_project(self, filename):
        project_path = self.get_file_path(filename)

        self.create_new_directory(project_path, 'images')
        self.create_new_directory(project_path, 'logs')

        self.create_file('%s/%s/%s' % (project_path, 'logs', 'default.log'))
        self.create_file('%s' % (filename))

    def create_file(self, filename):
        try:
            if not os.path.exists(filename):
                f = open(filename, 'w+')
                f.close()
        except Exception as e:
            # log error
            print(e)

    def create_new_directory(self, project_path, directory):
        try:
            if not os.path.exists( '%s/%s' % (project_path, directory) ):
                os.makedirs('%s/%s' % (project_path, directory))
        except Exception as e:
            # log error
            print(e)

    def get_file_path(self, filename):
        splitted_filename_path = filename.split('/')
        return '/'.join(splitted_filename_path[:-1])

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


class DateUtil:
    def __init__(self):
        print('__init__')

    def datetime_to_format_string(self, input, output):
        datetime_obj = datetime.strptime('%s' % input['datetime'], input['format'])
        return datetime_obj.strftime(output['format'])
