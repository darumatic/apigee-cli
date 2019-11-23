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

    def makedirs(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def path_exists(self, file):
        if os.path.exists(file):
            sys.exit('error: ' + os.path.abspath(file) + ' already exists')

    def paths_exist(self, files):
        for file in files:
            self.path_exists(file)

    def extractzip(self, source, dest):
        with zipfile.ZipFile(source, 'r') as zip_ref:
            zip_ref.extractall(dest)

    def writezip(self, file, content):
        with open(file, 'wb') as file:
            file.write(content)
