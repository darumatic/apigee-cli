import builtins
import http.client as http_client
import logging

import click
import requests


def verbose_callback(ctx, param, value):
    builtins.APIGEE_CLI_TOGGLE_VERBOSE = value
    if value > 0:
        http_client.HTTPConnection.debuglevel = value - 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger('requests.packages.urllib3')
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True


def common_verbose_options(func):
    func = click.option(
        '-v',
        '--verbose',
        show_default='toggle verbose output',
        count=True,
        callback=verbose_callback,
    )(func)
    return func
