APP = 'apigeecli'
CMD = 'apigee'
__version__ = '0.48.1'
description = 'Apigee Management API command-line interface with multi-factor authentication (MFA) and single sign-on (SSO)/SAML support'
long_description = """Apigee Management API command-line interface with multi-factor authentication (MFA) and single sign-on (SSO)/SAML support"""

import json
from os import getenv
from pathlib import Path


def is_true(value):
    return value in (True, 'True', 'true', '1')


def str_path(*args):
    if not args:
        return
    path = None
    for arg in args:
        if not path:
            path = Path(arg)
        else:
            path /= arg
    return str(path)


# auth
APIGEE_USERNAME = getenv('APIGEE_USERNAME')
APIGEE_PASSWORD = getenv('APIGEE_PASSWORD')
APIGEE_MFA_SECRET = getenv('APIGEE_MFA_SECRET')
APIGEE_IS_TOKEN = getenv('APIGEE_IS_TOKEN')
APIGEE_ADMIN_API_URL = 'https://api.enterprise.apigee.com'
APIGEE_OAUTH_URL = 'https://login.apigee.com/oauth/token'
APIGEE_ZONENAME_OAUTH_URL = 'https://{zonename}.login.apigee.com/oauth/token'
APIGEE_ZONENAME = getenv('APIGEE_ZONENAME')
APIGEE_CLI_IS_MACHINE_USER = is_true(getenv('APIGEE_CLI_IS_MACHINE_USER'))
APIGEE_SAML_LOGIN_URL = 'https://{zonename}.login.apigee.com/passcode'
APIGEE_ORG = getenv('APIGEE_ORG')

# crypto
APIGEE_CLI_SYMMETRIC_KEY = getenv('APIGEE_CLI_SYMMETRIC_KEY')

# custom
APIGEE_CLI_AUTHORIZATION_DEVELOPER_ATTRIBUTE = 'team'
APIGEE_CLI_PREFIX = getenv('APIGEE_CLI_PREFIX')

# flags
APIGEE_CLI_TOGGLE_SILENT = False
APIGEE_CLI_TOGGLE_VERBOSE = 0

# config directory
APIGEE_CLI_DIRECTORY = str_path(Path.home(), '.apigee')

# top-level config files
APIGEE_CLI_ACCESS_TOKEN_FILE = str_path(APIGEE_CLI_DIRECTORY, 'access_token')
APIGEE_CLI_CREDENTIALS_FILE = str_path(APIGEE_CLI_DIRECTORY, 'credentials')
APIGEE_CLI_EXCEPTION_LOG_FILE = str_path(APIGEE_CLI_DIRECTORY, 'exception.log')

# plugin files
APIGEE_CLI_PLUGINS_DIRECTORY = str_path(APIGEE_CLI_DIRECTORY, 'plugins')
APIGEE_CLI_PLUGINS_CONFIG_FILE = str_path(APIGEE_CLI_PLUGINS_DIRECTORY, 'config')
APIGEE_CLI_PLUGINS_PATH = str_path(APIGEE_CLI_PLUGINS_DIRECTORY, '__init__.py')
