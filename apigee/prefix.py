import configparser

import click

from apigee import APIGEE_CLI_CREDENTIALS_FILE


def common_prefix_options(func):
    config = configparser.ConfigParser()
    config.read(APIGEE_CLI_CREDENTIALS_FILE)
    profile = "default"
    import sys

    for i, arg in enumerate(sys.argv):
        if arg == "-P" or arg == "--profile":
            try:
                profile = sys.argv[i + 1]
            except IndexError:
                pass
    profile_dict = {}
    try:
        profile_dict = dict(config._sections[profile])
    except KeyError:
        pass
    prefix = ""
    try:
        prefix = profile_dict["prefix"]
    except KeyError:
        pass
    return click.option(
        "--prefix",
        help="team/resource prefix filter",
        default=prefix,
        show_default=True,
    )(func)
