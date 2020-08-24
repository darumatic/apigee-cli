import configparser

import click

from apigee import (APIGEE_CLI_AUTHORIZATION_DEVELOPER_ATTRIBUTE,
                    APIGEE_CLI_CREDENTIALS_FILE)
from apigee.developers.developers import Developers


def common_prefix_options(func):
    config = configparser.ConfigParser()
    config.read(APIGEE_CLI_CREDENTIALS_FILE)
    profile = 'default'
    import sys

    for i, arg in enumerate(sys.argv):
        if arg == '-P' or arg == '--profile':
            try:
                profile = sys.argv[i + 1]
            except IndexError:
                pass
    profile_dict = {}
    try:
        profile_dict = dict(config._sections[profile])
    except KeyError:
        pass
    prefix = ''
    try:
        prefix = profile_dict['prefix']
    except KeyError:
        pass
    return click.option(
        '--prefix', help='team/resource prefix filter', default=prefix, show_default=True
    )(func)


def auth_with_prefix(
    auth_obj, org, name, attribute_name=APIGEE_CLI_AUTHORIZATION_DEVELOPER_ATTRIBUTE
):
    team = (
        Developers(auth_obj, org, auth_obj.username)
        .get_developer_attribute(attribute_name)
        .json()['value']
    )
    allowed = team.split(',')
    for prefix in allowed:
        if name.startswith(prefix):
            return name
    raise Exception(
        f'401 Client Error: Unauthorized for team: {str(allowed)}\nAttempted to access resource: {name}'
    )
