#!/usr/bin/env python

import os
import configparser
from pathlib import Path

from apigee import APIGEE_CLI_DIRECTORY
from apigee import APIGEE_CLI_CREDENTIALS_FILE

class Configure:

    def __init__(self, args):
        self._args = args
        self._profile = args.profile
        self._config = configparser.ConfigParser()
        self._config.read(APIGEE_CLI_CREDENTIALS_FILE)
        self._username = None
        self._password = None
        self._mfa_secret = None
        self._org = None
        self._prefix = None

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, value):
        self._profile = value

    def _get_config(self, section, key):
        try:
            return self._config[section][key]
        except:
            pass

    def __call__(self):
        self._main()

    def _main(self):

        args = self._args
        profile_name = self._profile
        config = self._config

        if os.path.isfile(APIGEE_CLI_CREDENTIALS_FILE):
            if profile_name in config:
                self._username = self._get_config(profile_name, 'username')
                self._password = self._get_config(profile_name, 'password')
                self._mfa_secret = self._get_config(profile_name, 'mfa_secret')
                self._org = self._get_config(profile_name, 'org')
                self._prefix = self._get_config(profile_name, 'prefix')

        self._username = input('Apigee username (email) [{}]: '.format(self._username))
        self._password = input('Apigee password [{}]: '.format(self._password))
        self._mfa_secret = input('Apigee MFA key (recommended) [{}]: '.format(self._mfa_secret))
        self._org = input('Default Apigee organization (recommended) [{}]: '.format(self._org))
        self._prefix = input('Default team/resource prefix (recommended) [{}]: '.format(self._prefix))

        creds = {'username': self._username,
                 'password': self._password,
                 'mfa_secret': self._mfa_secret,
                 'org': self._org,
                 'prefix': self._prefix}

        config[profile_name] = {k: v for k, v in creds.items() if v}

        if not os.path.exists(APIGEE_CLI_DIRECTORY):
            os.makedirs(APIGEE_CLI_DIRECTORY)

        with open(APIGEE_CLI_CREDENTIALS_FILE, 'w') as configfile:
            config.write(configfile)
