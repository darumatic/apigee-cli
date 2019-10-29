APP = 'apigeecli'
CMD = 'apigee'
__version__ = '0.4.0'
description = 'apigee cli'

import json
from os import getenv

def getenv_else(a, b):
    try:
        return getenv(a) if getenv(a) is not None else b
    except:
        return None

def strtobool(s):
    try:
        return json.loads(s.lower()) if s is not None else None
    except:
        return None

APIGEE_CLI_PREFIX = getenv('APIGEE_CLI_PREFIX')
APIGEE_USERNAME = getenv('APIGEE_USERNAME')
APIGEE_PASSWORD = getenv('APIGEE_PASSWORD')
APIGEE_MFA_SECRET = getenv('APIGEE_MFA_SECRET')
APIGEE_ADMIN_API_URL = 'https://api.enterprise.apigee.com'
APIGEE_OAUTH_URL = 'https://login.apigee.com/oauth/token'
APIGEE_ORG = getenv('APIGEE_ORG')
HTTP_MAX_RETRIES = 3
