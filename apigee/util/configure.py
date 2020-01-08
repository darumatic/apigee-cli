#!/usr/bin/env python

import configparser
import os
from pathlib import Path

from apigee import APIGEE_CLI_DIRECTORY
from apigee import APIGEE_CLI_CREDENTIALS_FILE
from apigee.util.os import makedirs

class Configure:

    def __init__(self, args):
        self._args = args
        self._profile = args.profile
        self._config = configparser.ConfigParser()
        self._config.read(APIGEE_CLI_CREDENTIALS_FILE)
        self.KEY_LIST = (
            'username',
            'password',
            'mfa_secret',
            'org',
            'prefix'
        )
        try:
            self._profile_dict = dict(self._config._sections[self._profile])
            for key in self.KEY_LIST:
                if key not in self._profile_dict:
                    self._profile_dict[key] = None
        except KeyError:
            self._profile_dict = {k: None for k in self.KEY_LIST}

    def __call__(self):
        self._main()

    def _mask_secret(self, secret):
        return '*' * 16 if secret else secret

    def _remove_empty_keys(self, dict):
        return {k: v for k, v in dict.items() if v}

    def _save_config(self, file):
        makedirs(APIGEE_CLI_DIRECTORY)
        with open(file, 'w') as configfile:
            self._config.write(configfile)

    def _main(self):
        self._profile_dict['username'] = input('Apigee username (email) [{}]: '.format(self._profile_dict['username']))
        self._profile_dict['password'] = input('Apigee password [{}]: '.format(self._mask_secret(self._profile_dict['password'])))
        self._profile_dict['mfa_secret'] = input('Apigee MFA key (recommended) [{}]: '.format(self._mask_secret(self._profile_dict['mfa_secret'])))
        self._profile_dict['org'] = input('Default Apigee organization (recommended) [{}]: '.format(self._profile_dict['org']))
        self._profile_dict['prefix'] = input('Default team/resource prefix (recommended) [{}]: '.format(self._profile_dict['prefix']))
        self._config[self._profile] = self._remove_empty_keys(self._profile_dict)
        self._save_config(APIGEE_CLI_CREDENTIALS_FILE)
