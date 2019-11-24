#!/usr/bin/env python
"""https://apidocs.apigee.com/api/user-roles"""

import json
import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.userroles import IUserroles
from apigee.util import authorization

class Userroles(IUserroles):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_a_user_to_a_role(self, user_email):
        uri = '{0}/v1/organizations/{1}/userroles/{2}/users?id={3}'.format(APIGEE_ADMIN_API_URL, self._org_name, self._role_name, user_email)
        hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}, self._auth)
        resp = requests.post(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def add_permissions_for_a_resource_to_a_user_role(self):
        pass

    def add_permissions_for_multiple_resources_to_a_user_role(self):
        pass

    def create_a_user_role_in_an_organization(self):
        uri = '{0}/v1/organizations/{1}/userroles'.format(APIGEE_ADMIN_API_URL, self._org_name)
        hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, self._auth)
        roles = []
        for role in self._role_name:
            roles.append({
                'name': role
            })
        body = {"role" : roles}
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def delete_a_permission_for_a_resource(self, permission, resource_path):
        uri = '{0}/v1/organizations/{1}/userroles/{2}/permissions/{3}?path={4}'.format(APIGEE_ADMIN_API_URL, self._org_name, self._role_name, permission, resource_path)
        hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/octet-stream'}, self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def delete_a_user_role(self):
        uri = '{0}/v1/organizations/{1}/userroles/{2}'.format(APIGEE_ADMIN_API_URL, self._org_name, self._role_name)
        hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}, self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def get_a_role(self):
        pass

    def get_resource_permissions_for_a_specific_role(self):
        pass

    def get_users_for_a_role(self):
        pass

    def list_permissions_for_a_resource(self):
        pass

    def list_user_roles(self):
        pass

    def remove_user_membership_in_role(self, user_email):
        uri = '{0}/v1/organizations/{1}/userroles/{2}/users/{3}'.format(APIGEE_ADMIN_API_URL, self._org_name, self._role_name, user_email)
        hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def verify_a_user_roles_permission_on_a_specific_RBAC_resource(self):
        pass

    def verify_user_role_membership(self):
        pass
