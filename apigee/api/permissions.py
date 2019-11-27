#!/usr/bin/env python
"""https://docs.apigee.com/api-platform/system-administration/permissions"""

import json
import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.permissions import IPermissions, PermissionsSerializer
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
            "organization" : self._org_name,
            "path" : "/",
            "permissions" : [ "get" ]
          }, {
            "organization" : self._org_name,
            "path" : "/*",
            "permissions" : [ ]
          }, {
            "organization" : self._org_name,
            "path" : "/environments/*/targetservers",
            "permissions" : [ "put", "get" ]
          }, {
            "organization" : self._org_name,
            "path" : "/environments/*/targetservers/"+team_prefix+"*",
            "permissions" : [ "put", "get", "delete" ]
          }, {
            "organization" : self._org_name,
            "path" : "/developers",
            "permissions" : [ "get" ]
          }, {
            "organization" : self._org_name,
            "path" : "/apiproducts",
            "permissions" : [ "get" ]
          }, {
            "organization" : self._org_name,
            "path" : "/applications",
            "permissions" : [ "get" ]
          }, {
            "organization" : self._org_name,
            "path" : "/apiproducts/"+team_prefix+"*",
            "permissions" : [ "put", "get", "delete" ]
          }, {
            "organization" : self._org_name,
            "path" : "/applications/"+team_prefix+"*",
            "permissions" : [ "put", "get", "delete" ]
          }, {
            "organization" : self._org_name,
            "path" : "/developers/*/apps",
            "permissions" : [ "get" ]
          }, {
            "organization" : self._org_name,
            "path" : "/environments/*/caches",
            "permissions" : [ "get" ]
          }, {
            "organization" : self._org_name,
            "path" : "/apiproxies/*/maskconfigs",
            "permissions" : [ "get" ]
          }, {
            "organization" : self._org_name,
            "path" : "/developers/*/apps/"+team_prefix+"*",
            "permissions" : [ "put", "get", "delete" ]
          }, {
            "organization" : self._org_name,
            "path" : "/apiproxies/"+team_prefix+"*/maskconfigs",
            "permissions" : [ "put", "get", "delete" ]
          }, {
            "organization" : self._org_name,
            "path" : "/environments/*/keyvaluemaps",
            "permissions" : [ "put", "get" ]
          }, {
            "organization" : self._org_name,
            "path" : "/environments/*/caches/"+team_prefix+"*",
            "permissions" : [ "put", "get", "delete" ]
          }, {
            "organization" : self._org_name,
            "path" : "/environments/*/keyvaluemaps/"+team_prefix+"*",
            "permissions" : [ "put", "get", "delete" ]
          }, {
            "organization" : self._org_name,
            "path" : "/environments/*/applications/"+team_prefix+"*/revisions/*/debugsessions",
            "permissions" : [ "put", "get", "delete" ]
          }, {
            "organization" : self._org_name,
            "path": "/environments/*/applications/"+team_prefix+"*/revisions/*/deployments",
            "permissions": [ "put", "get", "delete" ]
          } ]
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
