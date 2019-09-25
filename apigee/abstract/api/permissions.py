#!/usr/bin/env python
"""https://docs.apigee.com/api-platform/system-administration/permissions"""

from abc import ABC, abstractmethod

# import pandas as pd
# from pandas.io.json import json_normalize
from tabulate import tabulate


class IPermissions:
    def __init__(self, auth, org_name, role_name):
        self._auth = auth
        self._org_name = org_name
        self._role_name = role_name

    def __call__(self):
        pass

    @property
    def auth(self):
        return self._auth

    @auth.setter
    def auth(self, value):
        self._auth = value

    @property
    def org_name(self):
        return self._org_name

    @org_name.setter
    def org_name(self, value):
        self._org_name = value

    @property
    def role_name(self):
        return self._role_name

    @role_name.setter
    def role_name(self, value):
        self._role_name = value

    @abstractmethod
    def create_permissions(self, request_body):
        pass

    @abstractmethod
    def team_permissions(
        self, template_file, placeholder_key=None, placeholder_value=""
    ):
        pass

    @abstractmethod
    def get_permissions(
        self, formatted=False, format="text", showindex=False, tablefmt="plain"
    ):
        pass


class PermissionsSerializer:
    def serialize_details(
        self, permission_details, format, showindex=False, tablefmt="plain"
    ):
        if format == "text":
            return permission_details.text
        elif format == "table":
            # pd.set_option('display.max_colwidth', max_colwidth)
            # return pd.DataFrame.from_dict(json_normalize(permission_details.json()['resourcePermission']), orient='columns')
            table = [
                [res["organization"], res["path"], res["permissions"]]
                for res in permission_details.json()["resourcePermission"]
            ]
            headers = []
            if showindex == "always" or showindex is True:
                headers = ["id", "organization", "path", "permissions"]
            elif showindex == "never" or showindex is False:
                headers = ["organization", "path", "permissions"]
            return tabulate(table, headers, showindex=showindex, tablefmt=tablefmt)
        # else:
        #     raise ValueError(format)
        return permission_details
