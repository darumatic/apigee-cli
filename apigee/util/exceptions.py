import functools
import sys

def exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            s = 'An exception of type {0} occurred. Arguments:\n{1}'
            # print(s.format(type(e).__name__, e.args))
            sys.exit(s.format(type(e).__name__, e))
        except KeyboardInterrupt as ki:
            s = 'An exception of type {0} occurred. Arguments:\n{1}'
            # print('\n', s.format(type(ki).__name__, ki))
            print()
            sys.exit(130)
    return wrapper

class CustomError(Exception):
    pass
