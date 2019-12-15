import os
import re
import sys
import zipfile

def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def path_exists(file):
    if os.path.exists(file):
        sys.exit('error: ' + os.path.abspath(file) + ' already exists')

def paths_exist(files):
    for file in files:
        path_exists(file)

def extractzip(source, dest):
    with zipfile.ZipFile(source, 'r') as zip_ref:
        zip_ref.extractall(dest)

def writezip(file, content):
    with open(file, 'wb') as f:
        f.write(content)

# def serializepath(path_items, separator='/'):
#     pass

def splitpath(path, delimiter='[/\\\\]'):
    return re.split(delimiter, path)
