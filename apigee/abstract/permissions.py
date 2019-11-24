#!/usr/bin/env python
"""https://docs.apigee.com/api-platform/system-administration/permissions"""

from abc import ABC, abstractmethod

import pandas as pd
from pandas.io.json import json_normalize

class IPermissions:

    def __init__(self, args, format=False):
        self._args = args
        self._format = format

    def __call__(self):
        pass

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        self._format = value

    @abstractmethod
    def create_permissions(self):
        pass

    @abstractmethod
    def team_permissions(self):
        pass

    @abstractmethod
    def get_permissions(self):
        pass

class PermissionsSerializer:
    def serialize_details(self, permission_details, format, max_colwidth=40):
        if format == 'text':
            return permission_details.text
        elif format == 'table':
            pd.set_option('display.max_colwidth', max_colwidth)
            return pd.DataFrame.from_dict(json_normalize(permission_details.json()['resourcePermission']), orient='columns')
        # else:
        #     raise ValueError(format)
        return permission_details
