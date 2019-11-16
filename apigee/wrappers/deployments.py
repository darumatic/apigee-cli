import functools

def get_api_proxy_deployment_details(func):
    @functools.wraps(func)
    def wrapper(fargs, *args, **kwargs):
        result = func(fargs)
        return result
    return wrapper
