from os.path import dirname, basename, isfile, join
import glob

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [
    basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")
]

import functools
import inspect
import sys

import apigee


def envvar_exists(envvar):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if getattr(apigee, envvar) is not None:
                result = func(*args, **kwargs)
                return result

        return wrapper

    return actual_decorator


# https://stackoverflow.com/a/15813469
module = sys.modules[__name__]
name_func_tuples = inspect.getmembers(module, inspect.isfunction)
name_func_tuples = [t for t in name_func_tuples if inspect.getmodule(t[1]) == module]
functions = dict(name_func_tuples)

__all__.extend(list(functions))
