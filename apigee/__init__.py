APP = 'apigeecli'
CMD = 'apigee'
__version__ = '0.23.6'
description = 'Apigee Management API command-line interface with multi-factor authentication'

import json
from os import getenv
from pathlib import Path

APIGEE_CLI_DIRECTORY = str(Path.home() / '.apigee')
APIGEE_CLI_ACCESS_TOKEN_FILE = str(Path(APIGEE_CLI_DIRECTORY) / 'access_token')
APIGEE_CLI_CREDENTIALS_FILE = str(Path(APIGEE_CLI_DIRECTORY) / 'credentials')
APIGEE_CLI_PREFIX = getenv('APIGEE_CLI_PREFIX')
APIGEE_CLI_SUPPRESS_RETRY_MESSAGE = getenv('APIGEE_CLI_SUPPRESS_RETRY_MESSAGE')
APIGEE_CLI_SUPPRESS_RETRY_RESPONSE = getenv('APIGEE_CLI_SUPPRESS_RETRY_RESPONSE')
APIGEE_USERNAME = getenv('APIGEE_USERNAME')
APIGEE_PASSWORD = getenv('APIGEE_PASSWORD')
APIGEE_MFA_SECRET = getenv('APIGEE_MFA_SECRET')
APIGEE_ADMIN_API_URL = 'https://api.enterprise.apigee.com'
APIGEE_OAUTH_URL = 'https://login.apigee.com/oauth/token'
APIGEE_ORG = getenv('APIGEE_ORG')
HTTP_MAX_RETRIES = 3

APIGEE_CLI_AUTHORIZATION_DEVELOPER_ATTRIBUTE = 'team'
