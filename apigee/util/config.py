#!/usr/bin/env python

import os
import configparser
from pathlib import Path

from apigee import APIGEE_CLI_DIR
from apigee import APIGEE_CLI_CREDS

def main(fargs, *args, **kwargs):

    profile_name = fargs.profile

    username = 'None'
    password = 'None'
    mfa_secret = 'None'
    org = 'None'
    prefix = 'None'

    existing_config = configparser.ConfigParser()
    existing_config.read(APIGEE_CLI_CREDS)

    if os.path.isfile(APIGEE_CLI_CREDS):
        existing_config = configparser.ConfigParser()
        existing_config.read(APIGEE_CLI_CREDS)
        if profile_name in existing_config:
            try:
                username = existing_config[profile_name]['username']
            except:
                username = None
            try:
                password = '*'*16 if existing_config[profile_name]['password'] else None
            except:
                password = None
            try:
                mfa_secret = '*'*16 if existing_config[profile_name]['mfa_secret'] else None
            except:
                mfa_secret = None
            try:
                org = existing_config[profile_name]['org']
            except:
                org = None
            try:
                prefix = existing_config[profile_name]['prefix']
            except:
                prefix = None

    username = input('Apigee username (email) [{}]: '.format(username))
    password = input('Apigee password [{}]: '.format(password))
    mfa_secret = input('Apigee MFA key (recommended) [{}]: '.format(mfa_secret))
    org = input('Default Apigee organization (recommended) [{}]: '.format(org))
    prefix = input('Default team/resource prefix (recommended) [{}]: '.format(prefix))

    creds = {'username': username,
             'password': password,
             'mfa_secret': mfa_secret,
             'org': org,
             'prefix': prefix}

    # config = configparser.ConfigParser()
    # config[profile_name] = {k: v for k, v in creds.items() if v}
    config = existing_config
    config[profile_name] = {k: v for k, v in creds.items() if v}

    if not os.path.exists(APIGEE_CLI_DIR):
        os.makedirs(APIGEE_CLI_DIR)

    with open(APIGEE_CLI_CREDS, 'w') as configfile:
        config.write(configfile)

if __name__ == '__main__':
    main()
