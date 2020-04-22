APP = "apigeecli"
CMD = "apigee"
__version__ = "0.36.1"
description = (
    "Apigee Management API command-line interface with multi-factor authentication"
)
long_description = (
    """Apigee Management API command-line interface with multi-factor authentication

Getting Help:

    Homepage:
        https://pypi.org/project/apigeecli/

    Apigee Product Documentation:
        https://apidocs.apigee.com/management/apis

    The Apigee Management API command-line interface documentation:
        https://mdelotavo.github.io/apigee-cli/
    """
)

import json
from os import getenv
from pathlib import Path

APIGEE_CLI_AUTHORIZATION_DEVELOPER_ATTRIBUTE = "team"

APIGEE_CLI_DIRECTORY = str(Path.home() / ".apigee")
APIGEE_CLI_ACCESS_TOKEN_FILE = str(Path(APIGEE_CLI_DIRECTORY) / "access_token")
APIGEE_CLI_CREDENTIALS_FILE = str(Path(APIGEE_CLI_DIRECTORY) / "credentials")
APIGEE_CLI_EXCEPTION_LOG_FILE = str(Path(APIGEE_CLI_DIRECTORY) / "exception.log")

APIGEE_CLI_PREFIX = getenv("APIGEE_CLI_PREFIX")
APIGEE_USERNAME = getenv("APIGEE_USERNAME")
APIGEE_PASSWORD = getenv("APIGEE_PASSWORD")
APIGEE_MFA_SECRET = getenv("APIGEE_MFA_SECRET")
APIGEE_ADMIN_API_URL = "https://api.enterprise.apigee.com"
APIGEE_OAUTH_URL = "https://login.apigee.com/oauth/token"
APIGEE_ORG = getenv("APIGEE_ORG")

APIGEE_CLI_TOGGLE_SILENT = False
APIGEE_CLI_TOGGLE_VERBOSE = 0
