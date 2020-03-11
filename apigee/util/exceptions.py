import functools
import logging
import sys

from apigee import *
from apigee.util import console
from apigee.util.os import touch


def exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            touch(APIGEE_CLI_EXCEPTION_LOG_FILE)
            f_handler = logging.FileHandler(APIGEE_CLI_EXCEPTION_LOG_FILE, "w+")
            f_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            f_handler.setFormatter(formatter)
            logging.getLogger("").addHandler(f_handler)
            logging.error("Exception occurred", exc_info=True)
            sys.exit(
                f"An exception of type {type(e).__name__} occurred. Arguments:\n{e}"
            )
        except KeyboardInterrupt as ki:
            console.log()
            sys.exit(130)

    return wrapper


class CustomError(Exception):
    pass
