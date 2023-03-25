import configparser
import contextlib

import click

from apigee import APIGEE_CLI_CREDENTIALS_FILE


def common_prefix_options(func):
    config = configparser.ConfigParser()
    config.read(APIGEE_CLI_CREDENTIALS_FILE)
    profile = "default"
    import sys

    for i, arg in enumerate(sys.argv):
        if arg in ["-P", "--profile"]:
            with contextlib.suppress(IndexError):
                profile = sys.argv[i + 1]
    profile_dict = {}
    with contextlib.suppress(KeyError):
        profile_dict = dict(config._sections[profile])
    prefix = ""
    with contextlib.suppress(KeyError):
        prefix = profile_dict["prefix"]
    return click.option(
        "--prefix",
        help="team/resource prefix filter",
        default=prefix,
        show_default=True,
    )(func)
