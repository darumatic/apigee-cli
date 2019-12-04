#!/usr/bin/env python
"""https://docs.apigee.com/api-platform/system-administration/permissions"""

import json
import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.permissions import IPermissions, PermissionsSerializer
from apigee.util import authorization

class Permissions(IPermissions):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_permissions(self, request_body):
        uri = '{0}/v1/organizations/{1}/userroles/{2}/resourcepermissions'.format(APIGEE_ADMIN_API_URL, self._org_name, self._role_name)
        hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, self._auth)
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def team_permissions(self, team_prefix):
        uri = '{0}/v1/organizations/{1}/userroles/{2}/resourcepermissions'.format(APIGEE_ADMIN_API_URL, self._org_name, self._role_name)
        hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, self._auth)
        body = {
          "resourcePermission" : [
          {
            "path" : "/",
            "permissions" : [ "get" ]
          },
          {
            "path" : "/apiproducts",
            "permissions" : [ "put", "get" ]
          },
          {
            "path" : "/apiproducts/*",
            "permissions" : [ ]
          },
          {
            "path" : "/apiproducts/" + team_prefix + "*",
            "permissions" : [ "delete", "put", "get" ]
          },
          {
            "path" : "/applications",
            "permissions" : [ "put", "get" ]
          },
          {
            "path" : "/applications/*",
            "permissions" : [ "get" ]
          },
          {
            "path" : "/developers/*/apps",
            "permissions" : [ "put", "get" ]
          },
          {
            "path" : "/developers/*/apps*",
            "permissions" : [  ]
          },
          {
            "path" : "/developers/*/apps/" + team_prefix + "*",
            "permissions" : [ "delete", "put", "get" ]
          },
          {
            "path" : "/developers/*/apps/" + team_prefix + "*/attributes",
            "permissions" : [ "put", "get" ]
          },
          {
            "path" : "/developers/*/apps/" + team_prefix + "*/attributes/*",
            "permissions" : [ "delete", "put", "get" ]
          },
          {
            "path" : "/environments/*/caches",
            "permissions" : [ "put", "get" ]
          },
          {
            "path" : "/applications/*/revisions",
            "permissions" : [ "get" ]
          },
          {
            "path" : "/applications/" + team_prefix + "*/revisions/*",
            "permissions" : [ "put", "get", "delete" ]
          },
          {
            "path" : "/environments/*/caches/*",
            "permissions" : [ ]
          },
          {
            "path" : "/applications/*/deployments",
            "permissions" : [ "get" ]
          },
          {
            "path" : "/environments/*/deployments",
            "permissions" : [ "get" ]
          },
          {
            "path" : "/apiproducts/" + team_prefix + "*/attributes",
            "permissions" : [ "put", "get" ]
          },
          {
            "path" : "/apiproxies/" + team_prefix + "*/maskconfigs",
            "permissions" : [ "put", "get" ]
          },
          {
            "path" : "/environments/*/keyvaluemaps",
            "permissions" : [ "put", "get" ]
          },
          {
            "path" : "/environments/*/virtualhosts",
            "permissions" : [ "get" ]
          },
          {
            "path" : "/environments/*/caches/" + team_prefix + "*",
            "permissions" : [ "delete", "put", "get" ]
          },
          {
            "path" : "/environments/*/targetservers",
            "permissions" : [ "put", "get" ]
          },
          {
            "path" : "/apiproducts/" + team_prefix + "*/attributes/*",
            "permissions" : [ "delete", "put", "get" ]
          },
          {
            "path" : "/apiproxies/" + team_prefix + "*/maskconfigs/*",
            "permissions" : [ "delete", "put", "get" ]
          },
          {
            "path" : "/environments/*/keyvaluemaps/*",
            "permissions" : [ ]
          },
          {
            "path" : "/environments/*/virtualhosts/*",
            "permissions" : [ "get" ]
          },
          {
            "path" : "/environments/*/targetservers/*",
            "permissions" : [ ]
          },
          {
            "path" : "/environments/*/keyvaluemaps/" + team_prefix + "*",
            "permissions" : [ "delete", "put", "get" ]
          },
          {
            "path" : "/environments/*/keyvaluemaps/" + team_prefix + "*/entries",
            "permissions" : [ "put" ]
          },
          {
            "path" : "/environments/*/targetservers/" + team_prefix + "*",
            "permissions" : [ "delete", "put", "get" ]
          },
          {
            "organization": "snsw",
            "path": "/applications/*/revisions/*",
            "permissions": [ "put", "get", "delete" ]
          },
          {
            "path" : "/applications/*/revisions/*/deployments",
            "permissions" : [ "put", "get" ]
          },
          {
            "path" : "/environments/*/applications/*/deployments",
            "permissions" : [ "get" ]
          },
          {
            "path" : "/environments/*/keyvaluemaps/" + team_prefix + "*/entries/*",
            "permissions" : [ "delete", "put", "get" ]
          },
          {
            "path" : "/environments/*/applications/*/revisions/*/deployments",
            "permissions" : [ "get" ]
          },
          {
            "path" : "/environments/*/applications/" + team_prefix + "*/revisions/*/deployments",
            "permissions" : [ "delete", "put", "get" ]
          },
          {
            "path" : "/environments/dev/applications/*/revisions/*/deployments",
            "permissions" : [ "delete", "put", "get" ]
          },
          {
            "path" : "/environments/sit/applications/*/revisions/*/deployments",
            "permissions" : [ "delete", "put", "get" ]
          },
          {
            "path" : "/environments/test/applications/*/revisions/*/deployments",
            "permissions" : [ "delete", "put", "get" ]
          },
          {
            "path" : "/environments/sandbox/applications/*/revisions/*/deployments",
            "permissions" : [ "delete", "put", "get" ]
          },
          {
            "path" : "/environments/psm/applications/*/revisions/*/deployments",
            "permissions" : [ "delete", "put", "get" ]
          },
          {
            "path" : "/environments/*/applications/" + team_prefix + "*/revisions/*/debugsessions",
            "permissions" : [ "put", "get" ]
          },
          {
            "path" : "/environments/*/applications/" + team_prefix + "*/revisions/*/debugsessions/*",
            "permissions" : [ "delete", "put", "get" ]
          }
         ]
        }
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def get_permissions(self, formatted=False, format='text', showindex=False, tablefmt='plain'):
        uri = '{0}/v1/o/{1}/userroles/{2}/permissions'.format(APIGEE_ADMIN_API_URL, self._org_name, self._role_name)
        hdrs = authorization.set_header({'Accept': 'application/json'}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        if formatted:
            return PermissionsSerializer().serialize_details(resp, format, showindex=showindex, tablefmt=tablefmt)
        return resp
