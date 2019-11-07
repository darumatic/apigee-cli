APP = 'apigeecli'
CMD = 'apigee'
__version__ = '0.11.1'
description = 'Apigee Management API command-line interface with easy-to-use OAuth2 authentication'

import json
from os import getenv
from pathlib import Path

APIGEE_CLI_DIR = str(Path.home())+'/.apigee'
APIGEE_CLI_CREDS = APIGEE_CLI_DIR+'/credentials'
APIGEE_CLI_PREFIX = getenv('APIGEE_CLI_PREFIX')
APIGEE_USERNAME = getenv('APIGEE_USERNAME')
APIGEE_PASSWORD = getenv('APIGEE_PASSWORD')
APIGEE_MFA_SECRET = getenv('APIGEE_MFA_SECRET')
APIGEE_ADMIN_API_URL = 'https://api.enterprise.apigee.com'
APIGEE_OAUTH_URL = 'https://login.apigee.com/oauth/token'
APIGEE_ORG = getenv('APIGEE_ORG')
HTTP_MAX_RETRIES = 3
