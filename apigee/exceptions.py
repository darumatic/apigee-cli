import builtins
import functools
import inspect
import json
import logging
import sys

from apigee import APIGEE_CLI_EXCEPTIONS_LOG_FILE, console
from apigee.utils import remove_file_above_size, touch


def setup_global_logger():
    remove_file_above_size(APIGEE_CLI_EXCEPTIONS_LOG_FILE, size_kb=1000)
    f_handler = logging.FileHandler(APIGEE_CLI_EXCEPTIONS_LOG_FILE)
    f_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(formatter)
    logging.getLogger("").addHandler(f_handler)
    # logging.StreamHandler(stream=None)


class InvalidApisError(Exception):
    pass


class NotYetImplementedError(Exception):
    pass


def exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.error('Exception occurred', exc_info=True)
            frm = inspect.trace()[-1]
            mod = inspect.getmodule(frm[0])
            modname = mod.__name__ if mod else frm[1]
            sys.exit(f'An exception of type {modname}.{type(e).__name__} occurred. Arguments:\n{e}')
        except KeyboardInterrupt:
            console.echo()
            sys.exit(130)

    return wrapper
