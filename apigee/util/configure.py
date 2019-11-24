#!/usr/bin/env python

import configparser
import os
from pathlib import Path

from apigee import APIGEE_CLI_DIRECTORY
from apigee import APIGEE_CLI_CREDENTIALS_FILE
from apigee.util.io import IO

class Configure:

    def __init__(self, args):
        self._args = args
        self._profile = args.profile
        self._config = configparser.ConfigParser()
        self._config.read(APIGEE_CLI_CREDENTIALS_FILE)
        self._username = self._get_config(self._profile, 'username')
        self._password = self._get_config(self._profile, 'password')
        self._mfa_secret = self._get_config(self._profile, 'mfa_secret')
        self._org = self._get_config(self._profile, 'org')
        self._prefix = self._get_config(self._profile, 'prefix')

    def __call__(self):
        self._main()

    def _get_config(self, section, key):
        try:
            return self._config[section][key]
        except:
            return None

    def _main(self):
        self._username   = input('Apigee username (email) [{}]: '                    .format(self._username))
        self._password   = input('Apigee password [{}]: '                            .format(self._password))
        self._mfa_secret = input('Apigee MFA key (recommended) [{}]: '               .format(self._mfa_secret))
        self._org        = input('Default Apigee organization (recommended) [{}]: '  .format(self._org))
        self._prefix     = input('Default team/resource prefix (recommended) [{}]: ' .format(self._prefix))

        creds = {'username': self._username,
                 'password': self._password,
                 'mfa_secret': self._mfa_secret,
                 'org': self._org,
                 'prefix': self._prefix}

        self._config[self._profile] = {k: v for k, v in creds.items() if v}

        IO().makedirs(APIGEE_CLI_DIRECTORY)

        with open(APIGEE_CLI_CREDENTIALS_FILE, 'w') as configfile:
            self._config.write(configfile)
