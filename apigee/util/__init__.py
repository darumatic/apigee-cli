from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

import argparse
import functools
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
            exit(1)
    return wrapper

def test(args):
    print(mfa_with_pyotp.get_access_token(args))

def isempty(s):
    return s == '' or s.isspace()

def isfile(f):
    if os.path.isfile(f):
        return f
    else:
        raise argparse.ArgumentTypeError('not a file')

def isdir(d):
    if os.path.isdir(d):
        return d
    else:
        raise argparse.ArgumentTypeError('not a directory')

__all__.extend(['do_nothing', 'envvar_exists', 'exception_handler', 'test', 'isempty', 'isfile', 'isdir'])
