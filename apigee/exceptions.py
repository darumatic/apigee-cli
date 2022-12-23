import builtins
import functools
import inspect
import json
import logging
import sys

from apigee import console
from apigee.utils import remove_file_above_size, touch


class InvalidApisError(Exception):
    pass


def setup_global_logger(log_file):
    touch(log_file)
    remove_file_above_size(log_file, size_kb=1000)
    logging.basicConfig(
        filename=log_file,
        level=logging.WARNING,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            frm = inspect.trace()[-1]
            mod = inspect.getmodule(frm[0])
            modname = mod.__name__ if mod else frm[1]
            sys.exit(
                f"An exception of type {modname}.{type(e).__name__} occurred. Arguments:\n{e}"
            )
        except KeyboardInterrupt:
            console.echo()
            sys.exit(130)

    return wrapper
