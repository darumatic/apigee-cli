import json
import os
import re
import sys
import zipfile


def extract_zip(source, dest):
    with zipfile.ZipFile(source, "r") as zip_ref:
        zip_ref.extractall(dest)

def is_dir(d):
    return os.path.isdir(d)

def is_file(f):
    return os.path.isfile(f)

def make_dirs(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass

def path_exists(file):
    if os.path.exists(file):
        # sys.exit(f"error: {os.path.abspath(file)} already exists")
        sys.exit(f"error: {file} already exists")

def paths_exist(files):
    for file in files:
        path_exists(file)

def read_file(file, type="text"):
    with open(file, "r") as f:
        if type == "json":
            return json.loads(f.read())
        return f.read()

# def serializepath(path_items, separator='/'):
#     pass

def show_message(msg):
    print(msg)

def split_path(path, delimiter="[/\\\\]"):
    return re.split(delimiter, path)

def touch(path):
    try:
        with open(path, "x"):
            os.utime(path, None)
    except FileNotFoundError:
        os.makedirs(os.path.split(path)[0])
    except FileExistsError:
        pass

def write_file(content, path, fs_write=True):
    if not fs_write:
        return
    touch(path)
    with open(path, "w") as f:
        try:
            f.write(content)
        except TypeError:
            if isinstance(content, dict) or isinstance(content, list):
                f.write(json.dumps(content))

def write_zip(file, content):
    with open(file, "wb") as f:
        f.write(content)
