import functools
import sys

def exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            sys.exit(f'An exception of type {type(e).__name__} occurred. Arguments:\n{e}')
        except KeyboardInterrupt as ki:
            print()
            sys.exit(130)
    return wrapper

class CustomError(Exception):
    pass
