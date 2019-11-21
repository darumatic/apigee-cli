import os
import sys
import zipfile

class IO:

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value):
        self._kwargs = value

    def resolve_file(self, file):
        return os.path.abspath(file)

    def create_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def check_file_exists(self, file):
        if os.path.exists(file):
            sys.exit('error: ' + self.resolve_file(file) + ' already exists')

    def check_files_exist(self, files):
        for file in files:
            self.check_file_exists(file)

    def extract_zip_file(self, source, dest):
        with zipfile.ZipFile(source, 'r') as zip_ref:
            zip_ref.extractall(dest)

    def write_zip_file(self, file, content):
        with open(file, 'wb') as file:
            file.write(content)
