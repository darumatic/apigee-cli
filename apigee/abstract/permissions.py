#!/usr/bin/env python
"""https://docs.apigee.com/api-platform/system-administration/permissions"""

from abc import ABC, abstractmethod

# import pandas as pd
# from pandas.io.json import json_normalize
from tabulate import tabulate

class IPermissions:

    def __init__(self, args):
        self._args = args

    def __call__(self):
        pass

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value

    @abstractmethod
    def create_permissions(self):
        pass

    @abstractmethod
    def team_permissions(self):
        pass

    @abstractmethod
    def get_permissions(self, formatted=False, showindex=False, tablefmt='plain'):
        pass

class PermissionsSerializer:
    def serialize_details(self, permission_details, format, showindex=False, tablefmt='plain'):
        if format == 'text':
            return permission_details.text
        elif format == 'table':
            # pd.set_option('display.max_colwidth', max_colwidth)
            # return pd.DataFrame.from_dict(json_normalize(permission_details.json()['resourcePermission']), orient='columns')
            table = [[res['organization'], res['path'], res['permissions']] for res in permission_details.json()['resourcePermission']]
            headers = list()
            if showindex == 'always' or showindex is True:
                headers = ['id', 'organization', 'path', 'permissions']
            elif showindex == 'never' or showindex is False:
                headers = ['organization', 'path', 'permissions']
            return tabulate(table, headers, showindex=showindex, tablefmt=tablefmt)
        # else:
        #     raise ValueError(format)
        return permission_details
