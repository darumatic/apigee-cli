import os
import re
import sys
import zipfile


def makedirs(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass


def path_exists(file):
    if os.path.exists(file):
        sys.exit(f"error: {os.path.abspath(file)} already exists")


def paths_exist(files):
    for file in files:
        path_exists(file)


def extractzip(source, dest):
    with zipfile.ZipFile(source, "r") as zip_ref:
        zip_ref.extractall(dest)


def writezip(file, content):
    with open(file, "wb") as f:
        f.write(content)


# def serializepath(path_items, separator='/'):
#     pass


def splitpath(path, delimiter="[/\\\\]"):
    return re.split(delimiter, path)


def touch(path):
    try:
        with open(path, "x"):
            os.utime(path, None)
    except FileNotFoundError:
        os.makedirs(os.path.split(path)[0])
    except FileExistsError:
        pass
