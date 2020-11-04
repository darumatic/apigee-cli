import json
import os
import re
import sys
import zipfile
from pathlib import Path


def add_to_dict_if_exists(options_dict, initial_dict={}):
    for k, v in options_dict.items():
        if v:
            initial_dict[k] = v
    return initial_dict


def convert_to_set(iterable):
    if not isinstance(iterable, set):
        return set(iterable)
    return iterable


def extract_zip(source, dest):
    with zipfile.ZipFile(source, 'r') as zip_ref:
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
        sys.exit(f'error: {file} already exists')


def paths_exist(files):
    for file in files:
        path_exists(file)


def read_file(file, type='text'):
    with open(file, 'r') as f:
        if type == 'json':
            return json.loads(f.read())
        return f.read()


# def serializepath(path_items, separator='/'):
#     pass


def remove_last_items_from_list(init_list, integer=0):
    if integer <= 0:
        return init_list
    return init_list[:-integer]


def resolve_target_directory(target_directory=None):
    if target_directory:
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        return str(Path(target_directory).resolve())
    return os.getcwd()


def run_func_on_dir_files(dir, func, glob='**/*', args=(), kwargs={}):
    state = []
    for file_path in Path(resolve_target_directory(dir)).resolve().glob(glob):
        _tuple = (str(file_path),)
        result = func(*(_tuple + args), **kwargs)
        if result:
            state.append(result)
    return state


def run_func_on_iterable(iterable, func, state_op='append', args=(), kwargs={}):
    state = []
    for item in iterable:
        _tuple = (item,)
        result = func(*(_tuple + args), **kwargs)
        if result:
            getattr(state, state_op)(result)
    return state


def show_message(msg):
    print(msg)


def split_path(path, delimiter='[/\\\\]'):
    return re.split(delimiter, path)


def touch(path):
    try:
        with open(path, 'x'):
            os.utime(path, None)
    except FileNotFoundError:
        os.makedirs(os.path.split(path)[0])
    except FileExistsError:
        pass


def write_file(content, path, fs_write=True, indent=None, eof=True):
    if not fs_write:
        return
    touch(path)
    with open(path, 'w') as f:
        if isinstance(content, str):
            if eof:
                content = f'{content}\n'
            f.write(content)
        elif isinstance(content, dict) or isinstance(content, list):
            if isinstance(indent, int):
                content = f'{json.dumps(content, indent=indent)}'
            else:
                content = f'{json.dumps(content)}'
            if eof:
                f.write(f'{content}\n')
            else:
                f.write(content)


def write_zip(file, content):
    touch(file)
    with open(file, 'wb') as f:
        f.write(content)
