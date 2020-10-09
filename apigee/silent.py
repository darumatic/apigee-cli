import builtins

import click


def silent_callback(ctx, param, value):
    builtins.APIGEE_CLI_TOGGLE_SILENT = value


def common_silent_options(func):
    func = click.option(
        '--silent',
        show_default='toggle silent output',
        flag_value=True,
        default=False,
        callback=silent_callback,
    )(func)
    return func
