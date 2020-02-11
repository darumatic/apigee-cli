import configparser
import base64
import os
import time

import jwt

from apigee import (APIGEE_CLI_CREDENTIALS_FILE,
                    APIGEE_CLI_DIRECTORY,
                    APIGEE_CLI_ACCESS_TOKEN_FILE,
                    APIGEE_CLI_AUTHORIZATION_DEVELOPER_ATTRIBUTE)
from apigee.api.developers import Developers
from apigee.util import envvar_exists, mfa_with_pyotp
from apigee.util.os import makedirs

def set_header(hdrs, args):
    if hdrs is None:
        hdrs = dict()
    if args.mfa_secret:
        access_token = ''
        makedirs(APIGEE_CLI_DIRECTORY)
        try:
            with open(APIGEE_CLI_ACCESS_TOKEN_FILE, 'r') as f:
                access_token = f.read()
        except (IOError, OSError) as e:
            pass
        finally:
            if access_token:
                decoded = jwt.decode(access_token, verify=False)
                if decoded['exp'] < int(time.time()):
                    access_token = ''
        if not access_token:
            access_token = mfa_with_pyotp.get_access_token(args)
            with open(APIGEE_CLI_ACCESS_TOKEN_FILE, 'w') as f:
                f.write(access_token)
        hdrs['Authorization'] = 'Bearer ' + access_token
    else:
        hdrs['Authorization'] = 'Basic ' + base64.b64encode((args.username + ':' + args.password).encode()).decode()
    return hdrs

def get_credential(section, key):
    try:
        config = configparser.ConfigParser()
        config.read(APIGEE_CLI_CREDENTIALS_FILE)
        if section in config:
            return config[section][key]
    except:
        return None

def with_prefix(name, args, attribute_name=APIGEE_CLI_AUTHORIZATION_DEVELOPER_ATTRIBUTE):
    team = Developers(args, args.org, args.username).get_developer_attribute(attribute_name).json()['value']
    allowed = team.split(',')
    for prefix in allowed:
        if name.startswith(prefix):
            return name
    raise Exception('401 Client Error: Unauthorized for team: ' + str(allowed) + '\nAttempted to access resource: ' + name)
