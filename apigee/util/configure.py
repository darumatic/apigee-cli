#!/usr/bin/env python

import configparser
import os
from pathlib import Path

from apigee import APIGEE_CLI_DIRECTORY
from apigee import APIGEE_CLI_CREDENTIALS_FILE
from apigee.util.os import makedirs


class Configure:
    KEY_LIST = ("username", "password", "mfa_secret", "org", "prefix")

    def __init__(self, args):
        # self._args = args
        self._profile = args.profile
        self._config = configparser.ConfigParser()
        self._config.read(APIGEE_CLI_CREDENTIALS_FILE)
        try:
            self._profile_dict = dict(self._config._sections[self._profile])
            for key in self.KEY_LIST:
                if key not in self._profile_dict:
                    self._profile_dict[key] = None
        except KeyError:
            self._profile_dict = {k: None for k in self.KEY_LIST}

    def __call__(self):
        self.main()

    def _mask_secret(self, secret):
        return "*" * 16 if secret else secret

    def main(self):
        prompts = {
            "username": f"Apigee username (email) [{self._profile_dict['username']}]: ",
            "password": f"Apigee password [{self._mask_secret(self._profile_dict['password'])}]: ",
            "mfa_secret": f"Apigee MFA key (optional) [{self._mask_secret(self._profile_dict['mfa_secret'])}]: ",
            "org": f"Default Apigee organization (recommended) [{self._profile_dict['org']}]: ",
            "prefix": f"Default team/resource prefix (optional) [{self._profile_dict['prefix']}]: ",
        }
        self._profile_dict["username"] = input(prompts["username"])
        self._profile_dict["password"] = input(prompts["password"])
        self._profile_dict["mfa_secret"] = input(prompts["mfa_secret"])
        self._profile_dict["org"] = input(prompts["org"])
        self._profile_dict["prefix"] = input(prompts["prefix"])
        self._config[self._profile] = {k: v for k, v in self._profile_dict.items() if v}
        makedirs(APIGEE_CLI_DIRECTORY)
        with open(APIGEE_CLI_CREDENTIALS_FILE, "w") as configfile:
            self._config.write(configfile)
