#!/usr/bin/env python
"""https://apidocs.apigee.com/api/user-roles"""

import json
import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.userroles import IUserroles
from apigee.util import authorization

class Userroles(IUserroles):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_a_user_to_a_role(self, user_email):
        uri = '{0}/v1/organizations/{1}/userroles/{2}/users?id={3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._role_name,
                    user_email)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/x-www-form-urlencoded'},
                                        self._auth)
        resp = requests.post(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def add_permissions_for_a_resource_to_a_user_role(self, request_body):
        uri = '{0}/v1/organizations/{1}/userroles/{2}/permissions' \
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

    def add_permissions_for_multiple_resources_to_a_user_role(self, request_body):
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

    def create_a_user_role_in_an_organization(self):
        uri = '{0}/v1/organizations/{1}/userroles' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
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
        uri = '{0}/v1/organizations/{1}/userroles/{2}/permissions/{3}?path={4}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._role_name,
                    permission,
                    resource_path)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/octet-stream'},
                                        self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def delete_resource_from_permissions(self, resource_path):
        uri = '{0}/v1/organizations/{1}/userroles/{2}/permissions?path={3}&delete=true' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._role_name,
                    resource_path)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/octet-stream'},
                                        self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def delete_a_user_role(self):
        uri = '{0}/v1/organizations/{1}/userroles/{2}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._role_name)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/x-www-form-urlencoded'},
                                        self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def get_a_role(self):
        uri = '{0}/v1/organizations/{1}/userroles/{2}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._role_name)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def get_resource_permissions_for_a_specific_role(self, resource_path=''):
        uri = '{0}/v1/organizations/{1}/userroles/{2}/permissions' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._role_name)
        if resource_path:
            uri += '?path={}'.format(resource_path)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/octet-stream'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def get_users_for_a_role(self):
        uri = '{0}/v1/organizations/{1}/userroles/{2}/users' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._role_name)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def list_permissions_for_a_resource(self):
        uri = '{0}/v1/organizations/{1}/userroles/{2}/permissions' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._role_name)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def list_user_roles(self):
        uri = '{0}/v1/organizations/{1}/userroles' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def remove_user_membership_in_role(self, user_email):
        uri = '{0}/v1/organizations/{1}/userroles/{2}/users/{3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._role_name,
                    user_email)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def verify_a_user_roles_permission_on_a_specific_RBAC_resource(self, permission, resource_path):
        uri = '{0}/v1/organizations/{1}/userroles/{2}/permissions/{3}?path={4}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._role_name,
                    permission,
                    resource_path)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/octet-stream'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def verify_user_role_membership(self, user_email):
        uri = '{0}/v1/organizations/{1}/userroles/{2}/users/{3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._role_name,
                    user_email)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp
