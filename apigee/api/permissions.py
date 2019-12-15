#!/usr/bin/env python
"""https://docs.apigee.com/api-platform/system-administration/permissions"""

import json
import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.permissions import IPermissions, PermissionsSerializer
from apigee.data.permissions import default, prod as production
from apigee.util import authorization

class Permissions(IPermissions):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_permissions(self, request_body):
        uri = '{0}/v1/organizations/{1}/userroles/{2}/resourcepermissions' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._role_name)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def team_permissions(self, team_prefix, prod=False):
        uri = '{0}/v1/organizations/{1}/userroles/{2}/resourcepermissions' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._role_name)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        if prod:
            body = production.resource_permissions(team_prefix)
        else:
            body = default.resource_permissions(team_prefix)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def get_permissions(self, formatted=False, format='text', showindex=False, tablefmt='plain'):
        uri = '{0}/v1/o/{1}/userroles/{2}/permissions' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._role_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        if formatted:
            return PermissionsSerializer().serialize_details(resp, format, showindex=showindex, tablefmt=tablefmt)
        return resp
