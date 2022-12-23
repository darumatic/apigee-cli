import builtins
import json
from os import getenv
from pathlib import Path

from apigee import utils

APP = "apigeecli"
CMD = "apigee"
__version__ = "0.51.1"
description = "(Unofficial) Apigee Management API command-line interface with multi-factor authentication (MFA) and single sign-on (SSO)/SAML support"
long_description = """(Unofficial) Apigee Management API command-line interface with multi-factor authentication (MFA) and single sign-on (SSO)/SAML support"""

APIGEE_CLI_DIRECTORY = utils.build_path_str(Path.home(), ".apigee")
APIGEE_CLI_PLUGINS_DIRECTORY = utils.build_path_str(APIGEE_CLI_DIRECTORY, "plugins")

APIGEE_ADMIN_API_URL = "https://api.enterprise.apigee.com"
APIGEE_CLI_ACCESS_TOKEN_FILE = utils.build_path_str(
    APIGEE_CLI_DIRECTORY, "access_token"
)
APIGEE_CLI_CREDENTIALS_FILE = utils.build_path_str(APIGEE_CLI_DIRECTORY, "credentials")
# APIGEE_CLI_EXCEPTION_LOG_FILE = utils.build_path_str(APIGEE_CLI_DIRECTORY, 'exception.log')
APIGEE_CLI_EXCEPTIONS_LOG_FILE = utils.build_path_str(
    APIGEE_CLI_DIRECTORY, "exceptions.log"
)
APIGEE_CLI_IS_MACHINE_USER = utils.is_envvar_true(getenv("APIGEE_CLI_IS_MACHINE_USER"))
APIGEE_CLI_PLUGINS_CONFIG_FILE = utils.build_path_str(
    APIGEE_CLI_PLUGINS_DIRECTORY, "config"
)
APIGEE_CLI_PLUGINS_PATH = utils.build_path_str(
    APIGEE_CLI_PLUGINS_DIRECTORY, "__init__.py"
)
APIGEE_CLI_PREFIX = getenv("APIGEE_CLI_PREFIX")
APIGEE_CLI_SYMMETRIC_KEY = getenv("APIGEE_CLI_SYMMETRIC_KEY")
APIGEE_CLI_TOGGLE_SILENT = False
APIGEE_CLI_TOGGLE_VERBOSE = 0
APIGEE_IS_TOKEN = getenv("APIGEE_IS_TOKEN")
APIGEE_MFA_SECRET = getenv("APIGEE_MFA_SECRET")
APIGEE_OAUTH_URL = "https://login.apigee.com/oauth/token"
APIGEE_ORG = getenv("APIGEE_ORG")
APIGEE_PASSWORD = getenv("APIGEE_PASSWORD")
APIGEE_SAML_LOGIN_URL = "https://{zonename}.login.apigee.com/passcode"
APIGEE_USERNAME = getenv("APIGEE_USERNAME")
APIGEE_ZONENAME = getenv("APIGEE_ZONENAME")
APIGEE_ZONENAME_OAUTH_URL = "https://{zonename}.login.apigee.com/oauth/token"

builtins.APIGEE_CLI_TOGGLE_SILENT = APIGEE_CLI_TOGGLE_SILENT
builtins.APIGEE_CLI_TOGGLE_VERBOSE = APIGEE_CLI_TOGGLE_VERBOSE
