import functools
import inspect
import json
import logging
import sys

from apigee import APIGEE_CLI_EXCEPTION_LOG_FILE, console
from apigee.utils import touch


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
            touch(APIGEE_CLI_EXCEPTION_LOG_FILE)
            f_handler = logging.FileHandler(APIGEE_CLI_EXCEPTION_LOG_FILE, 'w+')
            f_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            f_handler.setFormatter(formatter)
            logging.getLogger("").addHandler(f_handler)
            logging.error('Exception occurred', exc_info=True)
            frm = inspect.trace()[-1]
            mod = inspect.getmodule(frm[0])
            modname = mod.__name__ if mod else frm[1]
            # error_message = {'Exception': {'detail': {'errorcode': f'{modname}.{type(e).__name__}'}, 'exceptionstring': f'{e}'}}
            sys.exit(
                f'An exception of type {modname}.{type(e).__name__} occurred. Arguments:\n{e}'
            )
            # sys.exit(json.dumps(error_message, indent=2))
        except KeyboardInterrupt as ki:
            console.echo()
            sys.exit(130)

    return wrapper
