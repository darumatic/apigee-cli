APP = 'apigeecli'
CMD = 'apigee'
__version__ = '0.46.2'
description = 'Apigee Management API command-line interface with multi-factor authentication (MFA) and single sign-on (SSO)/SAML support'
long_description = """Apigee Management API command-line interface with multi-factor authentication (MFA) and single sign-on (SSO)/SAML support"""

import json
from os import getenv
from pathlib import Path

# auth
APIGEE_USERNAME = getenv('APIGEE_USERNAME')
APIGEE_PASSWORD = getenv('APIGEE_PASSWORD')
APIGEE_MFA_SECRET = getenv('APIGEE_MFA_SECRET')
APIGEE_IS_TOKEN = getenv('APIGEE_IS_TOKEN')
APIGEE_ADMIN_API_URL = 'https://api.enterprise.apigee.com'
APIGEE_OAUTH_URL = 'https://login.apigee.com/oauth/token'
APIGEE_ZONENAME_OAUTH_URL = 'https://{zonename}.login.apigee.com/oauth/token'
APIGEE_ZONENAME = getenv('APIGEE_ZONENAME')
APIGEE_CLI_IS_MACHINE_USER = (
    True if getenv('APIGEE_CLI_IS_MACHINE_USER') in (True, 'True', 'true', '1') else False
)
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

# paths
APIGEE_CLI_DIRECTORY = str(Path.home() / '.apigee')
APIGEE_CLI_ACCESS_TOKEN_FILE = str(Path(APIGEE_CLI_DIRECTORY) / 'access_token')
APIGEE_CLI_CREDENTIALS_FILE = str(Path(APIGEE_CLI_DIRECTORY) / 'credentials')
APIGEE_CLI_EXCEPTION_LOG_FILE = str(Path(APIGEE_CLI_DIRECTORY) / 'exception.log')
APIGEE_CLI_PLUGINS_PATH = str(Path(APIGEE_CLI_DIRECTORY) / 'plugins' / '__init__.py')
# APIGEE_CLI_PLUGINS_NAME = 'plugins_modules'
