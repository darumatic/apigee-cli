import importlib
import inspect
import json
import logging
import os
import re
import sys
import zipfile
from pathlib import Path

import click


def apply_function_on_iterable(iterable, func, state_op="append", args=(), kwargs=None):
    if kwargs is None:
        kwargs = {}
    state = []
    for item in iterable:
        _tuple = (item,)
        result = func(*(_tuple + args), **kwargs)
        if result:
            getattr(state, state_op)(result)
    return state


def check_file_exists(file):
    if os.path.exists(file):
        sys.exit(f"error: {file} already exists")


def check_files_exist(files):
    for file in files:
        check_file_exists(file)


def create_directory(path):
    if not path:
        return
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except FileExistsError:
            logging.warning(f"{inspect.stack()[0][3]}; will ignore FileExistsError")


def create_empty_file(path):
    try:
        create_directory(os.path.split(path)[0])
        if not os.path.exists(path):
            with open(path, "x"):
                os.utime(path, None)
    except FileExistsError:
        logging.warning(f"{inspect.stack()[0][3]}; will ignore FileExistsError")


def ensure_set(iterable):
    return iterable if isinstance(iterable, set) else set(iterable)


def execute_function_on_directory_files(dir, func, glob="**/*", args=(), kwargs=None):
    if kwargs is None:
        kwargs = {}
    state = []
    for file_path in Path(get_resolved_directory_path(dir)).resolve().glob(glob):
        _tuple = (str(file_path),)
        result = func(*(_tuple + args), **kwargs)
        if result:
            state.append(result)
    return state


def extract_zip_file(source, dest):
    with zipfile.ZipFile(source, "r") as zip_ref:
        zip_ref.extractall(dest)


def filter_out_empty_values(dictionary):
    return {
        k: v for k, v in dictionary.items() if v
    }


def get_resolved_directory_path(target_directory=None):
    if target_directory:
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        return str(Path(target_directory).resolve())
    return os.getcwd()


def import_plugins_from_directory(plugins_init_file, existing_commands):
    try:
        spec = importlib.util.spec_from_file_location(
            "plugins_modules", plugins_init_file
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        import plugins_modules # type: ignore
        from plugins_modules import __all__ as all_plugins_modules # type: ignore

        for module in all_plugins_modules:
            _module = getattr(plugins_modules, module)
            if isinstance(_module, (click.core.Command, click.core.Group)):
                existing_commands.add(_module)
    except ImportError:
        logging.warning(
            f"{inspect.stack()[0][3]}; will skip loading plugin: {module}",
            exc_info=True,
        )


def is_directory(d):
    return os.path.isdir(d)


def is_regular_file(f):
    return os.path.isfile(f)


def merge_dict_values(options_dict, initial_dict=None):
    if initial_dict is None:
        initial_dict = {}
    for k, v in options_dict.items():
        if v:
            initial_dict[k] = v
    return initial_dict


def read_file_content(file, type="text"):
    with open(file, "r") as f:
        return json.loads(f.read()) if type == "json" else f.read()


def remove_file_if_above_size(file, size_kb=100):
    if os.path.getsize(file) > size_kb * 1024:
        os.remove(file)


def remove_last_elements(init_list, integer=0):
    return init_list if integer <= 0 else init_list[:-integer]


def show_message(msg):
    print(msg)


def split_path_by_delimiter(path, delimiter="[/\\\\]"):
    return re.split(delimiter, path)


def write_content_to_file(content, file_path, write_to_filesystem=True, indentation=None, append_eof=True):
    if not write_to_filesystem:
        return
    create_empty_file(file_path)
    with open(file_path, "w") as file:
        if isinstance(content, str):
            if append_eof:
                content = f"{content}\n"
            file.write(content)
        elif isinstance(content, (dict, list)):
            if isinstance(indentation, int):
                content = f"{json.dumps(content, indent=indentation)}"
            else:
                content = f"{json.dumps(content)}"
            if append_eof:
                file.write(f"{content}\n")
            else:
                file.write(content)


def write_content_to_zip(file, content):
    create_empty_file(file)
    with open(file, "wb") as f:
        f.write(content)
