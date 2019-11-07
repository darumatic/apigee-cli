from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

import argparse
import functools
import inspect
import os
import sys

import apigee

def do_nothing():
    pass

def envvar_exists(envvar):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if getattr(apigee, envvar) is not None:
                result = func(*args, **kwargs)
                return result
            else:
                do_nothing()
        return wrapper
    return actual_decorator

def exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            s = 'An exception of type {0} occurred. Arguments:\n{1}'
            # print(s.format(type(e).__name__, e.args))
            print(s.format(type(e).__name__, e))
            sys.exit(1)
        except KeyboardInterrupt as ki:
            s = 'An exception of type {0} occurred. Arguments:\n{1}'
            # print('\n', s.format(type(ki).__name__, ki))
            print()
            sys.exit(130)
    return wrapper

def test(args):
    print(mfa_with_pyotp.get_access_token(args))

def isempty(s):
    return s == '' or s.isspace()

def isfile(f):
    if os.path.isfile(f):
        return f
    raise argparse.ArgumentTypeError('not a file')

def isdir(d):
    if os.path.isdir(d):
        return d
    raise argparse.ArgumentTypeError('not a directory')

# https://stackoverflow.com/a/15813469
module = sys.modules[__name__]
name_func_tuples = inspect.getmembers(module, inspect.isfunction)
name_func_tuples = [t for t in name_func_tuples if inspect.getmodule(t[1]) == module]
functions = dict(name_func_tuples)

__all__.extend(list(functions))
